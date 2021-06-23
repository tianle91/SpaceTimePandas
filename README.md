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
