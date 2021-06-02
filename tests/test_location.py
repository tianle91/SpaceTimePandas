import numpy as np
import pytest

from stpd.location import OpenStreetMap, OSMFeatures, SimpleMaps

# Toronto
LAT = 43.6534817
LON = -79.3839347


def test_simplemaps():
    sm = SimpleMaps(lat_col='lat', lon_col='lon')
    sm.get_features(LAT, LON)


@pytest.mark.parametrize(
    'feature_names',
    [
        pytest.param(None, id='default')
    ] + [
        pytest.param([n], id=n)
        for n in np.random.choice(list(OSMFeatures.keys()), size=5, replace=False)
    ]
)
def test_openstreemap(feature_names):
    osm = OpenStreetMap(
        lat_col='lat',
        lon_col='lon',
        feature_names=feature_names
    )
    osm.get_features(LAT, LON)


def test_openstreetmap_feature_query_values():
    osm = OpenStreetMap(
        lat_col='lat',
        lon_col='lon',
        feature_query_values={'natural=tree': ('node', '"natural"="tree"')}
    )
    osm.get_features(LAT, LON)
