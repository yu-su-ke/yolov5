from enum import Enum


class LabelList(Enum):
    ALL = [['plane', 'sleeve', 'wall', 'roof', 'banner', 'standing', 'signage', 'vehicle',
            'subway', 'pillar'], 'all']
    MAIN = [['plane', 'sleeve', 'wall', 'roof', 'banner', 'signage'], 'main']
    ONE = [['billboard'], 'one']

    Media = [['plane', 'sleeve', 'wall', 'roof', 'banner', 'standing', 'signage', 'vehicle',
              'subway', 'pillar'], 'all']

    Place = [['indoor', 'outdoor', 'subway'], 'place']

    Genre = [
        ['alcohol', 'art', 'car', 'cosmetics', 'distribution', 'education_medical_religion', 'energy_material_machine',
         'event', 'fashion', 'finance', 'food', 'gambling', 'game', 'government', 'hobbies_sports', 'home_appliances',
         'household_goods', 'information', 'medicine', 'movies', 'precision_equipment', 'publication', 'real_estate',
         'restaurant', 'soft_drink', 'sound', 'telecommunications', 'tobacco_luxury', 'transportation_leisure_travel',
         'tv'], 'genre']

    Adv = [['大正製薬株式会社'], 'advertiser']
