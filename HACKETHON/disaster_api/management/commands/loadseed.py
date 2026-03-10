from django.core.management.base import BaseCommand
from disaster_api.models import DisasterType, EmergencyContact


class Command(BaseCommand):
    help = 'Load initial seed data for the disaster optimizer'

    def handle(self, *args, **options):
        # Create disaster types
        disaster_types = [
            {'name': 'Flood', 'icon': '🌊', 'description': 'Flooding and water-related disasters'},
            {'name': 'Earthquake', 'icon': '🏚️', 'description': 'Seismic activities and earthquakes'},
            {'name': 'Cyclone', 'icon': '🌀', 'description': 'Cyclones and tropical storms'},
            {'name': 'Wildfire', 'icon': '🔥', 'description': 'Forest fires and wildfires'},
            {'name': 'Landslide', 'icon': '⛰️', 'description': 'Landslides and mudslides'},
            {'name': 'Tsunami', 'icon': '🌊', 'description': 'Tsunami and tidal waves'},
            {'name': 'Drought', 'icon': '🏜️', 'description': 'Drought conditions and water scarcity'},
            {'name': 'Heatwave', 'icon': '🌡️', 'description': 'Extreme heat conditions'},
        ]

        for disaster_data in disaster_types:
            disaster_type, created = DisasterType.objects.get_or_create(
                name=disaster_data['name'],
                defaults=disaster_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created disaster type: {disaster_type.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Disaster type already exists: {disaster_type.name}")
                )

        # Create emergency contacts
        emergency_contacts = [
            {
                'name': 'Ambulance',
                'number': '102',
                'description': 'Medical emergency services',
                'icon': '🚑'
            },
            {
                'name': 'Fire Brigade',
                'number': '101',
                'description': 'Fire emergency services',
                'icon': '🚒'
            },
            {
                'name': 'Police',
                'number': '100',
                'description': 'Police emergency services',
                'icon': '🚔'
            },
            {
                'name': 'Disaster Helpline',
                'number': '108',
                'description': 'National disaster response helpline',
                'icon': '🆘'
            }
        ]

        for contact_data in emergency_contacts:
            contact, created = EmergencyContact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created emergency contact: {contact.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Emergency contact already exists: {contact.name}")
                )

        self.stdout.write(
            self.style.SUCCESS('Seed data loaded successfully!')
        )
