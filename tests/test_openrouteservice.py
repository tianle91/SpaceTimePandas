import os

from stpd.openrouteservice import (OpenRouteServiceLocationFeatures,
                                   OpenRouteServicePathFeatures)


def test_OpenRouteServicePathFeatures():
    orspathft = OpenRouteServicePathFeatures(api_key=os.getenv('ORS_SECRET'))
    orspathft(location_strs=['toronto ontario', 'hamilton ontario'])


def test_OpenRouteServiceLocationFeatures():
    orslocft = OpenRouteServiceLocationFeatures(api_key=os.getenv('ORS_SECRET'))
    orslocft(location_str='toronto ontario')
