from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.gis.geos import Point
from .models import User
from .utils import get_geolocation_from_address


@receiver(pre_save, sender=User)
def save_geolocation_from_address(sender, instance, **kwargs):
    """
    Signal to be called before saving User instance,
    handles the geolocation API call
    """

    # Disable this function when loading initial example data from fixture
    if kwargs.get('raw', False):
        return

    # If the address is empty, reset the location point and exit
    if not instance.address:
        instance.location_point = Point(0, 0)
        return

    # If the user is just being created, don't check that address_has_changed
    if (instance.id is None or
            address_has_changed(instance) and
            address_is_valid(instance.address)):

        api_result = get_geolocation_from_address(instance.address)

        # Update geolocation point (lat and lng)
        instance.location_point = api_result['point']

        # Update address to full formatted adress
        instance.address = api_result['address']


def address_is_valid(address) -> bool:
    """Check that the address doesn't start with ERROR"""
    return not address.startswith('ERROR')


def address_has_changed(instance) -> bool:
    """
    Check that the newly saved address
    is different from the already saved
    """
    return (instance.address != get_user_model()
            .objects.get(id=instance.id).address)
