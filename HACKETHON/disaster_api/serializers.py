from rest_framework import serializers
from .models import (
    DisasterType, DisasterIncident, ResourceCalculation,
    EmergencyContact, WeatherData, RescueRoute
)


class DisasterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterType
        fields = '__all__'


class ResourceCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCalculation
        fields = '__all__'


class DisasterIncidentSerializer(serializers.ModelSerializer):
    disaster_type = DisasterTypeSerializer(read_only=True)
    disaster_type_id = serializers.IntegerField(write_only=True)
    resource_calculation = ResourceCalculationSerializer(read_only=True)
    
    class Meta:
        model = DisasterIncident
        fields = '__all__'


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class RescueRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RescueRoute
        fields = '__all__'


class DisasterAnalysisSerializer(serializers.Serializer):
    disaster_type = serializers.CharField(max_length=50)
    severity = serializers.IntegerField(min_value=1, max_value=3)
    population = serializers.IntegerField(min_value=1)
    location = serializers.CharField(max_length=200)
    
    def validate_disaster_type(self, value):
        valid_disasters = ['Flood', 'Earthquake', 'Cyclone', 'Wildfire', 'Landslide', 'Tsunami', 'Drought', 'Heatwave']
        if value not in valid_disasters:
            raise serializers.ValidationError(f"Invalid disaster type. Must be one of: {valid_disasters}")
        return value


class ResourceRequestSerializer(serializers.Serializer):
    food_packets = serializers.IntegerField()
    water_liters = serializers.IntegerField()
    medical_kits = serializers.IntegerField()
    shelters = serializers.IntegerField()
    rescue_teams = serializers.IntegerField()
    volunteers = serializers.IntegerField()
    ambulances = serializers.IntegerField()
    firetrucks = serializers.IntegerField()
    medical_teams = serializers.IntegerField()
    helicopters = serializers.IntegerField()
