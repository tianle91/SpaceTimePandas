from typing import List, Union

import pandas as pd

from stpd.location.base import BaseLocation
from stpd.weather.base import BaseWeather


class Pipeline:
    def __init__(self, stages: List[Union[BaseLocation, BaseWeather]]):
        for v in stages:
            if not isinstance(v, BaseLocation) and not isinstance(v, BaseWeather):
                raise ValueError(f'{v} has to be an instance of BaseLocation or BaseWeather')
        self.stages = stages

    def add_features_to_df(
        self, df: pd.DataFrame, date_col: str, lat_col: str, lon_col: str
    ) -> pd.DataFrame:
        index_cols = [date_col, lat_col, lon_col]
        res_l = [df[[c for c in index_cols if c in df.columns]]]
        for stage in self.stages:
            if isinstance(stage, BaseLocation):
                df_ft = stage.add_features_to_df(
                    df, lat_col=lat_col, lon_col=lon_col)
            elif isinstance(stage, BaseWeather):
                df_ft = stage.add_features_to_df(
                    df, date_col=date_col, lat_col=lat_col, lon_col=lon_col)
            df_ft = df_ft.rename(columns={
                c: f'{stage.__class__.__name__}_{c}'
                for c in df_ft if c not in df
            })
            res_l.append(df_ft.drop(columns=[
                c for c in index_cols if c in df_ft.columns
            ]))
        return pd.concat(res_l, axis=1)
