from datetime import date
from stpd import ClimateWeatherGC, SimpleMaps, NOAA


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


def test_simplemaps():
    sm = SimpleMaps([LAT, LON])
    sm.get_features()
