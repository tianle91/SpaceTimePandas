# SpaceTimePandas
Location and date features from a bunch of api sources to Pandas.
Repository hosted on [GitHub](https://github.com/tianle91/SpaceTimePandas).

![icon](SpaceTimePandas.png)
```
pip install SpaceTimePandas
```

# Demo 
Get a lot of space and time related features!
See also 
[demo_pipeline.ipynb](demo_pipeline.ipynb)
or on colab 
[[SpaceTimePandas] demo_pipeline.ipynb](https://colab.research.google.com/drive/1RdWAMbX8I5VjI7g43JLOwIh94LWEe9sK?usp=sharing)
```python
>>> df
         location_name        date
0      Toronto, Canada  2020-01-01
1      Toronto, Canada  2020-01-02
2  Halifax, NS B3J 1M3  2020-01-01
3  Halifax, NS B3J 1M3  2020-01-02
```
Define a collection of features.
```python
>>> from stpd.location import OpenStreetMap, SimpleMaps
>>> from stpd.pipeline import Pipeline
>>> from stpd.utils_geocode import GeoCode
>>> from stpd.weather import NOAA, ClimateWeatherGC
>>> p = Pipeline([
>>>     GeoCode(location_name_col='location_name', lat_col='lat', lon_col='lon'),
>>>     OpenStreetMap(lat_col='lat', lon_col='lon'),
>>>     SimpleMaps(lat_col='lat', lon_col='lon'),
>>>     NOAA(date_col='date', lat_col='lat', lon_col='lon'),
>>>     ClimateWeatherGC(date_col='date', lat_col='lat', lon_col='lon'),
>>> ])
>>> features = p.add_features_to_df(df)
>>> features.shape
(4, 60)
```
Preview of a single row (some columns truncated).
```python
>>> features.iloc[0]
location_name                Toronto, Canada
date                              2020-01-01
lat                                43.653482
lon                               -79.383935
count_natural=tree                       719
count_natural=water                       15
...
iso2                                      CA
iso3                                     CAN
admin_name                           Ontario
capital                                  NaN
population                         5429524.0
...
STATION                          USC00309690
TMAX                                    83.0
TMIN                                    -6.0
...
Heat Deg Days (°C)                      14.4
Heat Deg Days Flag                      None
...
Total Snow (cm)                          NaN
Total Snow Flag                         None
...
Dir of Max Gust (10s deg)                NaN
Dir of Max Gust Flag                       M
...
Name: 0, dtype: object
```

You can of course use the components above individually.
- Weather features [demo_weather.ipynb](demo_weather.ipynb).
- Location features [demo_location.ipynb](demo_location.ipynb).
