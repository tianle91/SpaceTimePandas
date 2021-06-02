from datetime import date

from stpd.weather import NOAA, ClimateWeatherGC

# Toronto
LAT = 43.6534817
LON = -79.3839347
START_DATE = date(2021, 5, 7)
END_DATE = date(2021, 5, 9)


def test_noaa():
    noaa = NOAA(date_col='date', lat_col='lat', lon_col='lon')
    noaa.get_features(dt=START_DATE, lat=LAT, lon=LON)


def test_cwgc():
    cwgc = ClimateWeatherGC(date_col='date', lat_col='lat', lon_col='lon')
    cwgc.get_features(dt=START_DATE, lat=LAT, lon=LON)
