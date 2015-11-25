from rgot.champion import Champion, DamageSet

__author__ = 'Vegard'


class Lucian(Champion):
    def __init__(self, champion_data):
        super().__init__(champion_data)
        number_of_shots = champion_data['spells'][3]['effect'][5]
        damage_per_shot = champion_data['spells'][3]['effect'][2]

        # Protected
        self._q_damage_category = 'physical'
        self._w_damage_category = 'magic'
        self._r_damage_category = 'physical'

        # Private
        self.__r_damage = [z[0]*z[1] for z in zip(number_of_shots, damage_per_shot)]
        pass