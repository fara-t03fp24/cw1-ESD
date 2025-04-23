from django.contrib import admin
from .models import City, WeatherData


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin interface for City model"""
    list_display = ('name', 'country', 'latitude', 'longitude')
    search_fields = ('name', 'country')
    list_filter = ('country',)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    """Admin interface for WeatherData model"""
    list_display = ('city', 'temperature', 'humidity', 'pressure', 
                   'wind_speed', 'description', 'recorded_at')
    search_fields = ('city__name', 'description')
    list_filter = ('city', 'recorded_at')
    date_hierarchy = 'recorded_at'
