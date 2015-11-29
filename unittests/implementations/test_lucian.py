import unittest
from rgot.database import ChampionGenerator, ItemFactory

class TestLucian(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.champion_generator = ChampionGenerator('../../data/all_champions.json')
        self.item_generator = ItemFactory('../../data/all_items_parsed.json')

    def tearDown(self):
        super().tearDown()

    def test_spell_scaling(self):
        lucian = self.champion_generator.create_champion('Lucian')
        q = lucian.calculate_scaled_damage_q(1)
        w = lucian.calculate_scaled_damage_w(2)
        e = lucian.calculate_scaled_damage_e(3)
        r = lucian.calculate_scaled_damage_r(2)
        self.assertEqual(lucian.name, 'Lucian')

    def test_q_spell_damage_with_item(self):
        lucian = self.champion_generator.create_champion('Lucian')
        q_noitem = lucian.direct_damage_q(1)
        lucian.items.append(self.item_generator.get('Infinity Edge'))
        q_ie = lucian.direct_damage_q(1)
        self.assertGreater(q_ie.physical, q_noitem.physical)

    def test_q_spell_scaling_with_item(self):
        lucian = self.champion_generator.create_champion('Lucian')
        lucian.items.append(self.item_generator.get('Infinity Edge'))
        q_ie = lucian.calculate_scaled_damage_q(1)
        self.assertGreater(q_ie.physical, 0)