#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements/production.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

#Load initial weather data
python manage.py load_weather_data --records-per-city 300
