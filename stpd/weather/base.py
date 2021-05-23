from datetime import date, datetime, timedelta
from typing import Union

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from timezonefinder import TimezoneFinder

TZFINDER = TimezoneFinder()


def filter_single_date(df: pd.DataFrame, dt: Union[date, datetime]) -> pd.DataFrame:
    date_format = '%Y-%m-%d'
    df = df.loc[df['dt'].apply(lambda dt: dt.strftime(date_format)) == dt.strftime(date_format)]
    df = df.reset_index(drop=True)
    return df


class BaseWeather:

    def __init__(self, lat, lon, **kwargs):
        self.lat = lat
        self.lon = lon
        self.tz = TZFINDER.timezone_at(lng=lon, lat=lat)
        self.kwargs = kwargs

    def get_features(self, dt: date) -> pd.DataFrame:
        raise NotImplementedError

    def validate_get_features(self, df: pd.DataFrame):
        if not is_datetime64_any_dtype(df.dtypes['dt']):
            raise TypeError(f'dt column: {df.dtypes["dt"]}, is not datetime64')

    def get_historical(
        self, start_date: date, end_date: date, partial_ok: bool = False
    ) -> pd.DataFrame:
        res_l = []
        for n in range((end_date - start_date).days + 1):
            dt = start_date + timedelta(days=n)
            df = self.get_features(dt)
            df = filter_single_date(df, dt=dt)
            self.validate_get_features(df)
            if len(df) == 0 and not partial_ok:
                raise ValueError(f'{dt} has no data {df}')
            res_l.append(df)
        return (
            pd.concat(res_l, axis=0)
            .drop_duplicates()
            .sort_values('dt')
            .reset_index(drop=True)
        )
