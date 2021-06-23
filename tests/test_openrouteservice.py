import os

from stpd.openrouteservice._openrouteservice import OpenRouteService


def test_OpenRouteService():
    ors = OpenRouteService(os.getenv('ORS_SECRET'))
    ors(location_strs=['toronto ontario', 'hamilton ontario'])
