from rgot.champion import Champion, DamageSet

__author__ = 'Vegard'

class Lucian(Champion):
    def __init__(self, champion_data):
        super().__init__(champion_data)
        # TODO: do this in the Champion class? Is the data always structured as follows?
        number_of_shots = champion_data['spells'][3]['effect'][5]
        damage_per_shot = champion_data['spells'][3]['effect'][2]

        # Private
        self.__r_damage = [z[0]*z[1] for z in zip(number_of_shots, damage_per_shot)]
        pass

    def direct_damage_e(self, skill_level=1):
        return super().direct_damage_e()

    def direct_damage_w(self, skill_level=1):

        return super().direct_damage_w()

    def direct_damage_r(self, skill_level=1):
        return super().direct_damage_r()

    def direct_damage_q(self, skill_level=1):
        return super().direct_damage_q()

