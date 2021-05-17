from datetime import date

import numpy as np
import pytest

from stpd import NOAA, ClimateWeatherGC, OpenStreetMap, SimpleMaps
from stpd.openstreetmap._osm_features import FEATURES as OSM_FEATURES

# Toronto
LAT = 43.6534817
LON = -79.3839347
START_DATE = date(2021, 5, 7)
END_DATE = date(2021, 5, 9)


def test_noaa():
    noaa = NOAA(LAT, LON)
    noaa.get_historical(START_DATE, END_DATE)


def test_cwgc():
    cwgc = ClimateWeatherGC(LAT, LON)
    cwgc.get_historical(START_DATE, END_DATE)


def test_simplemaps():
    sm = SimpleMaps()
    sm.get_features(LAT, LON)


@pytest.mark.parametrize(
    'feature_name',
    [
        pytest.param(n, id=n)
        for n in np.random.choice(list(OSM_FEATURES.keys()), size=5, replace=False)
    ]
)
def test_openstreemap(feature_name):
    osm = OpenStreetMap(feature_names=[feature_name])
    osm.get_features(LAT, LON)
