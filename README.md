# SpaceTimePandas
![icon](SpaceTimePandas.png)

Location and date features from a bunch of api sources to Pandas.
Repository hosted on [GitHub](https://github.com/tianle91/SpaceTimePandas).

```
pip install SpaceTimePandas
```

# Demo

## Climate
See also [demo_climate.ipynb](demo_climate.ipynb).
```python
>>> df
         date
0  2020-01-01
1  2020-01-02
```

`NOAA` provides climate data from a huge variety of weather stations.
See [ghcnd-inventory.txt](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt).
```python
>>> from stpd.weather import NOAA
>>> noaa = NOAA(lat, lon)
>>> noaa.add_features_to_df(df, date_col='date')
         date      STATION  TMAX  TMIN   TOBS
0  2020-01-01  USC00309690  83.0  -6.0     -6
1  2020-01-02  USC00309690  44.0 -11.0     44
```

`climate.weather.gc.ca` collects data from Canadian weather stations.
It has more complete weather information compared to `NOAA`.
```python
>>> from stpd.weather import ClimateWeatherGC
>>> cwgc = ClimateWeatherGC(lat, lon)
>>> cwgc.add_features_to_df(df, date_col='date')
         date  Longitude (x)  Latitude (y)  Station Name Climate ID  \
0  2020-01-01          -79.4         43.67  TORONTO CITY    6158355   
1  2020-01-02          -79.4         43.67  TORONTO CITY    6158355   

    Date/Time  Year  Month  Day  Data Quality  ...  Total Snow (cm)  \
0  2020-01-02  2020      1    2           NaN  ...              NaN   
1  2020-01-03  2020      1    3           NaN  ...              NaN   

  Total Snow Flag  Total Precip (mm) Total Precip Flag  Snow on Grnd (cm)  \
0            None                0.0              None                1.0   
1            None                0.0              None                1.0   

  Snow on Grnd Flag  Dir of Max Gust (10s deg) Dir of Max Gust Flag  \
0              None                        NaN                    M   
1              None                        NaN                    M   

   Spd of Max Gust (km/h) Spd of Max Gust Flag  
0                    None                    M  
1                    None                    M  
```

## Location
See also [demo_location.ipynb](demo_location.ipynb).
```python
>>> df
               location_name   latitude   longitude
0  221B Baker Street, London  51.523388   -0.158237
1            Shanghai, China  31.232276  121.469207
2        Halifax, NS B3J 1M3  44.648618  -63.585949
```

`OpenStreetMap` returns count of map features in a radius around a location.
```python
>>> from stpd.location import OpenStreetMap
>>> osm = OpenStreetMap()
>>> osm.add_features_to_df(df=df, lat_col='latitude', lon_col='longitude')
               location_name   latitude   longitude  count_natural=tree  \
0  221B Baker Street, London  51.523388   -0.158237                 783   
1            Shanghai, China  31.232276  121.469207                 114   
2        Halifax, NS B3J 1M3  44.648618  -63.585949                  48   

   count_natural=water  count_building=yes  count_building=house  \
0                   10                1459                   503   
1                    6                1586                     0   
2                    2                3115                    11   

   count_amenity=parking  count_amenity=restaurant  count_service=driveway  
0                     44                       135                      67  
1                      8                       109                       9  
2                     72                        90                      74  
```
You can also specify your own desired features
```python
>>> osm = OpenStreetMap(feature_names=['natural=tree'])
>>> # equivalently:
>>> # osm = OpenStreetMap(feature_query_values={'natural=tree': ('node', '"natural"="tree"')})
>>> osm.add_features_to_df(df=df, lat_col='latitude', lon_col='longitude')
               location_name   latitude   longitude  count_natural=tree
0  221B Baker Street, London  51.523388   -0.158237                 783
1            Shanghai, China  31.232276  121.469207                 114
2        Halifax, NS B3J 1M3  44.648618  -63.585949                  48
```

`SimpleMaps` provide basic city features
```python
>>> from stpd.location import SimpleMaps
>>> sm = SimpleMaps()
>>> sm.add_features_to_df(df=df, lat_col='latitude', lon_col='longitude')
               location_name   latitude   longitude     city city_ascii  \
0  221B Baker Street, London  51.523388   -0.158237   London     London   
1            Shanghai, China  31.232276  121.469207   Pudong     Pudong   
2        Halifax, NS B3J 1M3  44.648618  -63.585949  Halifax    Halifax   

       lat       lng         country iso2 iso3       admin_name  capital  \
0  51.5072   -0.1275  United Kingdom   GB  GBR  London, City of  primary   
1  31.2231  121.5397           China   CN  CHN         Shanghai    minor   
2  44.6475  -63.5906          Canada   CA  CAN      Nova Scotia      NaN   

   population          id  distance  
0  10979000.0  1826645935  2.792172  
1   5187200.0  1156644508  6.792938  
2    403131.0  1124130981  0.389333  
```
