import logging
from datetime import date, datetime
from io import StringIO
from typing import List, Optional

import pandas as pd
import requests
import requests_cache
from geopy import distance
from pytz import timezone
from timezonefinder import TimezoneFinder

from stpd.constants import TARGET_DATE_COL, TARGET_LAT_COL, TARGET_LON_COL

from .base import BaseWeather

session = requests_cache.CachedSession(namespace='noaa')
TZFINDER = TimezoneFinder()
logger = logging.getLogger(__name__)

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


def get_closest_valid_station_ids(
    lat: float,
    lon: float,
    dt: date,
    elements: Optional[List[str]] = None,
) -> pd.Series:
    """Return station ids reported to be active at dt by ghncd-inventory.txt, closest first.
    """
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
        lambda row: distance.distance(
            (row[latcol], row[loncol]),
            (lat, lon)
        ).km,
        axis=1
    )
    return station_inventory.sort_values('distance')['ID']


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
    df[TARGET_DATE_COL] = df['DATE'].apply(get_localized_datetime)
    df = df.drop(columns=['DATE'])
    df = df.astype({c: DAILY_DTYPES[c] for c in df.columns if c in DAILY_DTYPES})
    return df


class NOAA(BaseWeather):
    """
    https://www.ncdc.noaa.gov/homr/
    https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation
    """

    def __init__(self, date_col: str, lat_col: str, lon_col: str, elements=None) -> None:
        super().__init__(date_col, lat_col, lon_col)
        self.elements = elements

    def get_features(self, dt: date, lat: float, lon: float) -> pd.DataFrame:
        if dt >= date.today():
            raise ValueError(f'No data available for {dt} >= {date.today()}')
        closest_valid_stations = get_closest_valid_station_ids(
            lat=lat, lon=lon, dt=dt, elements=self.elements)
        for station_id in closest_valid_stations:
            # format request
            dt_str = dt.strftime('%Y-%m-%d')
            url = (
                'https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries'
                f'&stations={station_id}&startDate={dt_str}&endDate={dt_str}'
                '&format=json'
            )
            response_json = session.get(url).json()
            if len(response_json) > 0:
                df = format_df(response_json, tzstr=TZFINDER.timezone_at(lng=lon, lat=lat))
                df[TARGET_LAT_COL] = lat
                df[TARGET_LON_COL] = lon
                return df
            else:
                # NOAA inventory is accurate
                logger.warn(f'No data available for station_id: {station_id} at {dt}')
        raise ValueError(f'No data available for {dt}')
