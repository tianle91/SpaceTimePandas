import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Union

import geopy
import geopy.distance
from geopy import Point
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

from stpd.utils_geocode import get_lat_lon

from ._osm_features import DEFAULT_FEATURE_NAMES, FEATURES

OVERPASS = Overpass()

logger = logging.getLogger(__name__)


def get_bounding_box_around(point: Point, radius_km=1.) -> Tuple[float, float, float, float]:
    center = point
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
    point: Point,
    elementType: Union[str, List[str]],
    selector: str,
    radius_km: float = 1.,
    dt: Optional[datetime] = None,
) -> int:
    query = overpassQueryBuilder(
        bbox=get_bounding_box_around(point, radius_km=radius_km),
        elementType=elementType,
        selector=selector,
        out='count'
    )
    # https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#date
    p = {}
    if dt is not None:
        if dt.tzinfo is None:
            logger.warning(f'No tzinfo provided for dt:{dt}, assuming is UTC.')
        dt = dt.astimezone(timezone.utc)
        p.update({'date': f'{dt.isoformat()}'})
    result = OVERPASS.query(query, timeout=60, **p)
    return result.countElements()


class OpenStreetMap:
    """Give location receive features.
    """

    def __init__(
        self,
        feature_names: List[str] = DEFAULT_FEATURE_NAMES,
        feature_query_values: Dict[str, tuple] = {},
        radius_km=1.
    ) -> None:
        """
        Args:
            feature_names: names of features in stpd.location.OSMFeatures
            feature_query_values: dict of feature_name to (elementType, selector).
                These are passed into overpassQueryBuilder.
        """
        self.selected_features = feature_query_values
        self.selected_features.update({
            feature_name: FEATURES[feature_name]
            for feature_name in feature_names
        })
        self.radius_km = radius_km

    def __call__(
        self,
        location_str: Optional[str] = None,
        point: Optional[Point] = None,
        dt: Optional[datetime] = None,
    ) -> dict:
        if point is not None:
            point = point
        elif location_str is not None:
            lat, lon = get_lat_lon(s=location_str)
            point = Point(latitude=lat, longitude=lon)
        else:
            raise ValueError('At least one of location_str or point must be provided!')
        res = {}
        for feature_name, v in self.selected_features.items():
            elementType, selector = v
            res[f'count_{feature_name}'] = get_count_around(
                point=point,
                elementType=elementType,
                selector=selector,
                radius_km=self.radius_km,
                dt=dt
            )
        return res
