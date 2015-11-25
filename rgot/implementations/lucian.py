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

    def direct_damage_e(self, skill_level=1, target=None):
        return super().direct_damage_e()

    def direct_damage_w(self, skill_level=1, target=None):
        base = DamageSet(physical=0, magic=self._w_damage[skill_level], pure=0)
        scaled = self._calculate_scaled_damage('w', skill_level)
        if target is None:
            return DamageSet(physical=0, magic=base.magic + scaled.magic, pure=0)
        else:
            self._calculate_resisted_damage(DamageSet(physical=0, magic=base.magic + scaled.magic, pure=0), target)

    def direct_damage_r(self, skill_level=1, target=None):
        return super().direct_damage_r()

    def direct_damage_q(self, skill_level=1, target=None):
        base = DamageSet(physical=self._q_damage[skill_level], magic=0, pure=0)
        scaled = self._calculate_scaled_damage('q', skill_level)
        if target is None:
            return DamageSet(physical=base.physical + scaled.physical, magic=0, pure=0)
        else:
            self._calculate_resisted_damage(DamageSet(physical=base.physical+scaled.physical, magic=0, pure=0), target)