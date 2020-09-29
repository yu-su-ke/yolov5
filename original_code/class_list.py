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

    Adv = [['キリンビール株式会社', 'サントリービール株式会社', 'チョーヤ梅酒株式会社', 'ウォルト・ディズニー・ジャパン株式会社',
            '株式会社Cygames', 'ベトジェットエア', 'アウディジャパン株式会社', '株式会社マガジンハウス', '株式会社ブシロード',
            '森永製菓株式会社', '株式会社湖池屋', '日本テレビ放送網株式会社', 'LVMHファッション・グループ・ジャパン株式会社',
            '株式会社マイナビ', 'TBCグループ株式会社', '大塚製薬株式会社', 'レッドブル・ジャパン株式会社', 'モンスターエナジージャパン合同会社',
            '大塚食品株式会社', '日本コカ・コーラ株式会社', '花王株式会社', 'Apple Japan合同会社', '株式会社早稲田アカデミー', 'Mastercard',
            '株式会社NTTドコモ', 'KDDI株式会社', 'ソフトバンク株式会社', 'シチズン時計株式会社', 'LVMHウォッチ・ジュエリージャパン株式会社',
            '大正製薬株式会社', '株式会社龍角散'], 'advertiser']
