from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Avg
from django.db import DatabaseError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import Http404

from .models import City
from .utils import generate_temperature_chart


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)


class CityListView(ListView):
    """View to list all cities with their weather data"""
    model = City
    template_name = 'weather/city_list.html'
    context_object_name = 'cities'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Add average weather stats for each city
            cities_with_stats = []
            hottest_city = None
            coldest_city = None
            most_humid_city = None
            windiest_city = None
            max_temp = float('-inf')
            min_temp = float('inf')
            max_humidity = float('-inf')
            max_wind = float('-inf')

            for city in context['cities']:
                stats = city.weather_data.aggregate(
                    avg_temp=Avg('temperature'),
                    avg_humidity=Avg('humidity'),
                    avg_wind_speed=Avg('wind_speed')
                )
                city.stats = stats
                cities_with_stats.append(city)
                
                # Track extreme values
                if stats['avg_temp'] is not None:
                    if stats['avg_temp'] > max_temp:
                        max_temp = stats['avg_temp']
                        hottest_city = city
                    if stats['avg_temp'] < min_temp:
                        min_temp = stats['avg_temp']
                        coldest_city = city
                
                if stats['avg_humidity'] is not None and stats['avg_humidity'] > max_humidity:
                    max_humidity = stats['avg_humidity']
                    most_humid_city = city
                    
                if stats['avg_wind_speed'] is not None and stats['avg_wind_speed'] > max_wind:
                    max_wind = stats['avg_wind_speed']
                    windiest_city = city

            context['cities'] = cities_with_stats
            context['weather_summary'] = {
                'hottest_city': hottest_city,
                'coldest_city': coldest_city,
                'most_humid_city': most_humid_city,
                'windiest_city': windiest_city
            }
        except DatabaseError as e:
            messages.error(self.request, f"Database error while calculating statistics: {str(e)}")
        return context


class CityDetailView(DetailView):
    """View to display detailed information about a specific city and its weather data"""
    model = City
    template_name = 'weather/city_detail.html'
    context_object_name = 'city'
    paginate_by = 10  # Number of records per page

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            raise  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Get the weather data with pagination
            page = self.request.GET.get('page', 1)
            weather_data_list = self.object.weather_data.order_by('-recorded_at')
            paginator = Paginator(weather_data_list, self.paginate_by)
            
            try:
                weather_data = paginator.page(page)
            except PageNotAnInteger:
                weather_data = paginator.page(1)
            except EmptyPage:
                weather_data = paginator.page(paginator.num_pages)
            
            context['weather_data'] = weather_data
            
            # Calculate averages
            stats = self.object.weather_data.aggregate(
                avg_temp=Avg('temperature'),
                avg_humidity=Avg('humidity'),
                avg_wind_speed=Avg('wind_speed')
            )
            context['stats'] = stats

            # Generate temperature chart
            context['temperature_chart'] = generate_temperature_chart(weather_data.object_list[:10])
        except ObjectDoesNotExist:
            pass 
        except DatabaseError:
            pass  
        return context
