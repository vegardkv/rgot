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
        self.masteries = []
        self.runes = RuneSet()
        self.level = 1
        self.name = champion_data['name']
        # TODO: Item effects (e.x. randuins omen passive)
        self.item_effects = []

        # Protected variables

        # These values are read from champion_data directly, but should only be utilized by implementations of Champion.
        # The values are not necessarily correct for all champions, and each case must be inspected carefully. If the
        # values does not make sense, then they should be overwritten by the constructor of the implementation.
        self._q_damage = champion_data['spells'][0]['effect'][1]
        self._w_damage = champion_data['spells'][1]['effect'][1]
        self._e_damage = champion_data['spells'][2]['effect'][1]
        self._r_damage = champion_data['spells'][3]['effect'][1]

        self._q_scaling = champion_data['spells'][0].get('vars', {[]})
        self._w_scaling = champion_data['spells'][1].get('vars', {[]})
        self._e_scaling = champion_data['spells'][2].get('vars', {[]})
        self._r_scaling = champion_data['spells'][3].get('vars', {[]})

        # Private variables
        self.__bonus_stats = []
        self.__items = []

    # For implementations of Champion, override these. Another option is to implement an AbstractChampion class that
    # provide the interface to the Champion-class (for readability).
    def direct_damage_q(self, skill_level=1):
        return DamageSet(physical=0, magic=0, pure=0)

    def direct_damage_w(self, skill_level=1):
        return DamageSet(physical=0, magic=0, pure=0)

    def direct_damage_e(self, skill_level=1):
        return DamageSet(physical=0, magic=0, pure=0)

    def direct_damage_r(self, skill_level=1):
        return DamageSet(physical=0, magic=0, pure=0)

    # Damage over time returns the duration (default 0.0) and damage over time for a given ability. Override these.
    def damage_over_time_q(self, skill_level=1):
        return 0.0, DamageSet(physical=0, magic=0, pure=0)

    def damage_over_time_w(self, skill_level=1):
        return 0.0, DamageSet(physical=0, magic=0, pure=0)

    def damage_over_time_e(self, skill_level=1):
        return 0.0, DamageSet(physical=0, magic=0, pure=0)

    def damage_over_time_r(self, skill_level=1):
        return 0.0, DamageSet(physical=0, magic=0, pure=0)

    @property
    def bonus_stats(self):
        if not self.__bonus_stats:
            # Populated by item ids of each unique item that has been processed in order to check for unique effects
            unique_items = []
            # Matches item stat properties from "../data/all_items.json"
            temp_bonus_stats = {"rFlatArmorPenetrationMod": 0.0,
                                "rFlatPhysicalDamageModPerLevel": 0.0,
                                "rPercentArmorPenetrationMod": 0.0,
                                "FlatCritChanceMod": 0.0,
                                "FlatCritDamageMod": 0.0,
                                "FlatPhysicalDamageMod": 0.0,
                                "PercentAttackSpeedMod": 0.0,
                                "FlatArmorMod": 0.0}


            # TODO: Add other stats than physical modifiers and armor
            for item in self.__items:
                stats = item["stats"]
                if "rFlatArmorPenetrationMod" in stats:
                    temp_bonus_stats["rFlatArmorPenetrationMod"] += stats["rFlatArmorPenetrationMod"]

                if "rFlatPhysicalDamageModPerLevel" in stats:
                    temp_bonus_stats["rFlatPhysicalDamageModPerLevel"] += stats["rFlatPhysicalDamageModPerLevel"]

                # Percent armor penetration only occurs in unique effect "Last Whisper"
                if "rPercentArmorPenetrationMod" in stats:
                    temp_bonus_stats["rPercentArmorPenetrationMod"] = max(
                        stats["rPercentArmorPenetrationMod"],
                        temp_bonus_stats["rPercentArmorPenetrationMod"])

                if "FlatCritChanceMod" in stats:
                    temp_bonus_stats["FlatCritChanceMod"] += stats["FlatCritChanceMod"]

                if "FlatCritDamageMod" in stats:
                    temp_bonus_stats["FlatCritDamageMod"] += stats["FlatCritDamageMod"]

                if "FlatPhysicalDamageMod" in stats:
                    temp_bonus_stats["FlatPhysicalDamageMod"] += stats["FlatPhysicalDamageMod"]

                if "PercentAttackSpeedMod" in stats:
                    temp_bonus_stats["PercentAttackSpeedMod"] += stats["PercentAttackSpeedMod"]

                if "FlatArmorMod" in stats:
                    temp_bonus_stats["FlatArmorMod"] += stats["FlatArmorMod"]

            self.__bonus_stats = temp_bonus_stats

        return self.__bonus_stats

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, itemset):
        self.__items = itemset
        self.__bonus_stats = []

    def calculate_autoattack_dps(self, target=None):
        """
        useful information lmao
        """
        # TODO: Calculate with target items (randuins omen ect.)

        """
        Champion Stats
        """
        attack_damage = (self.basestats["attackdamage"] +
                         self.basestats["attackdamageperlevel"]*(self.level - 1) +
                         self.bonus_stats["FlatPhysicalDamageMod"] +
                         self.bonus_stats["rFlatPhysicalDamageModPerLevel"]*(self.level - 1))

        crit_chance = min(self.basestats["crit"] +
                          self.basestats["critperlevel"]*(self.level - 1) +
                          self.bonus_stats["FlatCritChanceMod"], 1.0)

        crit_damage = self.bonus_stats["FlatCritDamageMod"]

        # TODO: (1.0 + crit_damage) becomes (self.crit_damage_base + crit_damage)
        # From lol wiki: [Crit] Damage multiplier = 1 + (Critical chance × (1 + Bonus critical damage))
        crit_damage_multiplier = 1.0 + crit_chance * (1.0 + crit_damage)

        attack_speed_percent = (self.basestats["attackspeedperlevel"] / 100.0 * (self.level - 1) +
                                self.bonus_stats["PercentAttackSpeedMod"])

        attack_speed = self.base_attack_speed * (1.0 + attack_speed_percent)

        # TODO: Let this be controlled by some settings file/global variable
        if attack_speed > 2.5:
            attack_speed = 2.5

        armor_penetration_percent = self.bonus_stats["rPercentArmorPenetrationMod"]
        armor_penetration_flat = self.bonus_stats["rFlatArmorPenetrationMod"]

        """
        Target Stats
        """
        if target is not None:
            target_armor = (target.basestats["armor"] +
                            target.basestats["armorperlevel"]*target.level +
                            target.bonus_stats["FlatArmorMod"])
        else:
            target_armor = 0.0

        # TODO: Percent armor reduction (Black cleaver)
        target_armor_actual = target_armor * (1.0 - armor_penetration_percent) - armor_penetration_flat

        # TODO: Armor under 0.0 (Flat armor reduction, e.x. Rammus taunt)
        if target_armor_actual < 0.0:
            target_armor_actual = 0.0

        armor_multiplier = 100.0 / (target_armor_actual + 100.0)

        """
        Physical dps calculation
        """
        physical_dps = attack_damage * attack_speed * crit_damage_multiplier * armor_multiplier

        return DamageSet(physical=physical_dps, magic=0.0, pure=0.0)


"""
class Lucian(Champion):
    def __init__(self):
        stats = dict(attackDamage=50, attackSpeed=0.625)
        super().__init__(stats)

    def calculate_autoattack_dps(self):
        pass
"""