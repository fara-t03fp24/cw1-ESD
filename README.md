# ClimateWatch - Weather Monitoring System

Welcome to ClimateWatch, a collaborative project developed by group of students for the Enterprise Software Development (CS551Q) course at the University of Aberdeen. Our team has created a sophisticated weather monitoring system that provides weather data visualization and analysis.

## Team Members
- Student ID: 52428842 - Frontend Development, UI/UX Design
- Student ID: 52427848 - Backend Development, Database Design
- Student ID: 52426836 - Testing, Quality Assurance
- Student ID: 52428214 - DevOps, Deployment
- Student ID: 52319768 - Documentation, Project Management

## Project Overview

ClimateWatch was developed to address the need for an intuitive and comprehensive weather monitoring system. Our solution provides weather data visualization for cities worldwide, making it easier for users to track and analyze weather patterns.

### Key Features

- 📊 **Interactive Dashboard**: Display of weather highlights including temperature, humidity, and wind speed
- 🌍 **Global Coverage**: Monitoring of multiple cities worldwide with detailed weather information
- 📈 **Data Visualization**: Dynamic charts showing temperature trends and weather patterns
- 📱 **Responsive Design**: Mobile-first approach ensuring accessibility across all devices
- 🔄 **Sample Data**: Comprehensive sample weather data generation for demonstration purposes

## Technical Implementation

### Technology Stack
- **Backend**: Django 5.2 for robust server-side operations
- **Database**: PostgreSQL for production, SQLite for development
- **Frontend**: Bootstrap 5 + Custom CSS for responsive design
- **Charting**: Matplotlib for data visualization
- **Deployment**: Render.com cloud platform
- **Static Files**: WhiteNoise for efficient static file serving

### Development Best Practices
- Modular Django architecture
- Comprehensive test coverage
- Code quality enforcement via pre-commit hooks
- Git-based version control
- Continuous Integration/Deployment

## Installation Guide

1. Clone the repository:
```bash
git clone https://github.com/fara-t03fp24/cw1-ESD-52428842-52427848-52426836-52428214-52319768-CS551Q.git
cd cw1-ESD
```

2. Set up virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements/develop.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Initialize database:
```bash
python manage.py migrate
python manage.py load_weather_data --records-per-city 500
```

6. Start development server:
```bash
python manage.py runserver
```

## Live Demo

Visit our live application: [ClimateWatch on Render](https://cw1-esd.onrender.com)

## Project Structure
```
├── apps/
│   ├── common/      # Shared utilities and base models
│   ├── users/       # User authentication and management
│   └── weather/     # Core weather monitoring functionality
├── core/            # Project settings and configuration
├── static/          # Static assets (CSS, JS, images)
├── templates/       # HTML templates
└── requirements/    # Environment-specific dependencies
```

## Testing

Our application includes comprehensive tests covering:
- Model validation and relationships
- View functionality and rendering
- Data processing and visualization
- API endpoints and responses

Run tests with:
```bash
python manage.py test
```

## Learning Outcomes

Through this project, our team:
- Gained practical experience in enterprise software development
- Implemented modern web development best practices
- Developed skills in team collaboration and project management
- Created production-ready software with real-world applications

## Future Enhancements

- Integration with actual weather data APIs
- Real-time weather data updates
- Advanced weather prediction capabilities
- User customization options
- Mobile application development
- API access for third-party integration

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Developed with ❤️ by Team - Enterprise Software Development (CS551Q) - University of Aberdeen
