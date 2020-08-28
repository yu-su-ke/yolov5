from enum import Enum


class LabelList(Enum):
    ALL = [['plane', 'sleeve', 'wall', 'roof', 'banner', 'standing', 'signage', 'vehicle',
            'subway', 'pillar'], 'all']
    MAIN = [['plane', 'sleeve', 'wall', 'roof', 'banner', 'signage'], 'main']
    ONE = [['billboard'], 'one']
