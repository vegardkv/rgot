import json
import rgot.champion as dc

__author__ = 'Vegard'

import unittest

class TestChampion(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.dummy_champion_info = json.load(open('../data/dummy_champion.json', 'r'))

    def test_auto_attack_dps_calc(self):
        general_champion = dc.Champion(self.dummy_champion_info)
        result = general_champion.calculate_autoattack_dps()
        self.assertEqual(result['physical'], 0.625*(50 + 10*5))
        self.assertEqual(result['magic'], 0)
        self.assertEqual(result['pure'], 0)