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

    def test_lucian_spell_scaling(self):
        lucian = self.champion_generator.create_champion('Lucian')
        q = lucian.calculate_scaled_damage_q()
        w = lucian.calculate_scaled_damage_w()
        e = lucian.calculate_scaled_damage_e()
        r = lucian.calculate_scaled_damage_r()
        self.assertEqual(lucian.name, 'Lucian')