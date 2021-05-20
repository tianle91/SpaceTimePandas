# SpaceTimePandas
![icon](SpaceTimePandas.png)

Location and date features from a bunch of api sources to Pandas.
Repository hosted on [GitHub](https://github.com/tianle91/SpaceTimePandas).

```
pip install SpaceTimePandas
```

# Demo
See also the [notebook](demo.ipynb).
You'll need to get `lat, lon` from addresses or location names if you don't have it.
```python
>>> from stpd.utils_geocode import get_lat_lon
>>> from datetime import date
>>> lat, lon = get_lat_lon('Toronto, Canada')
>>> start_date, end_date = date(2000, 1, 1), date(2000, 1, 8)
```

## Historical weather features 

### NOAA
`NOAA` provides climate data from a huge variety of weather stations.
```python
>>> from stpd import NOAA
>>> noaa = NOAA(lat, lon)
>>> noaa.get_historical(start_date, end_date)
       STATION  SNOW   TMAX  TMIN  PRCP  SNWD                        dt
0  CA006158350   0.0   86.0   0.0   0.0   0.0 2000-01-01 00:00:00-05:00
1  CA006158350   0.0  129.0  35.0  18.0   0.0 2000-01-02 00:00:00-05:00
```

### Government of Canada
`climate.weather.gc.ca` collects data from Canadian weather stations.
```python
>>> from stpd import ClimateWeatherGC
>>> cwgc = ClimateWeatherGC(lat, lon)
>>> cwgc.get_historical(start_date, end_date).tail()
   Longitude (x)  Latitude (y)      Station Name Climate ID   Date/Time  Year  \
0          -79.4         43.63  TORONTO ISLAND A    6158665  2000-01-02  2000   
1          -79.4         43.63  TORONTO ISLAND A    6158665  2000-01-03  2000   

   Month  Day  Data Quality  Max Temp (°C)  ... Total Snow Flag  \
0      1    2           NaN           11.7  ...               M   
1      1    3           NaN           11.0  ...               M   

   Total Precip (mm) Total Precip Flag  Snow on Grnd (cm) Snow on Grnd Flag  \
0                1.5               NaN                NaN               NaN   
1                3.5               NaN                NaN               NaN   

   Dir of Max Gust (10s deg) Dir of Max Gust Flag  Spd of Max Gust (km/h)  \
0                       23.0                  NaN                      44   
1                        7.0                  NaN                      65   

  Spd of Max Gust Flag                        dt  
0                  NaN 2000-01-01 19:00:00-05:00  
1                  NaN 2000-01-02 19:00:00-05:00  
```

## Location features

### OpenStreetMap
`OpenStreetMap` can be used to count map features in a radius around a location.
You get a default set of features if no arguments are specified.
```python
>>> from stpd import OpenStreetMap
>>> osm = OpenStreetMap()
>>> osm.get_features(lat, lon)
   target_lat  target_lon  count_natural=tree  count_natural=water  \
0   43.653482  -79.383935                 719                   15   

   count_building=yes  count_building=house  count_amenity=parking  \
0                1151                    39                    148   

   count_amenity=restaurant  count_service=driveway  
0                       327                      77 
```

### SimpleMaps
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
