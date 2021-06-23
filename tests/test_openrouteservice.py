from stpd.openrouteservice._openrouteservice import OpenRouteService


def test_OpenRouteService():
    with open('ors.secret') as f:
        ors = OpenRouteService(f.read())
    ors(location_strs=['toronto ontario', 'hamilton ontario'])
