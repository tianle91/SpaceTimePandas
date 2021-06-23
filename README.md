# SpaceTimePandas
Location and date features from a bunch of api sources to Pandas.
Repository hosted on [GitHub](https://github.com/tianle91/SpaceTimePandas).

![icon](SpaceTimePandas.png)
```
pip install SpaceTimePandas
```

# Demo 
```python
>>> from stpd.openstreetmap import OpenStreetMap
>>> osm=OpenStreetMap()
>>> osm('Toronto Ontario')
[nominatim] downloading data: search
{'count_natural=tree': 719, 'count_natural=water': 15, 'count_building=yes': 1151, 'count_building=house': 39, 'count_amenity=parking': 148, 'count_amenity=restaurant': 327, 'count_service=driveway': 77}
```

```python
>>> from stpd.openrouteservice._openrouteservice import OpenRouteServicePathFeatures
>>> ors = OpenRouteServicePathFeatures(api_key='<GET-ONE-FROM-OPENROUTESERVICE>')
>>> ors(location_strs=['toronto ontario', 'hamilton ontario'])
{'distance': 67828.8, 'duration': 3125.3}
```

```python
>>> from stpd.openrouteservice import OpenRouteServiceLocationFeatures
>>> ors = OpenRouteServiceLocationFeatures(api_key='<GET-ONE-FROM-OPENROUTESERVICE>')
>>> ors(location_str='toronto ontario')
{'range_seconds_100.0_area': 553988.44, 'range_seconds_100.0_reachfactor': 0.0229, 'range_seconds_100.0_total_pop': 1953.0, 'range_seconds_200.0_area': 3674992.8, 'range_seconds_200.0_reachfactor': 0.0379, 'range_seconds_200.0_total_pop': 47290.0, 'range_seconds_500.0_area': 29204165.23, 'range_seconds_500.0_reachfactor': 0.0482, 'range_seconds_500.0_total_pop': 289365.0, 'range_seconds_1000.0_area': 137873463.18, 'range_seconds_1000.0_reachfactor': 0.0569, 'range_seconds_1000.0_total_pop': 942521.0}
```
