from django.db import models
from django.utils import timezone


class DisasterType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.name


class DisasterIncident(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('High', 'High'),
        ('CRITICAL', 'CRITICAL'),
    ]
    
    disaster_type = models.ForeignKey(DisasterType, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    population_affected = models.IntegerField()
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.disaster_type.name} - {self.location}"
    
    class Meta:
        ordering = ['-created_at']


class ResourceCalculation(models.Model):
    incident = models.OneToOneField(DisasterIncident, on_delete=models.CASCADE)
    food_packets = models.IntegerField()
    water_liters = models.IntegerField()
    medical_kits = models.IntegerField()
    shelters = models.IntegerField()
    rescue_teams = models.IntegerField()
    volunteers = models.IntegerField()
    ambulances = models.IntegerField()
    firetrucks = models.IntegerField()
    medical_teams = models.IntegerField()
    helicopters = models.IntegerField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Resources for {self.incident}"


class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.number}"


class WeatherData(models.Model):
    location = models.CharField(max_length=200)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    flood_risk = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Weather for {self.location}"


class RescueRoute(models.Model):
    start_location = models.CharField(max_length=200)
    end_location = models.CharField(max_length=200)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    estimated_time_minutes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Route: {self.start_location} to {self.end_location}"
