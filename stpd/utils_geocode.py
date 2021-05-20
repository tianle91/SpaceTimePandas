from typing import Tuple

import pandas as pd
from OSMPythonTools.nominatim import Nominatim

nominatim = Nominatim()


def get_lat_lon(s: str, nom: Nominatim = nominatim) -> Tuple[float, float]:
    best_match = nom.query(s).toJSON()[0]
    return float(best_match['lat']), float(best_match['lon'])


def add_lat_lon_to_df(
    df: pd.DataFrame, location_name_column='location_name'
) -> pd.DataFrame:
    geocoded_mapping = {
        n: get_lat_lon(n)
        for n in df[location_name_column].unique()
    }
    geocoded_df = pd.DataFrame([
        {
            location_name_column: k,
            'latitude': v[0],
            'longitude': v[1],
        }
        for k, v in geocoded_mapping.items()
    ])
    return df.merge(
        geocoded_df, how='left', on=location_name_column)
