from datetime import date, datetime, timedelta
from typing import Union

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from timezonefinder import TimezoneFinder

TZFINDER = TimezoneFinder()


def filter_single_date(df: pd.DataFrame, dt: Union[date, datetime]) -> pd.DataFrame:
    date_format = '%Y-%m-%d'
    df = df.loc[df['dt'].apply(lambda dt: dt.strftime(date_format)) == dt.strftime(date_format)]
    df = df.reset_index(drop=True)
    return df


def to_date(dt: Union[date, datetime]) -> date:
    return date(dt.year, dt.month, dt.day)


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

    def add_features_to_df(
        self, df: pd.DataFrame, date_col: str
    ) -> pd.DataFrame:
        df = df.copy()
        if not all([isinstance(v, date) for v in df[date_col].unique()]):
            raise ValueError('Only dates supported')
        res_l = []
        for dt in df[date_col].unique():
            single_date_feature = self.get_features(dt)
            self.validate_get_features(single_date_feature)
            res_l.append(single_date_feature)
        res_df = pd.concat(res_l, axis=0).reset_index(drop=True)
        # res_df needs to have single row per unique date
        res_df['dt'] = res_df['dt'].apply(to_date)
        res_df = res_df.groupby('dt').agg({
            c: 'mean' if is_numeric_dtype(res_df.dtypes[c]) else 'first'
            for c in res_df.columns
        }).reset_index(drop=True)
        # for joining purposes
        df['dt'] = df[date_col]
        return (
            df
            .merge(res_df, on=['dt'], how='left')
            .drop(columns=['dt'])
        )

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
