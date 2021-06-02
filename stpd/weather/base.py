from datetime import date, datetime
from typing import Union

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from timezonefinder import TimezoneFinder

from stpd.constants import TARGET_DATE_COL, TARGET_LAT_COL, TARGET_LON_COL

TZFINDER = TimezoneFinder()


def filter_single_date(df: pd.DataFrame, dt: Union[date, datetime]) -> pd.DataFrame:
    date_format = '%Y-%m-%d'
    df = df.loc[df['dt'].apply(lambda dt: dt.strftime(date_format)) == dt.strftime(date_format)]
    df = df.reset_index(drop=True)
    return df


def to_date(dt: Union[date, datetime]) -> date:
    return date(dt.year, dt.month, dt.day)


class BaseWeather:
    def __init__(self, date_col: str, lat_col: str, lon_col: str) -> None:
        self.date_col = date_col
        self.lat_col = lat_col
        self.lon_col = lon_col

    def get_features(self, dt: date, lat: float, lon: float) -> pd.DataFrame:
        raise NotImplementedError

    def validate_get_features(self, single_feature_df: pd.DataFrame):
        for c in [TARGET_LAT_COL, TARGET_LON_COL]:
            if c not in single_feature_df.columns:
                raise KeyError(f'{c} not in single_feature_df.columns')
        for c in [self.date_col, self.lat_col, self.lon_col]:
            if c in single_feature_df.columns:
                raise KeyError(f'{c} should not be in single_feature_df.columns')
        if not is_datetime64_any_dtype(single_feature_df.dtypes[TARGET_DATE_COL]):
            raise TypeError(
                f'TARGET_DATE_COL: {TARGET_DATE_COL} in single_feature_df'
                f' has incorrect type: {single_feature_df.dtypes[TARGET_DATE_COL]}'
                'which is not datetime64'
            )

    def add_features_to_df(self, df: pd.DataFrame) -> pd.DataFrame:
        date_col = self.date_col
        lat_col = self.lat_col
        lon_col = self.lon_col
        if not all([isinstance(v, date) for v in df[date_col].unique()]):
            raise ValueError('Only dates supported')
        df = df.copy()
        res_l = []
        for _, row in df[[lat_col, lon_col, date_col]].drop_duplicates().iterrows():
            single_date_feature = self.get_features(
                dt=row[date_col], lat=row[lat_col], lon=row[lon_col])
            self.validate_get_features(single_date_feature)
            res_l.append(single_date_feature)
        res_df = pd.concat(res_l, axis=0).reset_index(drop=True)
        # res_df needs to have single row per unique date
        res_df[TARGET_DATE_COL] = res_df[TARGET_DATE_COL].apply(to_date)
        join_cols = [TARGET_LAT_COL, TARGET_LON_COL, TARGET_DATE_COL]
        res_df = res_df.groupby(join_cols).agg({
            c: 'mean' if is_numeric_dtype(res_df.dtypes[c]) else 'first'
            for c in res_df.columns if c not in join_cols
        }).reset_index()
        # for joining purposes
        df[TARGET_DATE_COL] = df[date_col]
        df[TARGET_LAT_COL] = df[lat_col]
        df[TARGET_LON_COL] = df[lon_col]
        return (
            df
            .merge(res_df, on=join_cols, how='left')
            .drop(columns=join_cols)
        )
