from datetime import date, datetime
from io import StringIO

import numpy as np
import pandas as pd
import requests
from pytz import timezone

from .base import BaseWeather

HOURLY_DF_DTYPES = {
    'Longitude (x)': float,
    'Latitude (y)': float,
    'Station Name': str,
    'Climate ID': str,
    'Date/Time (LST)': str,
    'Year': int,
    'Month': int,
    'Day': int,
    'Time (LST)': str,
    'Temp (°C)': float,
    'Temp Flag': str,
    'Dew Point Temp (°C)': float,
    'Dew Point Temp Flag': str,
    'Rel Hum (%)': float,
    'Rel Hum Flag': str,
    'Precip. Amount (mm)': float,
    'Precip. Amount Flag': str,
    'Wind Dir (10s deg)': float,
    'Wind Dir Flag': str,
    'Wind Spd (km/h)': float,
    'Wind Spd Flag': str,
    'Visibility (km)': float,
    'Visibility Flag': str,
    'Stn Press (kPa)': float,
    'Stn Press Flag': str,
    'Hmdx': str,
    'Hmdx Flag': str,
    'Wind Chill': str,
    'Wind Chill Flag': str,
    'Weather': str
}

# https://drive.google.com/drive/folders/1WJCDEU34c60IfOnG4rv5EPZ4IhhW9vZH
STATION_INVENTORY = pd.read_csv(
    StringIO(requests.get(
        'https://drive.google.com/u/0/uc?id=1egfzGgzUb0RFu_EE5AYFZtsyXPfZ11y2&export=download'
    ).text),
    skiprows=2,
    dtype={
        'Latitude (Decimal Degrees)': float,
        'Longitude (Decimal Degrees)': float,
        'HLY First Year': float,
        'HLY Last Year': float,
    }
)


def get_closest_valid_station_id(lat: float, lon: float, dt: date) -> str:
    station_inventory = STATION_INVENTORY.copy()
    station_inventory = station_inventory.loc[
        (station_inventory['HLY First Year'] <= dt.year)
        & (dt.year <= station_inventory['HLY Last Year'])
    ]
    latcol, loncol = 'Latitude (Decimal Degrees)', 'Longitude (Decimal Degrees)'
    station_inventory['distance'] = station_inventory.apply(
        lambda row: float(np.linalg.norm(
            np.array([row[latcol], row[loncol]]) - np.array([lat, lon])
        )),
        axis=1
    )
    return station_inventory.sort_values('distance').iloc[0]['Station ID']


def format_df(request_text: str, default_tzstr='US/Eastern') -> pd.DataFrame:
    df = pd.read_csv(StringIO(request_text), dtype=HOURLY_DF_DTYPES)

    def format_datetime(dtstr: str) -> datetime:
        try:
            dt = datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S%z')
        except ValueError:
            dt = datetime.strptime(dtstr, '%Y-%m-%d %H:%M')
            dt = timezone(default_tzstr).localize(dt)
        return dt.astimezone(timezone(default_tzstr))

    df['dt'] = df['Date/Time (LST)'].apply(format_datetime)
    return df


class ClimateWeatherGC(BaseWeather):
    """
    climate.weather.gc.ca
    """

    def get_historical_single_date(self, dt: date) -> pd.DataFrame:
        station_id = get_closest_valid_station_id(self.lat, self.lon, dt)
        if dt >= date.today():
            raise ValueError(f'No data available for {dt} >= {date.today()}')
        df = format_df(
            requests.get(
                'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&'
                f'stationID={station_id}&Year={dt.year}&Month={dt.month}&Day={dt.day}'
                '&timeframe=1&submit=Download+Data'
            ).text,
            default_tzstr=self.tz
        )
        return df
