from datetime import date

from stpd import NOAA, ClimateWeatherGC, OpenStreetMap, SimpleMaps

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


def test_openstreemap():
    osm = OpenStreetMap()
    osm.get_features(LAT, LON)
