import json
import unittest
import rgot.champion
import rgot.optimizer

__author__ = 'Vegard'


class TestOptimizer(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.dummy_champion_info = json.load(open('../data/dummy_champion.json', 'r'))

    def test_brute_force_write_result(self):
        items = []
        champion = rgot.champion.Champion(self.dummy_champion_info)
        target_champion = rgot.champion.Champion(self.dummy_champion_info)
        result = rgot.optimizer.brute_force_for_itemsets(champion, target_champion, items)
        result.sort_permanently(ascending=False)
        result.write_to_json('./out/test.json')