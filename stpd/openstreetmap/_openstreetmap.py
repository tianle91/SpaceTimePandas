from typing import Dict, List, Optional, Tuple, Union

import geopy
import geopy.distance
import pandas as pd
from geopy import Point
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

from ._osm_features import FEATURES

OVERPASS = Overpass()


def get_bounding_box_around(lat, lon, radius_km=1.) -> Tuple[float, float, float, float]:
    """
    https://stackoverflow.com/questions/24427828/calculate-point-based-on-distance-and-direction
    """
    center = Point(lat, lon)
    r = geopy.distance.distance(kilometers=radius_km)
    north: Point = r.destination(point=center, bearing=0)
    east: Point = r.destination(point=center, bearing=90)
    south: Point = r.destination(point=center, bearing=180)
    west: Point = r.destination(point=center, bearing=270)
    return (
        south.latitude,
        west.longitude,
        north.latitude,
        east.longitude
    )


def get_count_around(
    lat: float, lon: float, elementType: Union[str, List[str]], selector: str, radius_km: float = 1.
) -> int:
    query = overpassQueryBuilder(
        bbox=get_bounding_box_around(lat, lon, radius_km=radius_km),
        elementType=elementType,
        selector=selector,
        out='count'
    )
    result = OVERPASS.query(query)
    return result.countElements()


class OpenStreetMap:
    """
    https://wiki.openstreetmap.org/
    https://github.com/mocnik-science/osm-python-tools
    """

    def __init__(
        self,
        feature_names: Optional[List[str]] = None,
        feature_query_values: Optional[Dict[str, tuple]] = None,
    ):
        """
        Args:
            feature_names: names of features in FEATURES
            feature_query_values: dict of feature_name to (elementType, selector), like in FEATURES.
                These are passed into overpassQueryBuilder.
        """
        if (feature_names is None) and (feature_query_values is None):
            raise ValueError('Some features need to be set.')
        if feature_names is None:
            feature_names = []
        self.feature_names = feature_names
        if feature_query_values is None:
            feature_query_values = {}
        self.feature_query_values = feature_query_values

    def get_features(self, lat, lon, radius_km=1.):
        all_df = pd.DataFrame({'target_lat': [lat], 'target_lon': [lon]})
        selected_features = {
            **{feature_name: FEATURES[feature_name] for feature_name in self.feature_names},
            **self.feature_query_values
        }
        for feature_name in selected_features:
            elementType, selector = selected_features[feature_name]
            all_df[f'count_{feature_name}'] = all_df.apply(
                lambda row: get_count_around(
                    row['target_lat'],
                    row['target_lon'],
                    elementType=elementType,
                    selector=selector,
                    radius_km=radius_km
                ),
                axis=1
            )
        return all_df
