from datetime import date

import pytest

from stpd import NOAA, ClimateWeatherGC, OpenStreetMap, SimpleMaps

# Toronto
LAT = 43.700111
LON = -79.416298
START_DATE = date(2021, 5, 7)
END_DATE = date(2021, 5, 9)


def test_noaa():
    noaa = NOAA(LAT, LON)
    noaa.get_historical(START_DATE, END_DATE)


def test_cwgc():
    cwgc = ClimateWeatherGC(LAT, LON)
    cwgc.get_historical(START_DATE, END_DATE)


@pytest.mark.parametrize(
    'lat_lon_list',
    [
        pytest.param([(LAT, LON)], id='single'),
        pytest.param([(LAT, LON), (LAT, LON)], id='double')
    ]
)
def test_simplemaps(lat_lon_list):
    sm = SimpleMaps(lat_lon_list=lat_lon_list)
    sm.get_features()


@pytest.mark.parametrize(
    'lat_lon_list',
    [
        pytest.param([(LAT, LON)], id='single'),
        pytest.param([(LAT, LON), (LAT, LON)], id='double')
    ]
)
def test_openstreemap(lat_lon_list):
    osm = OpenStreetMap(lat_lon_list=lat_lon_list)
    osm.get_features()
