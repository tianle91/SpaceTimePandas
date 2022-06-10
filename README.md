# SpaceTimePandas
Location and date features from a bunch of api sources to Pandas.
Repository hosted on [GitHub](https://github.com/tianle91/SpaceTimePandas).

![icon](SpaceTimePandas.png)
```
pip install SpaceTimePandas
```


# Temporal features

```python
>>> import datetime
>>> from stpd.event import Holiday
>>> Holiday('US')(datetime.date(2022, 1, 17))
{
    'us_holiday_days_since_last': 0,
    'us_holiday_days_to_next': 35
}
```

```python
>>> from datetime import datetime
>>> from stpd.fourier import Fourier
>>> Fourier()(datetime(2020, 1, 1))
{
    'week_of_year_sine_phase_0': 0.1198805403706726,
    ...
    'week_of_year_sine_phase_52': 0.08569582503232778,
    'week_of_year_cos_phase_0': 0.9927883238840168,
    ...
    'minute_of_hour_cos_phase_59': 0.9945218953682733
}
```


# Location features
```python
>>> from stpd.openstreetmap import OpenStreetMap
>>> osm=OpenStreetMap()('Toronto Ontario')
[nominatim] downloading data: search
{
    'count_natural=tree': 719, 
    'count_natural=water': 15, 
    'count_building=yes': 1151, 
    'count_building=house': 39, 
    'count_amenity=parking': 148, 
    'count_amenity=restaurant': 327, 
    'count_service=driveway': 77
}
```

```python
>>> from stpd.openrouteservice import OpenRouteServicePathFeatures
>>> ors = OpenRouteServicePathFeatures(api_key='<GET-ONE-FROM-OPENROUTESERVICE>')
>>> ors(location_strs=['toronto ontario', 'hamilton ontario'])
{
    'distance': 67828.8,
    'duration': 3125.3
}
```

```python
>>> from stpd.openrouteservice import OpenRouteServiceLocationFeatures
>>> ors = OpenRouteServiceLocationFeatures(api_key='<GET-ONE-FROM-OPENROUTESERVICE>')
>>> ors(location_str='toronto ontario')
{
    'range_seconds_100.0_area': 553988.44, 
    'range_seconds_100.0_reachfactor': 0.0229, 
    'range_seconds_100.0_total_pop': 1953.0, 
    'range_seconds_200.0_area': 3674992.8, 
    ...
    'range_seconds_1000.0_total_pop': 942521.0
}
```
