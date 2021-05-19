# SpaceTimePandas
![icon](SpaceTimePandas.png)

Location and date features from a bunch of api sources to Pandas.

```
pip install SpaceTimePandas
```

# Demo
See also the [notebook](demo.ipynb).

You'll need to get `lat, lon` from addresses or location names if you don't have it.
```python
>>> from stpd.utils_geocode import get_lat_lon
>>> lat, lon = get_lat_lon('Toronto, Canada')
>>> lat, lon
(43.6534817, -79.3839347)
```

## Historical weather features 
Set up start and end dates for historical weather.
```python
>>> from datetime import date
>>> start_date = date(2021, 5, 7)
>>> end_date = date(2021, 5, 9)
```

`NOAA` provides a hugeclimate data from a huge variety of weather stations.
```python
>>> from stpd import NOAA
>>> noaa = NOAA(lat, lon)
>>> noaa.get_historical(start_date, end_date)
       STATION  SNOW   TMAX   TAVG  TMIN  PRCP  SNWD                        dt
0  CA00615S001   0.0  125.0     88  50.0   0.0   0.0 2021-05-07 00:00:00-04:00
1  CA00615S001   0.0  160.0     80   0.0   0.0   0.0 2021-05-08 00:00:00-04:00
2  CA00615S001   0.0  130.0     70  10.0   0.0   0.0 2021-05-09 00:00:00-04:00
```

`climate.weather.gc.ca` collects data from Canadian weather stations.
```python
>>> from stpd import ClimateWeatherGC
>>> cwgc = ClimateWeatherGC(lat, lon)
>>> cwgc.get_historical(start_date, end_date).tail()
    Longitude (x)  Latitude (y)  Station Name Climate ID   Date/Time (LST)  \
0           -79.4         43.67  TORONTO CITY    6158355  2021-05-07 00:00   
..            ...           ...           ...        ...               ...   

    Year  Month  Day Time (LST)  Temp (°C)  ... Visibility (km)  \
0   2021      5    7      00:00        9.3  ...             NaN   

    Visibility Flag Stn Press (kPa)  Stn Press Flag Hmdx  Hmdx Flag  \
0               NaN          100.22             NaN  NaN        NaN   

   Wind Chill  Wind Chill Flag Weather                        dt  
0         NaN              NaN     NaN 2021-05-07 00:00:00-04:00  
```

## Location features
`SimpleMaps` provide basic city features
```python
>>> from stpd import SimpleMaps
>>> sm = SimpleMaps()
>>> sm.get_features(lat, lon)
   target_lat  target_lon     city city_ascii      lat      lng country iso2  \
0   43.653482  -79.383935  Toronto    Toronto  43.7417 -79.3733  Canada   CA   

  iso3 admin_name  capital  population          id  distance  
0  CAN    Ontario      NaN   5429524.0  1124279679  0.088857  
```

### OpenStreetMap
`OpenStreetMap` can be used to count map features in a radius around a location.
Check [here](stpd/openstreetmap/_osm_features.py) for a complete set of pre-defined values for `feature_names`.
```python
>>> from stpd import OpenStreetMap
>>> osm = OpenStreetMap(feature_names=['natural=tree'])
>>> osm.get_features(lat, lon)
   target_lat  target_lon  count_natural=tree
0   43.653482  -79.383935                 719
```
Equivalently, you can use `feature_query_values` to query for your own tags of interest.
```python
>>> osm = OpenStreetMap(feature_query_values={'natural=tree': ('node', '"natural"="tree"')})
>>> osm.get_features(lat, lon)
   target_lat  target_lon  count_natural=tree
0   43.653482  -79.383935                 719
```
