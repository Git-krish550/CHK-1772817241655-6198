from django.http import JsonResponse, FileResponse
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
import requests
import math
from django.db import models

from .models import (
    DisasterType, DisasterIncident, ResourceCalculation,
    EmergencyContact, WeatherData, RescueRoute
)
from .serializers import (
    DisasterTypeSerializer, DisasterIncidentSerializer,
    ResourceCalculationSerializer, EmergencyContactSerializer,
    WeatherDataSerializer, RescueRouteSerializer,
    DisasterAnalysisSerializer, ResourceRequestSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
    API root - provides information about available endpoints
    """
    return Response({
        'message': 'AI Disaster Resource Optimizer API',
        'version': '1.0.0',
        'endpoints': {
            'analyze_disaster': '/api/analyze/ (POST)',
            'disaster_types': '/api/disaster-types/ (GET)',
            'incidents': '/api/incidents/ (GET)',
            'incident_detail': '/api/incidents/<id>/ (GET)',
            'emergency_contacts': '/api/emergency-contacts/ (GET)',
            'weather': '/api/weather/?location=<location> (GET)',
            'calculate_route': '/api/calculate-route/ (POST)',
            'dashboard_stats': '/api/dashboard-stats/ (GET)',
        },
        'admin': '/admin/',
        'status': 'running'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_disaster(request):
    """
    Analyze disaster and calculate required resources
    """
    serializer = DisasterAnalysisSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Get or create disaster type
        disaster_type, created = DisasterType.objects.get_or_create(
            name=data['disaster_type'],
            defaults={'icon': get_disaster_icon(data['disaster_type'])}
        )
        
        # Calculate resources
        resources = calculate_resources(
            data['severity'], 
            data['population'], 
            data['disaster_type']
        )
        
        # Calculate risk level
        risk_score = (data['severity'] * 2) + (data['population'] / 500)
        risk_level = 'Low'
        if risk_score > 5:
            risk_level = 'Medium'
        if risk_score > 10:
            risk_level = 'High'
        
        # Calculate priority
        priority = 'Normal'
        if data['population'] > 1000 and data['severity'] == 3:
            priority = 'CRITICAL'
        elif data['population'] > 500 or data['severity'] == 3:
            priority = 'High'
        
        # Create disaster incident
        incident = DisasterIncident.objects.create(
            disaster_type=disaster_type,
            location=data['location'],
            severity=data['severity'],
            population_affected=data['population'],
            risk_level=risk_level,
            priority=priority
        )
        
        # Create resource calculation
        resource_calc = ResourceCalculation.objects.create(
            incident=incident,
            **resources
        )
        
        # Get weather data
        weather_data = get_weather_data(data['location'])
        
        # Return response
        response_data = {
            'incident_id': incident.id,
            'risk_level': risk_level,
            'priority': priority,
            'resources': resources,
            'summary': f"📍 {data['location']} | 👥 {data['population']} people affected",
            'weather': weather_data,
            'map_url': f"https://maps.google.com/maps?q={data['location']}&output=embed"
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_disaster_types(request):
    """
    Get list of all disaster types
    """
    disasters = DisasterType.objects.all()
    serializer = DisasterTypeSerializer(disasters, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_incidents(request):
    """
    Get list of all disaster incidents
    """
    incidents = DisasterIncident.objects.filter(is_active=True).order_by('-created_at')
    serializer = DisasterIncidentSerializer(incidents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_incident_detail(request, incident_id):
    """
    Get detailed information about a specific incident
    """
    incident = get_object_or_404(DisasterIncident, id=incident_id)
    serializer = DisasterIncidentSerializer(incident)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_emergency_contacts(request):
    """
    Get list of emergency contacts
    """
    contacts = EmergencyContact.objects.filter(is_active=True)
    serializer = EmergencyContactSerializer(contacts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_weather(request):
    """
    Get weather information for a location
    """
    location = request.GET.get('location', '')
    if not location:
        return Response({'error': 'Location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    weather_data = get_weather_data(location)
    return Response(weather_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_route(request):
    """
    Calculate rescue route between two locations
    """
    start = request.data.get('start', '')
    end = request.data.get('end', '')
    
    if not start or not end:
        return Response({'error': 'Both start and end locations are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create rescue route record
    route = RescueRoute.objects.create(
        start_location=start,
        end_location=end
    )
    
    # Generate map URL
    map_url = f"https://maps.google.com/maps?saddr={start}&daddr={end}&output=embed"
    
    response_data = {
        'route_id': route.id,
        'start_location': start,
        'end_location': end,
        'map_url': map_url,
        'summary': f"Fastest route from {start} to {end}"
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_dashboard_stats(request):
    """
    Get dashboard statistics
    """
    total_incidents = DisasterIncident.objects.filter(is_active=True).count()
    high_priority_incidents = DisasterIncident.objects.filter(is_active=True, priority='CRITICAL').count()
    total_people_affected = DisasterIncident.objects.filter(is_active=True).aggregate(
        total=models.Sum('population_affected')
    )['total'] or 0
    
    # Get recent incidents
    recent_incidents = DisasterIncident.objects.filter(is_active=True).order_by('-created_at')[:5]
    recent_serializer = DisasterIncidentSerializer(recent_incidents, many=True)
    
    stats = {
        'total_incidents': total_incidents,
        'high_priority_incidents': high_priority_incidents,
        'total_people_affected': total_people_affected,
        'recent_incidents': recent_serializer.data
    }
    
    return Response(stats)


def calculate_resources(severity, population, disaster_type):
    """
    Calculate required resources based on severity and population
    """
    food = math.ceil((population * severity) / 2)
    water = math.ceil((population * severity) * 1.5)
    medical = math.ceil(population / 10) * severity
    shelters = math.ceil(population / 25)
    rescue = math.ceil((population * severity) / 8)
    volunteers = math.ceil(population / 20)
    
    ambulances = math.ceil(population / 100)
    firetrucks = math.ceil(population / 200)
    medical_teams = math.ceil(population / 150)
    helicopters = math.ceil(population / 500)
    
    # Adjust firetrucks based on disaster type
    if disaster_type not in ['Flood', 'Cyclone', 'Tsunami']:
        firetrucks = math.ceil(population / 100)
    
    return {
        'food_packets': food,
        'water_liters': water,
        'medical_kits': medical,
        'shelters': shelters,
        'rescue_teams': rescue,
        'volunteers': volunteers,
        'ambulances': ambulances,
        'firetrucks': firetrucks,
        'medical_teams': medical_teams,
        'helicopters': helicopters
    }


def get_disaster_icon(disaster_type):
    """
    Get icon for disaster type
    """
    icons = {
        'Flood': '🌊',
        'Earthquake': '🏚️',
        'Cyclone': '🌀',
        'Wildfire': '🔥',
        'Landslide': '⛰️',
        'Tsunami': '🌊',
        'Drought': '🏜️',
        'Heatwave': '🌡️'
    }
    return icons.get(disaster_type, '⚠️')


def get_weather_data(location):
    """
    Get weather data for a location
    """
    try:
        # Using wttr.in service
        response = requests.get(f"https://wttr.in/{location}?format=j1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_condition', [{}])[0]
            
            weather_info = {
                'temperature': float(current.get('temp_C', 0)),
                'humidity': float(current.get('humidity', 0)),
                'description': current.get('weatherDesc', [{}])[0].get('value', ''),
                'flood_risk': 'rain' in current.get('weatherDesc', [{}])[0].get('value', '').lower()
            }
            
            # Save to database
            WeatherData.objects.create(
                location=location,
                **weather_info
            )
            
            return weather_info
    except:
        pass
    
    return {
        'temperature': None,
        'humidity': None,
        'description': 'Weather data unavailable',
        'flood_risk': False
    }


def serve_frontend(request):
    """
    Serve the main.html frontend file
    """
    import os
    from django.http import HttpResponse
    
    # Look for main.html in the project root
    main_html_path = os.path.join(settings.BASE_DIR, 'main.html')
    
    if os.path.exists(main_html_path):
        with open(main_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    else:
        # If main.html not found, redirect to API info
        from django.shortcuts import redirect
        return redirect('api_info')
