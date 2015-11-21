from collections import namedtuple

__author__ = 'Vegard'

class ItemSet:
    pass

DamageSet = namedtuple('DamageSet', ['physical', 'magic', 'pure'])

ATTACK_SPEED_NUMERATOR = 0.625 #  http://leagueoflegends.wikia.com/wiki/Attack_speed

class RuneSet:
    def __init__(self):
        self.stats = {}

    def stats(self):
        pass

class Champion:
    def __init__(self, champion_data):
        global ATTACK_SPEED_NUMERATOR
        self.base_attack_speed = ATTACK_SPEED_NUMERATOR/(1 + champion_data['stats']['attackspeedoffset'])
        self.basestats = champion_data['stats']
        self.items = []
        self.masteries = []
        self.runes = RuneSet()
        self.level = 1

    def calculate_autoattack_dps(self, target=None):
        return DamageSet(physical=0, magic=0, pure=0)


"""
class Lucian(Champion):
    def __init__(self):
        stats = dict(attackDamage=50, attackSpeed=0.625)
        super().__init__(stats)

    def calculate_autoattack_dps(self):
        pass
"""