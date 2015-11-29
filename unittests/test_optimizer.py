import json
import unittest
import rgot.champion
import rgot.optimizer
import rgot.database

__author__ = 'Vegard'


class TestOptimizer(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.dummy_champion_info = json.load(open('../data/dummy_champion.json', 'r'))
        self.champion_database = rgot.database.ChampionGenerator('../data/all_champions.json')
        self.item_base = rgot.database.ItemFactory('../data/all_items_parsed.json')

    def test_brute_force_write_result(self):
        items = []
        champion = self.champion_database.create_champion('Thresh')#rgot.champion.Champion(self.dummy_champion_info)
        target_champion = self.champion_database.create_champion('Thresh')#rgot.champion.Champion(self.dummy_champion_info)
        result = rgot.optimizer.brute_force_for_itemsets(champion, target_champion, items, 'autoAttackDPS')
        result.sort_permanently(ascending=False)
        result.write_to_json_file('./out/test.json')

    def test_aa_dps_with_tags_and_brute_force(self):
        lucian = self.champion_database.create_champion('Lucian')
        lucian.level = 1
        item_base = self.item_base.generate(['CriticalStrike', 'Damage', 'AttackSpeed', 'ArmorPenetration'])
        my_filters = {'maxNumberOfItems' : 1}
        result = rgot.optimizer.brute_force_for_itemsets(lucian, lucian, item_base, 'autoAttackDPS', my_filters)
        result.sort_permanently(ascending=False)
        result.write_to_csv_file('./out/test.csv')