from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.common.models import BaseModel


class City(BaseModel):
    """
    Model to store city information for weather data
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )
    
    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ['latitude', 'longitude']
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherData(BaseModel):
    """
    Model to store weather data for cities
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_data')
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    pressure = models.IntegerField() 
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)  # in m/s
    description = models.CharField(max_length=200)
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = "Weather Data"
        unique_together = ['city', 'recorded_at'] 

    def __str__(self):
        return f"{self.city.name} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
