from datetime import date

import pandas as pd

from stpd.location import OpenStreetMap, SimpleMaps
from stpd.pipeline import Pipeline
from stpd.weather import NOAA, ClimateWeatherGC

df = pd.DataFrame({
    'lat': 43.653482,
    'lon': -79.383935,
    'date': [date(2020, 1, 1 + i) for i in range(2)]
})


p = Pipeline([
    OpenStreetMap(lat_col='lat', lon_col='lon'),
    SimpleMaps(lat_col='lat', lon_col='lon'),
    NOAA(date_col='date', lat_col='lat', lon_col='lon'),
    ClimateWeatherGC(date_col='date', lat_col='lat', lon_col='lon'),
])


def test_pipeline():
    p.add_features_to_df(df)
