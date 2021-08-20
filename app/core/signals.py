from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User
from .utils import get_geolocation_from_address


@receiver(pre_save, sender=User)
def save_geolocation_from_address(sender, instance, **kwargs):
    """
    Signal to be called before saving User instance,
    handles the geolocation API call
    """

    # If instance is being created, do nothing
    if instance.id is None:
        pass

    else:

        # If either lat or lng are empty
        # and address is provided, make API call
        if ((not instance.lat() or
            not instance.lng()) and
                instance.address):

            api_result = get_geolocation_from_address(instance.address)

            # Update geolocation point (lat and lng)
            instance.location_point = api_result['point']

            # Update address to full formatted adress
            instance.address = api_result['address']
