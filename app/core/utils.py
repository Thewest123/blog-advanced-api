import os
import requests
from django.contrib.gis.geos import Point
from rest_framework import status
from typing import Dict


def get_geolocation_from_address(address: str) -> Dict[Point, str]:
    """
    Returns geolocation point with latitude and longitude
    and formatted-address
    from provided string adress
    """

    payload = {
        'key': os.environ.get('GOOGLE_GEOCODING_API_KEY'),
        'language': 'cs',
        'address': address
    }

    # Call API
    response = requests.get(os.environ.get(
        'GOOGLE_GEOCODING_API_LINK'), params=payload)

    # Parse response
    r = response.json()

    if response.status_code == status.HTTP_200_OK and r['status'] == 'OK':

        lat = r['results'][0]['geometry']['location']['lat']
        lng = r['results'][0]['geometry']['location']['lng']
        address = r['results'][0]['formatted_address']

        return {
            'point': Point(lng, lat),
            'address': address
        }

    return Point(0, 0), 'Chyba'
