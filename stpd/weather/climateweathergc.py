from datetime import date, datetime
from io import StringIO

import pandas as pd
import requests
import requests_cache
from geopy import distance
from pytz import timezone
from timezonefinder import TimezoneFinder

from stpd.constants import TARGET_DATE_COL, TARGET_LAT_COL, TARGET_LON_COL

from .base import BaseWeather

session = requests_cache.CachedSession(namespace='climateweathergc')
TZFINDER = TimezoneFinder()
DAILY_DF_DTYPES = {
    "Longitude (x)": float,
    "Latitude (y)": float,
    "Station Name": str,
    "Climate ID": str,
    "Date/Time": str,
    "Year": int,
    "Month": int,
    "Day": int,
    "Data Quality": float,
    "Max Temp (°C)": float,
    "Max Temp Flag": str,
    "Min Temp (°C)": float,
    "Min Temp Flag": str,
    "Mean Temp (°C)": float,
    "Mean Temp Flag": str,
    "Heat Deg Days (°C)": float,
    "Heat Deg Days Flag": str,
    "Cool Deg Days (°C)": float,
    "Cool Deg Days Flag": str,
    "Total Rain (mm)": float,
    "Total Rain Flag": str,
    "Total Snow (cm)": float,
    "Total Snow Flag": str,
    "Total Precip (mm)": float,
    "Total Precip Flag": str,
    "Snow on Grnd (cm)": float,
    "Snow on Grnd Flag": str,
    "Dir of Max Gust (10s deg)": float,
    "Dir of Max Gust Flag": str,
    "Spd of Max Gust (km/h)": str,
    "Spd of Max Gust Flag": str,
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
        lambda row: distance.distance(
            (row[latcol], row[loncol]),
            (lat, lon)
        ).km,
        axis=1
    )
    return station_inventory.sort_values('distance').iloc[0]['Station ID']


def format_df(request_text: str, default_tzstr='US/Eastern') -> pd.DataFrame:
    df = pd.read_csv(StringIO(request_text), dtype=DAILY_DF_DTYPES)

    def format_datetime(dtstr: str) -> datetime:
        dt = datetime.strptime(dtstr, '%Y-%m-%d')
        return dt.astimezone(timezone(default_tzstr))

    df[TARGET_DATE_COL] = df['Date/Time'].apply(format_datetime)
    return df


class ClimateWeatherGC(BaseWeather):
    """
    climate.weather.gc.ca
    """

    def get_features(self, dt: date, lat: float, lon: float) -> pd.DataFrame:
        station_id = get_closest_valid_station_id(lat=lat, lon=lon, dt=dt)
        if dt >= date.today():
            raise ValueError(f'No data available for {dt} >= {date.today()}')
        # format request
        url = (
            'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&'
            f'stationID={station_id}&Year={dt.year}&Month={dt.month}&Day={dt.day}'
            '&timeframe=2&submit=Download+Data'
        )
        response_text = session.get(url).text
        try:
            df = format_df(response_text, default_tzstr=TZFINDER.timezone_at(lng=lon, lat=lat))
            df[TARGET_LAT_COL] = lat
            df[TARGET_LON_COL] = lon
            return df
        except Exception:
            raise ValueError(f'url:\n{url}\nresponse_text:\n{response_text}')
