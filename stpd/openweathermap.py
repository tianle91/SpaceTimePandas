from datetime import date, datetime

import pandas as pd
import requests
from pytz import timezone

from .base import BaseWeather

HOURLY_DF_DTYPES = {
    'temp': float,
    'feels_like': float,
    'pressure': float,
    'humidity': float,
    'dew_point': float,
    'uvi': float,
    'clouds': float,
    'visibility': float,
    'wind_speed': float,
    'wind_deg': float,
    'wind_gust': float,
    'weather': str,
    'rain': str,
}


def format_df(response_json_hourly, tzstr='US/Eastern') -> pd.DataFrame:
    df = pd.DataFrame(response_json_hourly)
    df = df.astype({c: v for c, v in HOURLY_DF_DTYPES.items() if c in df.columns})

    def format_as_datetime(utc_timestamp) -> datetime:
        dt = datetime.fromtimestamp(utc_timestamp)
        dt = timezone('UTC').localize(dt)
        dt = dt.astimezone(timezone(tzstr))
        return dt

    df['dt'] = df['dt'].apply(format_as_datetime)
    return df


def get_onecall_response(lat, lon, api_key):
    return requests.get(
        'https://api.openweathermap.org/data/2.5/onecall'
        f'?lat={lat}&lon={lon}&appid={api_key}'
        '&units=metric&exclude=current,minutely,daily'
    ).json()


def get_onecall_timemachine_response(lat, lon, dt, api_key):
    return requests.get(
        'https://api.openweathermap.org/data/2.5/onecall/timemachine'
        f'?lat={lat}&lon={lon}&dt={dt}&appid={api_key}'
        '&units=metric&exclude=current,minutely,hourly'
    ).json()


class OpenWeatherMap(BaseWeather):
    """
    openweathermap.org
    """
    @property
    def api_key(self) -> str:
        return self.kwargs.get('api_key')

    def get_hourly_forecast(self):
        response_json = get_onecall_response(
            lat=self.lat,
            lon=self.lon,
            api_key=self.api_key
        )
        return format_df(response_json['hourly'], tzstr=self.tz)

    def get_historical_single_date(self, dt: date) -> pd.DataFrame:
        dt = timezone(self.tz).localize(datetime.combine(dt, datetime.min.time()))
        response_json = get_onecall_timemachine_response(
            lat=self.lat,
            lon=self.lon,
            dt=int(dt.astimezone(timezone('UTC')).timestamp()),
            api_key=self.api_key
        )
        try:
            df = format_df(response_json['hourly'], tzstr=self.tz)
            return df
        except KeyError:
            raise ValueError(f'No hourly data for dt: {dt}. response_json: {response_json}')
