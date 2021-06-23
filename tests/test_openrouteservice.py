import os

from stpd.openrouteservice import OpenRouteService


def test_OpenRouteService():
    ors = OpenRouteService(api_key=os.getenv('ORS_SECRET'))
    ors(location_strs=['toronto ontario', 'hamilton ontario'])
