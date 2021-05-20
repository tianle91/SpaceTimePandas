from typing import Dict, List, Tuple, Union

DEFAULT_FEATURE_NAMES = [
    'natural=tree',
    'natural=water',
    'building=yes',
    'building=house',
    'amenity=parking',
    'amenity=restaurant',
    'service=driveway',
]

FEATURES: Dict[str, Tuple[Union[str, List[str]], str]] = {
    # https://taginfo.openstreetmap.org/
    # feature_name: (elementType, selector)

    # natural:
    'natural=tree': ('node', '"natural"="tree"'),
    'natural=water': (['way', 'relation'], '"natural"="water"'),
    'natural=wood': ('relation', '"natural"="wood"'),
    'natural=scrub': ('relation', '"natural"="scrub"'),
    'natural=wetland': ('relation', '"natural"="wetland"'),

    # building:
    'building=yes': (['way', 'relation'], '"building"="yes"'),
    'building=house': ('way', '"building"="house"'),
    'building=residential': ('way', '"building"="residential"'),

    # amenity:
    'amenity=parking': (['way', 'relation'], '"amenity"="parking"'),
    'amenity=bench': ('node', '"amenity"="bench"'),
    'amenity=place_of_worship': ('node', '"amenity"="place_of_worship"'),
    'amenity=restaurant': ('node', '"amenity"="restaurant"'),
    'amenity=school': (['node', 'relation'], '"amenity"="school"'),

    # highway:
    'highway=residential': ('way', '"highway"="residential"'),
    'highway=service': ('way', '"highway"="service"'),
    'highway=track': ('way', '"highway"="track"'),
    'highway=unclassified': ('way', '"highway"="unclassified"'),
    'highway=footway': ('way', '"highway"="footway"'),
    'highway=path': ('way', '"highway"="path"'),
    'highway=tertiary': ('way', '"highway"="tertiary"'),
    'highway=crossing': ('node', '"highway"="crossing"'),
    'highway=secondary': ('way', '"highway"="secondary"'),
    'highway=primary': ('way', '"highway"="primary"'),

    # power:
    'power=tower': ('node', '"power"="tower"'),
    'power=pole': ('node', '"power"="pole"'),
    'power=generator': ('node', '"power"="generator"'),
    'power=line': ('way', '"power"="line"'),
    'power=minor_line': ('way', '"power"="minor_line"'),
    'power=substation': (['node', 'way', 'relation'], '"power"="substation"'),
    'power=portal': ('node', '"power"="portal"'),
    'power=transformer': ('node', '"power"="transformer"'),
    'power=switch': ('node', '"power"="switch"'),
    'power=catenary_mast': ('node', '"power"="catenary_mast"'),

    # service:
    'service=driveway': ('way', '"service"="driveway"'),
    'service=parking_aisle': ('way', '"service"="parking_aisle"'),
    'service=alley': ('way', '"service"="alley"'),
    'service=yard': ('way', '"service"="yard"'),
    'service=spur': ('way', '"service"="spur"'),
    'service=siding': ('way', '"service"="siding"'),
    'service=drive-through': ('way', '"service"="drive-through"'),
    'service=crossover': ('way', '"service"="crossover"'),

    # surface:
    'surface=asphalt': ('way', '"surface"="asphalt"'),
    'surface=unpaved': ('way', '"surface"="unpaved"'),
    'surface=paved': ('way', '"surface"="paved"'),
    'surface=ground': ('way', '"surface"="ground"'),
    'surface=concrete': ('way', '"surface"="concrete"'),
    'surface=gravel': ('way', '"surface"="gravel"'),
    'surface=paving_stones': ('way', '"surface"="paving_stones"'),
    'surface=dirt': ('way', '"surface"="dirt"'),
    'surface=grass': ('way', '"surface"="grass"'),
    'surface=compacted': ('way', '"surface"="compacted"'),
}
