from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    """
    Django command that for each user bulk fills
    the location point(latitude and langitude) from adress,
    if empty
    """

    def handle(self, *args, **options):
        """Handle the command"""
        users = get_user_model().objects.filter(location_point__isnull=True)
        for user in users:
            # TODO: Reverse geocoding API call
            user.location_point = Point(12.3456, 12.3456)
            user.save()
            print(f'Obtained lat+lng for user {user}')
