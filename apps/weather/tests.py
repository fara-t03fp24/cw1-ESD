from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from .models import City, WeatherData
from .utils import generate_temperature_chart
from django.core.management import call_command
from io import StringIO
from django.test import Client
from unittest.mock import patch

class CityModelTests(TestCase):
    def setUp(self):
        self.city_data = {
            'name': 'London',
            'country': 'UK',
            'latitude': Decimal('51.5074'),
            'longitude': Decimal('-0.1278')
        }
        self.city = City.objects.create(**self.city_data)

    def test_city_creation(self):
        self.assertEqual(self.city.name, 'London')
        self.assertEqual(self.city.country, 'UK')
        self.assertEqual(float(self.city.latitude), 51.5074)
        self.assertEqual(float(self.city.longitude), -0.1278)

    def test_city_str_representation(self):
        self.assertEqual(str(self.city), 'London, UK')

    def test_invalid_latitude(self):
        city = City(
            name='Invalid',
            country='Test',
            latitude=91,  # Invalid latitude
            longitude=0
        )
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_invalid_longitude(self):
        city = City(
            name='Invalid',
            country='Test',
            latitude=0,
            longitude=181  # Invalid longitude
        )
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_unique_coordinates(self):
        with self.assertRaises(Exception):
            # Try to create city with same coordinates
            City.objects.create(**self.city_data)

class WeatherDataModelTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='London',
            country='UK',
            latitude=51.5074,
            longitude=-0.1278
        )
        self.weather_data = {
            'city': self.city,
            'temperature': 20.5,
            'humidity': 65,
            'pressure': 1013,
            'wind_speed': 5.5,
            'description': 'Partly cloudy',
            'recorded_at': timezone.now()
        }

    def test_weather_data_creation(self):
        weather = WeatherData.objects.create(**self.weather_data)
        self.assertEqual(float(weather.temperature), 20.5)
        self.assertEqual(weather.humidity, 65)
        self.assertEqual(weather.pressure, 1013)
        self.assertEqual(float(weather.wind_speed), 5.5)
        self.assertEqual(weather.description, 'Partly cloudy')

    def test_invalid_humidity(self):
        weather = WeatherData(
            **{**self.weather_data, 'humidity': 101}  # Invalid humidity
        )
        with self.assertRaises(ValidationError):
            weather.full_clean()

    def test_weather_data_str_representation(self):
        weather = WeatherData.objects.create(**self.weather_data)
        expected_str = f"London - {weather.recorded_at.strftime('%Y-%m-%d %H:%M')}"
        self.assertEqual(str(weather), expected_str)

class WeatherViewTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='London',
            country='UK',
            latitude=51.5074,
            longitude=-0.1278
        )
        self.weather_data = WeatherData.objects.create(
            city=self.city,
            temperature=20.5,
            humidity=65,
            pressure=1013,
            wind_speed=5.5,
            description='Partly cloudy',
            recorded_at=timezone.now()
        )

    def test_city_list_view(self):
        response = self.client.get(reverse('city_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/city_list.html')
        self.assertContains(response, 'London')

    def test_city_detail_view(self):
        response = self.client.get(reverse('city_detail', args=[self.city.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/city_detail.html')
        self.assertContains(response, 'London')
        self.assertContains(response, '20.5')  # Temperature

    def test_city_detail_view_404(self):
        response = self.client.get(reverse('city_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')

class WeatherUtilsTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='London',
            country='UK',
            latitude=51.5074,
            longitude=-0.1278
        )
        # Create multiple weather records
        self.weather_records = []
        base_time = timezone.now()
        for i in range(5):
            self.weather_records.append(
                WeatherData.objects.create(
                    city=self.city,
                    temperature=20.0 + i,
                    humidity=65,
                    pressure=1013,
                    wind_speed=5.5,
                    description='Partly cloudy',
                    recorded_at=base_time + timezone.timedelta(hours=i)
                )
            )

    def test_generate_temperature_chart(self):
        chart_data = generate_temperature_chart(self.weather_records)
        self.assertTrue(isinstance(chart_data, str))
        self.assertTrue(chart_data.startswith('data:image/png;base64,'))

    def test_generate_temperature_chart_empty_data(self):
        chart_data = generate_temperature_chart([])
        self.assertTrue(isinstance(chart_data, str))
        self.assertTrue(chart_data.startswith('data:image/png;base64,'))

class ManagementCommandTests(TestCase):
    def test_load_weather_data_command(self):
        out = StringIO()
        call_command('load_weather_data', '--records-per-city=2', stdout=out)
        self.assertIn('Successfully created', out.getvalue())

    @patch('apps.weather.management.commands.load_weather_data.City.objects.get_or_create')
    def test_load_weather_data_error_handling(self, mock_get_or_create):
        mock_get_or_create.side_effect = Exception('Database error')
        out = StringIO()
        call_command('load_weather_data', stdout=out)
        self.assertIn('Error loading weather data', out.getvalue())

class ErrorHandlerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_404_handler(self):
        response = self.client.get('/nonexistent-path/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        self.assertContains(response, 'Page Not Found', status_code=404)

    def test_custom_error_page_content(self):
        response = self.client.get('/nonexistent-path/')
        self.assertContains(response, 'Return to Weather Dashboard', status_code=404)
        self.assertContains(response, 'got lost in the storm', status_code=404)

class WeatherDataAggregationTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='London',
            country='UK',
            latitude=51.5074,
            longitude=-0.1278
        )
        # Create weather data with known values
        self.timestamps = [
            timezone.now() - timezone.timedelta(hours=i)
            for i in range(5)
        ]
        self.temperatures = [20.0, 22.0, 21.0, 23.0, 19.0]
        
        for temp, timestamp in zip(self.temperatures, self.timestamps):
            WeatherData.objects.create(
                city=self.city,
                temperature=temp,
                humidity=65,
                pressure=1013,
                wind_speed=5.5,
                description='Partly cloudy',
                recorded_at=timestamp
            )

    def test_weather_statistics_calculation(self):
        response = self.client.get(reverse('city_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test context data
        context = response.context
        self.assertTrue('weather_summary' in context)
        
        # Verify statistics
        cities_with_stats = context['cities']
        city_stats = next(city for city in cities_with_stats if city.id == self.city.id)
        
        # Check average temperature calculation
        self.assertAlmostEqual(
            float(city_stats.stats['avg_temp']), 
            sum(self.temperatures) / len(self.temperatures),
            places=2
        )

    def test_pagination_on_city_detail(self):
        response = self.client.get(reverse('city_detail', args=[self.city.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Verify pagination
        weather_data = response.context['weather_data']
        self.assertTrue(hasattr(weather_data, 'paginator'))
        self.assertEqual(len(weather_data.object_list), 5)  # All our test data

class AdvancedWeatherTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name='TestCity',
            country='TestCountry',
            latitude=0,
            longitude=0
        )

    def test_weather_data_bulk_creation(self):
        """Test bulk creation of weather data"""
        data_points = []
        base_time = timezone.now()
        for i in range(100):  # Create 100 data points
            data_points.append(WeatherData(
                city=self.city,
                temperature=20.0 + (i % 5),
                humidity=60 + (i % 20),
                pressure=1013 + (i % 10),
                wind_speed=5.0 + (i % 3),
                description='Test weather',
                recorded_at=base_time + timezone.timedelta(hours=i)
            ))
        
        # Bulk create
        WeatherData.objects.bulk_create(data_points)
        self.assertEqual(WeatherData.objects.count(), 100)
        
        # Test pagination
        response = self.client.get(reverse('city_detail', args=[self.city.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['weather_data']), 10)  # Default pagination

    def test_concurrent_weather_updates(self):
        """Test handling multiple weather updates"""
        from django.db import transaction
        from django.db.utils import IntegrityError
        
        # Create initial weather data
        weather1 = WeatherData.objects.create(
            city=self.city,
            temperature=20.0,
            humidity=60,
            pressure=1013,
            wind_speed=5.0,
            description='Initial weather',
            recorded_at=timezone.now()
        )
        
        # Try to create overlapping weather data
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                WeatherData.objects.create(
                    city=self.city,
                    temperature=21.0,
                    humidity=61,
                    pressure=1014,
                    wind_speed=5.1,
                    description='Overlapping weather',
                    recorded_at=weather1.recorded_at  # Same timestamp
                )

    @patch('apps.weather.utils.plt')
    def test_chart_generation_with_large_dataset(self, mock_plt):
        """Test chart generation with a large dataset"""
        # Create 1000 weather records
        data_points = []
        base_time = timezone.now()
        for i in range(1000):
            data_points.append(WeatherData(
                city=self.city,
                temperature=20.0 + (i % 10),
                humidity=60,
                pressure=1013,
                wind_speed=5.0,
                description='Test weather',
                recorded_at=base_time + timezone.timedelta(hours=i)
            ))
        WeatherData.objects.bulk_create(data_points)
        
        # Get the latest 10 records and generate chart
        latest_data = WeatherData.objects.filter(
            city=self.city
        ).order_by('-recorded_at')[:10]
        
        chart_data = generate_temperature_chart(latest_data)
        self.assertTrue(mock_plt.figure.called)
        self.assertTrue(mock_plt.close.called)
        self.assertTrue(chart_data.startswith('data:image/png;base64,'))

    def test_error_handling_edge_cases(self):
        """Test various error handling edge cases"""
        # Test with missing city
        response = self.client.get(reverse('city_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        
        # Test with invalid page number
        response = self.client.get(
            reverse('city_detail', args=[self.city.pk]) + '?page=invalid'
        )
        self.assertEqual(response.status_code, 200)  # Should handle gracefully
        
        # Test with out of range page
        response = self.client.get(
            reverse('city_detail', args=[self.city.pk]) + '?page=9999'
        )
        self.assertEqual(response.status_code, 200)  # Should handle gracefully
