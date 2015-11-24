import rgot.database

__author__ = 'Vegard'

import unittest

class TestChampionGenerator(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.champion_generator = rgot.database.ChampionGenerator('../data/all_champions.json')

    def test_generate_lucian(self):
        lucian = self.champion_generator.create_champion('Lucian')
        self.assertEqual(lucian.name, 'Lucian')

class TestItemGeneretor(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        super().setUp()
        self.item_generator = rgot.database.ItemBaseGenerator('../data/all_items_parsed.json')

    def test_get_by_name(self):
        ie = self.item_generator.get(name='Infinity Edge')
        self.assertEqual(ie['id'], 3031)

    def test_get_by_index(self):
        ie1 = self.item_generator.get(index=3031)
        ie2 = self.item_generator.get(index='3031')
        self.assertEqual(ie1['name'], 'Infinity Edge')
        self.assertEqual(ie2['name'], 'Infinity Edge')