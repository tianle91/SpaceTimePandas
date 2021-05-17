from typing import Dict, List, Tuple, Union

FEATURES: Dict[str, Tuple[Union[str, List[str]], str]] = {
    # https://taginfo.openstreetmap.org/
    # TODO: predefined or user defined features for passing into overpassQueryBuilder
    # feature_name: (elementType, selector)
    'tree': ('node', '"natural"="tree"'),
    'building': (['way', 'relation'], '"building"="yes"'),
}
