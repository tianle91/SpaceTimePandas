from datetime import date

import pandas as pd

from stpd.location import OpenStreetMap, SimpleMaps
from stpd.pipeline import Pipeline
from stpd.utils_geocode import get_lat_lon
from stpd.weather import NOAA, ClimateWeatherGC

lat, lon = get_lat_lon('Toronto, Canada')
df = pd.DataFrame({
    'lat': lat,
    'lon': lon,
    'date': [date(2020, 1, 1 + i) for i in range(2)]
})


p = Pipeline([
    OpenStreetMap(),
    SimpleMaps(),
    NOAA(),
    ClimateWeatherGC(),
])


def test_pipeline():
    p.add_features_to_df(df, date_col='date', lat_col='lat', lon_col='lon')
