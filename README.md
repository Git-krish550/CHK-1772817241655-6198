# AI Disaster Resource Optimizer - Django Backend

A Django REST API backend for the AI Disaster Resource Optimizer application. This backend provides comprehensive disaster management capabilities including resource calculation, incident tracking, and emergency response coordination.

## Features

- **Disaster Analysis**: Analyze disasters and calculate required resources
- **Resource Management**: Calculate and track required resources (food, water, medical, shelter, personnel)
- **Incident Tracking**: Track disaster incidents with severity levels and risk assessment
- **Emergency Contacts**: Manage emergency contact information
- **Weather Integration**: Get weather data to assess flood risks
- **Route Planning**: Calculate rescue routes for emergency response
- **Dashboard Statistics**: Real-time statistics and incident monitoring

## API Endpoints

### Disaster Analysis
- `POST /api/analyze/` - Analyze disaster and calculate resources
- `GET /api/disaster-types/` - Get all disaster types

### Incidents
- `GET /api/incidents/` - Get all active incidents
- `GET /api/incidents/{id}/` - Get incident details

### Emergency Services
- `GET /api/emergency-contacts/` - Get emergency contacts
- `GET /api/weather/?location={location}` - Get weather data
- `POST /api/calculate-route/` - Calculate rescue route

### Dashboard
- `GET /api/dashboard-stats/` - Get dashboard statistics

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HACKETHON
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data (optional)**
   ```bash
   python manage.py loadseed initial_data.json
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Usage Examples

### Analyze a Disaster
```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "Flood",
    "severity": 2,
    "population": 5000,
    "location": "Mumbai, India"
  }'
```

### Get Weather Data
```bash
curl "http://localhost:8000/api/weather/?location=Mumbai"
```

### Calculate Rescue Route
```bash
curl -X POST http://localhost:8000/api/calculate-route/ \
  -H "Content-Type: application/json" \
  -d '{
    "start": "Mumbai Airport",
    "end": "Gateway of India"
  }'
```

## Frontend Integration

The frontend (`main.html`) can be updated to use these API endpoints instead of client-side calculations. Update the JavaScript functions to make API calls:

```javascript
async function predict() {
    const response = await fetch('/api/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            disaster_type: document.getElementById("disaster").value,
            severity: parseInt(document.getElementById("severity").value),
            population: parseInt(document.getElementById("people").value),
            location: document.getElementById("location").value
        })
    });
    
    const data = await response.json();
    // Update UI with response data
}
```

## Database Models

### DisasterIncident
- Tracks disaster incidents with location, severity, and affected population
- Calculates risk levels and priority
- Stores resource requirements

### ResourceCalculation
- Stores calculated resources for each incident
- Includes food, water, medical supplies, shelter, and personnel

### EmergencyContact
- Manages emergency contact information
- Includes phone numbers and descriptions

### WeatherData
- Stores weather information for locations
- Tracks flood risk indicators

### RescueRoute
- Stores rescue route information
- Calculates distances and estimated times

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to:
- Manage disaster incidents
- Update emergency contacts
- View weather data
- Monitor rescue routes

## Development

### Adding New Features

1. **Models**: Add new models in `disaster_api/models.py`
2. **Serializers**: Create serializers in `disaster_api/serializers.py`
3. **Views**: Implement API views in `disaster_api/views.py`
4. **URLs**: Add URL patterns in `disaster_api/urls.py`

### Running Tests

```bash
python manage.py test
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### CORS Settings

Update `CORS_ALLOWED_ORIGINS` in `settings.py` for production:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Production Deployment

1. **Set DEBUG=False** in settings.py
2. **Configure ALLOWED_HOSTS**
3. **Set up a production database** (PostgreSQL recommended)
4. **Configure static files serving**
5. **Set up HTTPS**
6. **Use a production WSGI server** (Gunicorn recommended)

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.
