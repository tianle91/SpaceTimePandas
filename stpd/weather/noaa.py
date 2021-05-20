from datetime import date, datetime
from io import StringIO

import numpy as np
import pandas as pd
import requests
from pytz import timezone

from .base import BaseWeather

# --------------------------------------------------------------------------------------------------
# INVENTORY_DF
# https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
# --------------------------------------------------------------------------------------------------
INVENTORY_URL = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'
INVENTORY_COLSPECS = [
    (0, 11),
    (12, 20),
    (21, 30),
    (31, 35),
    (36, 40),
    (41, 45),
]
INVENTORY_COLNAMES = {
    0: 'ID',
    1: 'LATITUDE',
    2: 'LONGITUDE',
    3: 'ELEMENT',
    4: 'FIRSTYEAR',
    5: 'LASTYEAR'
}
INVENTORY_DF = pd.read_fwf(
    StringIO(requests.get(INVENTORY_URL).text), header=None, colspecs=INVENTORY_COLSPECS)
INVENTORY_DF = INVENTORY_DF.rename(columns=INVENTORY_COLNAMES)


DEFAULT_ELEMENTS = ('PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN')


def get_closest_valid_station_id(lat: float, lon: float, dt: date, elements=None) -> str:
    if elements is None:
        elements = DEFAULT_ELEMENTS
    station_inventory = INVENTORY_DF.copy()
    station_inventory = station_inventory.loc[
        (station_inventory['FIRSTYEAR'] <= dt.year)
        & (dt.year <= station_inventory['LASTYEAR'])
    ]
    station_inventory = station_inventory.groupby('ID').agg({
        'LATITUDE': 'first',
        'LONGITUDE': 'first',
        'ELEMENT': lambda x: set(x)
    }).reset_index()
    station_inventory = station_inventory.loc[station_inventory['ELEMENT'].apply(
        lambda x: all([v in x for v in elements])
    )]
    latcol, loncol = 'LATITUDE', 'LONGITUDE'
    station_inventory['distance'] = station_inventory.apply(
        lambda row: float(np.linalg.norm(
            np.array([row[latcol], row[loncol]]) - np.array([lat, lon])
        )),
        axis=1
    )
    return station_inventory.sort_values('distance').iloc[0]['ID']


DAILY_DTYPES = {
    'STATION': str,
    'PRCP': float,
    'SNWD': float,
    'SNOW': float,
    'TMAX': float,
    'TMIN': float,
}


def format_df(response_json, tzstr) -> pd.DataFrame:

    def get_localized_datetime(s):
        dt = datetime.strptime(s, '%Y-%m-%d')
        dt = timezone(tzstr).localize(dt)
        return dt

    df = pd.DataFrame(response_json)
    df['dt'] = df['DATE'].apply(get_localized_datetime)
    df = df.drop(columns=['DATE'])
    df = df.astype({c: DAILY_DTYPES[c] for c in df.columns if c in DAILY_DTYPES})
    return df


class NOAA(BaseWeather):
    """
    https://www.ncdc.noaa.gov/homr/
    https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation
    """

    def get_historical_single_date(self, dt: date) -> pd.DataFrame:
        elements = self.kwargs.get('elements', None)
        station_id = get_closest_valid_station_id(self.lat, self.lon, dt, elements=elements)
        if dt >= date.today():
            raise ValueError(f'No data available for {dt} >= {date.today()}')
        # format request
        dt_str = dt.strftime('%Y-%m-%d')
        url = (
            'https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries'
            f'&stations={station_id}&startDate={dt_str}&endDate={dt_str}'
            '&format=json'
        )
        response_json = requests.get(url).json()
        try:
            return format_df(response_json, tzstr=self.tz)
        except Exception:
            raise ValueError(f'url:\n{url}\nresponse_json:\n{response_json}')
