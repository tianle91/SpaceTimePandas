from typing import List, Union

import pandas as pd

from stpd.location.base import BaseLocation
from stpd.utils_geocode import GeoCode
from stpd.weather.base import BaseWeather


class Pipeline:
    def __init__(self, stages: List[Union[BaseLocation, BaseWeather, GeoCode]]):
        for v in stages:
            if not any([isinstance(v, c) for c in [BaseLocation, BaseWeather, GeoCode]]):
                raise ValueError(f'{v} has to be an instance of BaseLocation, BaseWeather, GeoCode')
        self.stages = stages

    def add_features_to_df(self, df: pd.DataFrame) -> pd.DataFrame:
        merged_df = df.copy()
        for stage in self.stages:
            merged_df = stage.add_features_to_df(merged_df)
        return merged_df
