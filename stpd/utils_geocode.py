from typing import Tuple

from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()


def get_lat_lon(s: str, nom: Nominatim = nominatim) -> Tuple[float, float]:
    best_match = nom.query(s).toJSON()[0]
    return float(best_match['lat']), float(best_match['lon'])
