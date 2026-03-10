from django.urls import path
from . import views

urlpatterns = [
    # Frontend
    path('', views.serve_frontend, name='frontend'),
    
    # API Root
    
    # Disaster Analysis
    path('analyze/', views.analyze_disaster, name='analyze_disaster'),
    path('disaster-types/', views.get_disaster_types, name='get_disaster_types'),
    
    # Incidents
    path('incidents/', views.get_incidents, name='get_incidents'),
    path('incidents/<int:incident_id>/', views.get_incident_detail, name='get_incident_detail'),
    
    # Emergency Contacts
    path('emergency-contacts/', views.get_emergency_contacts, name='get_emergency_contacts'),
    
    # Weather
    path('weather/', views.get_weather, name='get_weather'),
    
    # Route Calculation
    path('calculate-route/', views.calculate_route, name='calculate_route'),
    
    # Dashboard
    path('dashboard-stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
]
