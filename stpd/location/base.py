import pandas as pd

from stpd.constants import TARGET_LAT_COL, TARGET_LON_COL


class BaseLocation:
    def __init__(self, lat_col: str, lon_col: str) -> None:
        self.lat_col = lat_col
        self.lon_col = lon_col

    def get_features(self, lat, lon):
        raise NotImplementedError

    def validate_get_features(self, single_feature_df: pd.DataFrame):
        for c in [TARGET_LAT_COL, TARGET_LON_COL]:
            if c not in single_feature_df.columns:
                raise KeyError(f'{c} not in single_feature_df.columns')
        for c in [self.lat_col, self.lon_col]:
            if c in single_feature_df.columns:
                raise KeyError(f'{c} should not in single_feature_df.columns')

    def add_features_to_df(self, df: pd.DataFrame) -> pd.DataFrame:
        lat_col = self.lat_col
        lon_col = self.lon_col
        df = df.copy()
        res_l = []
        for _, row in df[[lat_col, lon_col]].drop_duplicates().iterrows():
            single_location_feature = self.get_features(lat=row[lat_col], lon=row[lon_col])
            self.validate_get_features(single_location_feature)
            res_l.append(single_location_feature)
        res_df = pd.concat(res_l, axis=0).reset_index(drop=True)
        df[TARGET_LAT_COL] = df[lat_col]
        df[TARGET_LON_COL] = df[lon_col]
        join_cols = [TARGET_LAT_COL, TARGET_LON_COL]
        return (
            df
            .merge(res_df, on=join_cols, how='left')
            .drop(columns=join_cols)
        )
