from io import StringIO, TextIOWrapper
from tempfile import TemporaryFile
from typing import Dict
from zipfile import ZipFile

import numpy as np
import pandas as pd
import requests


def extract_zip(input_zip: TextIOWrapper) -> Dict[str, str]:
    input_zip = ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


WORLDCITIES_DTYPES = {
    'city': str,
    'city_ascii': str,
    'lat': float,
    'lng': float,
    'country': str,
    'iso2': str,
    'iso3': str,
    'admin_name': str,
    'capital': str,
    'population': float,
    'id': str,
}

URL = 'https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.73.zip'

with TemporaryFile() as f:
    f.write(requests.get(URL).content)
    WORLDCITIES = pd.read_csv(
        StringIO(extract_zip(f)['worldcities.csv'].decode("utf-8")),
        dtype=WORLDCITIES_DTYPES
    )


def euclidean_distance(xy1, xy2):
    return float(np.linalg.norm(np.array(xy1) - np.array(xy2)))


class SimpleMaps:
    """
    https://simplemaps.com/data/world-cities
    """

    def get_features(self, lat, lon):
        all_df = pd.DataFrame({
            'target_lat': [lat],
            'target_lon': [lon],
        }, dtype=float).merge(WORLDCITIES, how='cross')
        all_df['distance'] = all_df.apply(
            lambda row: euclidean_distance(
                (row['lat'], row['lng']),
                (row['target_lat'], row['target_lon'])
            ),
            axis=1
        )
        out_rows = []
        for _, subdf in all_df.groupby(['target_lat', 'target_lon']):
            out_rows.append(subdf.loc[subdf['distance'].idxmin()])
        return pd.DataFrame(out_rows).reset_index(drop=True)
