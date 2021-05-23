import pandas as pd


class BaseLocation:
    def get_features(self, lat, lon, **kwargs):
        raise NotImplementedError

    def validate_get_features(self, df: pd.DataFrame):
        for c in ['target_lat', 'target_lon']:
            if c not in df.columns:
                raise KeyError(f'{c} not in df.columns')

    def add_features_to_df(
        self, df: pd.DataFrame, lat_col: str, lon_col: str
    ) -> pd.DataFrame:
        res_l = []
        for _, row in df[[lat_col, lon_col]].drop_duplicates().iterrows():
            single_location_feature = self.get_features(lat=row[lat_col], lon=row[lon_col])
            self.validate_get_features(single_location_feature)
            res_l.append(single_location_feature)
        res_df = pd.concat(res_l, axis=0).reset_index(drop=True)
        df['target_lat'] = df[lat_col]
        df['target_lon'] = df[lon_col]
        return (
            df
            .merge(res_df, on=['target_lat', 'target_lon'], how='left')
            .drop(columns=['target_lat', 'target_lon'])
        )
