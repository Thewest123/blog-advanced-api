from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from core.utils import get_geolocation_from_address


class Command(BaseCommand):
    """
    Django command that bulk fills for all users
    new location point (lat, lng) if they have the default point (0, 0)
    and new address is set
    """

    def handle(self, *args, **options):
        """Handle the command"""

        # Get users with default location point (0, 0)
        users = get_user_model().objects.filter(
            location_point__distance_lte=(Point(0, 0), Distance(mm=0)))
        for user in users:

            # If user has address to geolocate
            if user.address:
                api_call = get_geolocation_from_address(user.address)

                user.location_point = api_call['point']
                user.address = api_call['address']
                user.save()

                print(f'USER: {user} | New location: {user.address} ',
                      f'[{user.location_point.y}, {user.location_point.x}] ')

            else:
                print(f'USER: {user} | NO new location!')
