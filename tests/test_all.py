from datetime import date

import numpy as np
import pytest

from stpd.location import OpenStreetMap, OSMFeatures, SimpleMaps
from stpd.weather import NOAA, ClimateWeatherGC

# Toronto
LAT = 43.6534817
LON = -79.3839347
START_DATE = date(2021, 5, 7)
END_DATE = date(2021, 5, 9)


def test_noaa():
    noaa = NOAA(LAT, LON)
    noaa.get_features(START_DATE)


def test_cwgc():
    cwgc = ClimateWeatherGC(LAT, LON)
    cwgc.get_features(START_DATE)


def test_simplemaps():
    sm = SimpleMaps()
    sm.get_features(LAT, LON)


@pytest.mark.parametrize(
    'feature_names',
    [
        pytest.param(None, id='default')
    ] + [
        pytest.param([n], id=n)
        for n in np.random.choice(list(OSMFeatures.keys()), size=5, replace=False)
    ]
)
def test_openstreemap(feature_names):
    osm = OpenStreetMap(feature_names=feature_names)
    osm.get_features(LAT, LON)


def test_openstreetmap_feature_query_values():
    osm = OpenStreetMap(feature_query_values={'natural=tree': ('node', '"natural"="tree"')})
    osm.get_features(LAT, LON)
