import json
import unittest
import rgot.database
from rgot.database import ItemFactory

__author__ = 'knutanha'

class TestItem(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.item_db = ItemFactory('../data/all_items_parsed.json')
#        self.botrk = self.full_item_base.get(name="Blade of the ruined king")

    def test_bonus_stats_single_item(self):
        ie = self.item_db.get(name = 'Infinity Edge')
        self.assertIn('FlatCritChanceMod', ie.bonus_stats)
        self.assertIn('FlatCritDamageMod', ie.bonus_stats)
        self.assertIn('FlatPhysicalDamageMod', ie.bonus_stats)

class TestItemSet(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.item_db = ItemFactory('../data/all_items_parsed.json')

    def test_bonus_stats_for_two_items(self):
        itemset = self.item_db.get_itemset(['Infinity Edge', 'Blade of the Ruined King'])
        self.assertIn('FlatCritChanceMod', itemset.bonus_stats)
        self.assertIn('FlatCritDamageMod', itemset.bonus_stats)
        self.assertIn('FlatPhysicalDamageMod', itemset.bonus_stats)
        self.assertIn('PercentAttackSpeedMod', itemset.bonus_stats)
        self.assertIn('PercentLifeStealMod', itemset.bonus_stats)


"""
    def test_iteminfo(self):


        general_champion = dc.Champion(self.dummy_champion_info)
        result = general_champion.calculate_autoattack_dps()
        self.assertEqual(result['physical'], 0.625*(50 + 10*5))
        self.assertEqual(result['magic'], 0)
        self.assertEqual(result['pure'], 0)

"""