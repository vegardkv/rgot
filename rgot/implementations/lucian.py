from rgot.champion import Champion, DamageSet

__author__ = 'Vegard'


class Lucian(Champion):
    def __init__(self, champion_data):
        super().__init__(champion_data)
        number_of_shots = champion_data['spells'][3]['effect'][5]
        damage_per_shot = champion_data['spells'][3]['effect'][2]

        # Private
        self.__r_damage = [z[0]*z[1] for z in zip(number_of_shots, damage_per_shot)]
        pass

    def direct_damage_e(self, skill_level=1):
        return super().direct_damage_e()

    def direct_damage_w(self, skill_level=1): #todo: this can perhaps be moved to the parent class?
        tmp_damage = self._w_damage[skill_level] + self._w_scaling['coeff'] * self.bonus_stats.get()
        return super().direct_damage_w()

    def direct_damage_r(self, skill_level=1):
        return super().direct_damage_r()

    def direct_damage_q(self, skill_level=1):
        return super().direct_damage_q()

