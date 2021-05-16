from typing import Tuple

import numpy as np
import pandas as pd
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

OVERPASS = Overpass()


def get_bounding_box_around(lat, lon, radius_km=1.) -> Tuple[float, float, float, float]:
    # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
    # Latitude: 1 deg = 110.574 km
    # Longitude: 1 deg = 111.320*cos(latitude) km
    lat_delta = radius_km / 110.574
    lon_delta = radius_km / (111.320 * np.cos(lat * np.pi / 180 * np.pi))
    return (
        lat - lat_delta,
        lon - lon_delta,
        lat + lat_delta,
        lon + lon_delta
    )


FEATURES = {
    # https://taginfo.openstreetmap.org/
    # TODO: predefined or user defined features for passing into overpassQueryBuilder
    # feature_name: (elementType, selector)
    'tree': ('node', '"natural"="tree"'),
    'building': (['way', 'relation'], '"building"="yes"'),
}


def get_count_around(lat: float, lon: float, feature_name: str, radius_km: float = 1.) -> int:
    # TODO: do single call with multiple feature_name
    elementType, selector = FEATURES[feature_name]
    bbox = get_bounding_box_around(lat, lon, radius_km=radius_km)
    query = overpassQueryBuilder(
        bbox=bbox, elementType=elementType, selector=selector, out='count')
    result = OVERPASS.query(query)
    return result.countElements()


class OpenStreetMap:
    """
    https://wiki.openstreetmap.org/
    https://github.com/mocnik-science/osm-python-tools
    """

    def __init__(self, feature_names=None):
        if feature_names is None:
            feature_names = ['tree']
        self.feature_names = feature_names

    def get_features(self, lat, lon, radius_km=1.):
        all_df = pd.DataFrame({'target_lat': [lat], 'target_lon': [lon]})
        for feature_name in self.feature_names:
            all_df[f'count_{feature_name}'] = all_df.apply(
                lambda row: get_count_around(
                    row['target_lat'],
                    row['target_lon'],
                    feature_name=feature_name,
                    radius_km=radius_km
                ),
                axis=1
            )
        return all_df
