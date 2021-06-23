from stpd.openstreetmap import OpenStreetMap


def test_OpenStreetMap():
    osm = OpenStreetMap()
    osm('toronto ontario')
