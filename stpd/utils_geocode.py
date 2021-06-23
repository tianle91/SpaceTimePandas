from geopy import Point
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()


def get_point(location_str: str, nom: Nominatim = nominatim) -> Point:
    best_match = nom.query(location_str).toJSON()[0]
    return Point(latitude=best_match['lat'], longitude=best_match['lon'])
