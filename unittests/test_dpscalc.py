import json
import rgot.champion as dc

__author__ = 'Vegard'

import unittest

class TestDpsCalc(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.dummy_champion_info = json.load(open('../data/dummy_champion.json', 'r'))

    def test_dps_calc(self):
        general_champion = dc.Champion(self.dummy_champion_info)
        result = general_champion.calculate_autoattack_dps(level=10)
        self.assertEqual(result['physical'], 0.625*(50 + 10*5))