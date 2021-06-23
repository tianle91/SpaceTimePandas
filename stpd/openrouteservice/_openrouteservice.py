from typing import List, Optional

import openrouteservice
from geopy import Point

from stpd.utils_geocode import get_point


def route_features(routes) -> dict:
    return routes['routes'][0]['summary']


class OpenRouteService:
    """Give location receive features.
    """

    def __init__(
        self,
        api_key: str
    ) -> None:
        """
        Args:
            api_key: https://openrouteservice.org/
        """
        self.client = openrouteservice.Client(key=api_key)

    def __call__(
        self,
        location_strs: Optional[List[str]] = None,
        points: Optional[List[Point]] = None,
    ) -> dict:
        if points is not None:
            points = points
        elif location_strs is not None:
            points = [get_point(s) for s in location_strs]
        else:
            raise ValueError('At least one of location_strs or points must be provided!')
        coords = tuple([
            # this is longitude and latitude!
            # the default example is in germany, not somalia
            (p.longitude, p.latitude) for p in points
        ])
        routes = self.client.directions(coords)
        return route_features(routes)
