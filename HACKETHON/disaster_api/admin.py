from django.contrib import admin
from .models import (
    DisasterType, DisasterIncident, ResourceCalculation,
    EmergencyContact, WeatherData, RescueRoute
)


@admin.register(DisasterType)
class DisasterTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description']
    search_fields = ['name']


@admin.register(DisasterIncident)
class DisasterIncidentAdmin(admin.ModelAdmin):
    list_display = ['disaster_type', 'location', 'severity', 'population_affected', 'risk_level', 'priority', 'is_active', 'created_at']
    list_filter = ['disaster_type', 'severity', 'risk_level', 'priority', 'is_active', 'created_at']
    search_fields = ['location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('disaster_type', 'location', 'latitude', 'longitude', 'description')
        }),
        ('Impact Assessment', {
            'fields': ('severity', 'population_affected', 'risk_level', 'priority')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ResourceCalculation)
class ResourceCalculationAdmin(admin.ModelAdmin):
    list_display = ['incident', 'food_packets', 'water_liters', 'medical_kits', 'shelters', 'rescue_teams', 'calculated_at']
    readonly_fields = ['calculated_at']
    
    fieldsets = (
        ('Basic Resources', {
            'fields': ('food_packets', 'water_liters', 'medical_kits', 'shelters')
        }),
        ('Personnel Resources', {
            'fields': ('rescue_teams', 'volunteers', 'medical_teams')
        }),
        ('Vehicle Resources', {
            'fields': ('ambulances', 'firetrucks', 'helicopters')
        }),
        ('Timestamps', {
            'fields': ('calculated_at',)
        }),
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'description', 'icon', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'temperature', 'humidity', 'flood_risk', 'recorded_at']
    list_filter = ['flood_risk', 'recorded_at']
    search_fields = ['location']
    readonly_fields = ['recorded_at']


@admin.register(RescueRoute)
class RescueRouteAdmin(admin.ModelAdmin):
    list_display = ['start_location', 'end_location', 'distance_km', 'estimated_time_minutes', 'created_at']
    search_fields = ['start_location', 'end_location']
    readonly_fields = ['created_at']
