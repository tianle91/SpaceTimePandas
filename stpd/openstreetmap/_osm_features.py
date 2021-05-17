from typing import Dict, List, Tuple, Union

# https://taginfo.openstreetmap.org/
FEATURES: Dict[str, Tuple[Union[str, List[str]], str]] = {
    # feature_name: (elementType, selector)
    'tree': ('node', '"natural"="tree"'),
    'building': (['way', 'relation'], '"building"="yes"'),
}
