import random
from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.weather.models import City, WeatherData

SAMPLE_CITIES = [
    {"name": "London", "country": "UK", "lat": 51.5074, "lon": -0.1278},
    {"name": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"name": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"name": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"name": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
]

WEATHER_DESCRIPTIONS = [
    "Clear sky",
    "Partly cloudy",
    "Overcast",
    "Light rain",
    "Heavy rain",
    "Thunderstorm",
    "Foggy",
    "Sunny",
]

class Command(BaseCommand):
    help = 'Loads sample weather data for demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--records-per-city',
            type=int,
            default=500,
            help='Number of weather records to generate per city'
        )

    def handle(self, *args, **options):
        records_per_city = options['records_per_city']
        
        try:
            with transaction.atomic():
                # Create cities
                cities = []
                for city_data in SAMPLE_CITIES:
                    city, created = City.objects.get_or_create(
                        name=city_data["name"],
                        country=city_data["country"],
                        defaults={
                            "latitude": city_data["lat"],
                            "longitude": city_data["lon"]
                        }
                    )
                    cities.append(city)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created city: {city.name}'))

                # Generate weather data
                weather_records = []
                base_time = datetime.now(pytz.UTC) - timedelta(days=30)
                
                for city in cities:
                    # Base temperature for the city (varying by latitude)
                    base_temp = 20 - (abs(float(city.latitude)) / 5)
                    
                    for i in range(records_per_city):
                        # Add some randomness to the data
                        temp_variation = random.uniform(-5, 5)
                        humidity_variation = random.uniform(-10, 10)
                        
                        record_time = base_time + timedelta(
                            hours=i * (24 / (records_per_city/30))
                        )
                        
                        weather_records.append(WeatherData(
                            city=city,
                            temperature=base_temp + temp_variation,
                            humidity=min(max(60 + humidity_variation, 0), 100),
                            pressure=random.randint(980, 1020),
                            wind_speed=random.uniform(0, 20),
                            description=random.choice(WEATHER_DESCRIPTIONS),
                            recorded_at=record_time
                        ))

                # Bulk create weather records
                WeatherData.objects.bulk_create(weather_records)
                
                total_records = len(weather_records)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {total_records} weather records '
                        f'for {len(cities)} cities'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading weather data: {str(e)}')
            )