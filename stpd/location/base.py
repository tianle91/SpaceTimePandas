import pandas as pd


class BaseLocation:
    def get_features(self, lat, lon, **kwargs):
        raise NotImplementedError

    def add_features_to_df(
        self, df: pd.DataFrame, lat_col: str, lon_col: str, **kwargs
    ) -> pd.DataFrame:
        res_l = []
        for _, row in df[[lat_col, lon_col]].drop_duplicates().iterrows():
            res_l.append(self.get_features(
                lat=row[lat_col], lon=row[lon_col], **kwargs))
        return pd.concat(res_l, axis=0).reset_index(drop=True)
