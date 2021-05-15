from typing import List, Tuple

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
    'trees': ('node', '"natural"="tree"')
}


class OpenStreetMap:
    """
    https://wiki.openstreetmap.org/
    https://github.com/mocnik-science/osm-python-tools
    """

    def __init__(self, lat_lon_list: List[Tuple[float, float]]):
        self.lat_lon_list = lat_lon_list

    def get_features(self, feature_names=None):

        lats, lons = zip(*self.lat_lon_list)
        if feature_names is None:
            feature_names = ['trees']

        all_df = pd.DataFrame({
            'target_lat': lats,
            'target_lon': lons,
        })

        def get_count(lat, lon, feature_name):
            elementType, selector = FEATURES[feature_name]
            bbox = get_bounding_box_around(lat, lon, radius_km=1.)
            query = overpassQueryBuilder(
                bbox=bbox, elementType=elementType, selector=selector, out='count')
            result = OVERPASS.query(query)
            return result.countElements()

        for feature_name in feature_names:
            all_df[f'count_{feature_name}'] = all_df.apply(
                lambda row: get_count(
                    row['target_lat'], row['target_lon'], feature_name=feature_name),
                axis=1
            )
        return all_df
