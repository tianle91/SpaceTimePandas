from typing import List, Optional

import openrouteservice
from geopy import Point

from stpd.utils_geocode import get_point


def route_features(routes) -> dict:
    return routes['routes'][0]['summary']


class OpenRouteServiceBase:

    def __init__(
        self,
        api_key: str
    ) -> None:
        """
        Args:
            api_key: https://openrouteservice.org/
        """
        self.client = openrouteservice.Client(key=api_key)


class OpenRouteServicePathFeatures(OpenRouteServiceBase):
    """Give path receive features.
    """

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


def get_isochrones_features(
    p: Point,
    client: openrouteservice.Client,
    isochrone_seconds_range: List[float] = [100., 200., 500., 1000.],
    attributes: List[str] = ["area", "reachfactor", "total_pop"],
) -> dict:
    res = client.isochrones(
        locations=[(p.longitude, p.latitude)],
        attributes=attributes,
        range=isochrone_seconds_range,
    )
    return {
        f'range_seconds_{ft["properties"]["value"]}_{attr}': ft['properties'][attr]
        for ft in res['features']
        for attr in attributes
    }


class OpenRouteServiceLocationFeatures(OpenRouteServiceBase):
    """Give location receive features.
    """

    def __call__(
        self,
        location_str: Optional[str] = None,
        point: Optional[Point] = None,
    ) -> dict:
        if point is not None:
            point = point
        elif location_str is not None:
            point = get_point(location_str)
        else:
            raise ValueError('At least one of location_str or point must be provided!')
        return get_isochrones_features(point, client=self.client)
