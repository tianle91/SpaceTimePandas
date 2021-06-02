from typing import Tuple

import pandas as pd
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()


def get_lat_lon(s: str, nom: Nominatim = nominatim) -> Tuple[float, float]:
    best_match = nom.query(s).toJSON()[0]
    return float(best_match['lat']), float(best_match['lon'])


class GeoCode:
    def __init__(self, location_name_col: str, lat_col: str = 'lat', lon_col: str = 'lon') -> None:
        self.location_name_col = location_name_col
        self.lat_col = lat_col
        self.lon_col = lon_col

    def add_features_to_df(self, df: pd.DataFrame) -> pd.DataFrame:
        geocoded_mapping = {
            n: get_lat_lon(n)
            for n in df[self.location_name_col].unique()
        }
        geocoded_df = pd.DataFrame([
            {
                self.location_name_col: k,
                self.lat_col: v[0],
                self.lon_col: v[1],
            }
            for k, v in geocoded_mapping.items()
        ])
        return df.merge(geocoded_df, how='left', on=self.location_name_col)
