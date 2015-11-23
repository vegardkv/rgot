from collections import namedtuple

__author__ = 'Vegard'

class ItemSet:
    pass

DamageSet = namedtuple('DamageSet', ['physical', 'magic', 'pure'])
ATTACK_SPEED_NUMERATOR = 0.625  # http://leagueoflegends.wikia.com/wiki/Attack_speed


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

        self._q_scaling = champion_data['spells'][0].get('vars', [{}])
        self._w_scaling = champion_data['spells'][1].get('vars', [{}])
        self._e_scaling = champion_data['spells'][2].get('vars', [{}])
        self._r_scaling = champion_data['spells'][3].get('vars', [{}])

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
            # unique_items = []

            # Matches item stat properties from "../data/all_items.json"
            # TODO: Ikke fyll inn alle keys, la bonus_stats returnere 0.0 dersom taggen ikke fins
            temp_bonus_stats = {
                # AD STATS
                # Attack Damage
                "rFlatPhysicalDamageModPerLevel": 0.0,
                "FlatPhysicalDamageMod": 0.0,
                "PercentPhysicalDamageMod": 0.0,
                # Critical Chance
                "FlatCritChanceMod": 0.0,
                "FlatCritDamageMod": 0.0,
                "PercentCritChanceMod": 0.0,    # Not used
                "PercentCritDamageMod": 0.0,    # Not used
                "rFlatCritChanceModPerLevel": 0.0,
                "rFlatCritDamageModPerLevel": 0.0,
                # Attack Speed
                "PercentAttackSpeedMod": 0.0,
                "FlatAttackSpeedMod": 0.0,  # Not used
                "rPercentAttackSpeedModPerLevel": 0.0,
                # Armor Penetration
                "rFlatArmorPenetrationMod": 0.0,
                "rPercentArmorPenetrationMod": 0.0,
                "rFlatArmorPenetrationModPerLevel": 0.0,
                "rPercentArmorPenetrationModPerLevel": 0.0,
                # Life Steal
                "PercentLifeStealMod": 0.0,

                # AP STATS
                # Ability Power / Magic Damage
                "PercentMagicDamageMod": 0.0,
                "FlatMagicDamageMod": 0.0,
                "rFlatMagicDamageModPerLevel": 0.0,
                # Magic Penetration
                "rFlatMagicPenetrationMod": 0.0,
                "rFlatMagicPenetrationModPerLevel": 0.0,
                "rPercentMagicPenetrationMod": 0.0,
                "rPercentMagicPenetrationModPerLevel": 0.0,
                # Spell Vamp
                "PercentSpellVampMod": 0.0,

                # COOLDOWN REDUCTION
                "rPercentCooldownMod": 0.0,
                "rPercentCooldownModPerLevel": 0.0,

                # RESOURCE POOL STATS
                # Mana
                "FlatMPPoolMod": 0.0,
                "rFlatMPModPerLevel": 0.0,
                "PercentMPPoolMod": 0.0,
                "FlatMPRegenMod": 0.0,
                "rFlatMPRegenModPerLevel": 0.0,
                "PercentMPRegenMod": 0.0,
                # Energy
                "FlatEnergyPoolMod": 0.0,
                "rFlatEnergyModPerLevel": 0.0,
                "FlatEnergyRegenMod": 0.0,
                "rFlatEnergyRegenModPerLevel": 0.0,

                # HP POOL
                "FlatHPPoolMod": 0.0,
                "rFlatHPModPerLevel": 0.0,
                "PercentHPPoolMod": 0.0,
                "FlatHPRegenMod": 0.0,
                "rFlatHPRegenModPerLevel": 0.0,
                "PercentHPRegenMod": 0.0,

                # DEFENSIVE STATS
                # Armor
                "FlatArmorMod": 0.0,
                "rFlatArmorModPerLevel": 0.0,
                "PercentArmorMod": 0.0,
                # Magic Resist / Spell Block
                "FlatSpellBlockMod": 0.0,
                "rFlatSpellBlockModPerLevel": 0.0,
                "PercentSpellBlockMod": 0.0,
                # Dodge (obsolete)
                "rFlatDodgeMod": 0.0,
                "rFlatDodgeModPerLevel": 0.0,
                "PercentDodgeMod": 0.0,
                # Block
                "FlatBlockMod": 0.0,
                "PercentBlockMod": 0.0,

                # MOVEMENT SPEED
                "FlatMovementSpeedMod": 0.0,
                "rFlatMovementSpeedModPerLevel": 0.0,
                "PercentMovementSpeedMod": 0.0,
                "rPercentMovementSpeedModPerLevel": 0.0,

                # MISC STATS
                # Bonus XP
                "FlatEXPBonus": 0.0,
                "PercentEXPBonus": 0.0,
                # Gold per 10 sec
                "rFlatGoldPer10Mod": 0.0,
                # Time Dead
                "rFlatTimeDeadMod": 0.0,
                "rFlatTimeDeadModPerLevel": 0.0,
                "rPercentTimeDeadMod": 0.0,
                "rPercentTimeDeadModPerLevel": 0.0,
            }

            # Collecting stats from items
            # TODO: en UNIQUE handler (må tagges på en eller annen måte)
            for item in self.__items:
                for key, value in item["stats"].items():
                    if key == "rPercentArmorPenetrationMod" or key == "FlatCritDamageMod":
                        temp_bonus_stats[key] = max(value, temp_bonus_stats[key])
                    else:
                        temp_bonus_stats[key] += value
            self.__bonus_stats = temp_bonus_stats

        return self.__bonus_stats

    # Common calculations has the "derived"-tag
    # AD STATS
    @property
    def derived_bonus_attack_damage(self):
        return (self.bonus_stats["rFlatPhysicalDamageModPerLevel"] *
                (self.level - 1) + self.bonus_stats["FlatPhysicalDamageMod"])

    @property
    def derived_base_attack_damage(self):
        return self.basestats["attackdamage"] + self.basestats["attackdamageperlevel"] * (self.level - 1)

    @property
    def derived_total_attack_speed(self):
        total_attack_speed = (self.base_attack_speed * (1.0 +
                              self.basestats["attackspeedperlevel"] / 100.0 * (self.level - 1) +
                              self.bonus_stats["PercentAttackSpeedMod"] +
                              self.bonus_stats["rPercentAttackSpeedModPerLevel"] * (self.level - 1)))
        return total_attack_speed if total_attack_speed <= 2.5 else 2.5

    @property
    def derived_total_crit_chance(self):
        total_crit_chance = ((self.bonus_stats["FlatCritChanceMod"] +
                              self.bonus_stats["rFlatCritChanceModPerLevel"] * (self.level - 1) +
                              self.basestats["crit"] +
                              self.basestats["critperlevel"] * (self.level - 1)) *
                             (1.0 + self.bonus_stats["PercentCritChanceMod"]))
        return total_crit_chance if total_crit_chance <= 1.0 else 1.0

    # TODO: "PercentCritDamageMod" would this apply to total crit damage or only bonus
    # Given as a number 1.0 + bonus_crit_damage
    @property
    def derived_total_crit_damage(self):
        return (1.0 + self.bonus_stats["rFlatCritDamageModPerLevel"] * (self.level - 1) +
                self.bonus_stats["FlatCritDamageMod"])

    # ARMOR
    @property
    def derived_base_armor(self):
        return self.basestats["armor"] + self.basestats["armorperlevel"] * (self.level - 1)

    @property
    def derived_bonus_armor(self):
        return self.bonus_stats["FlatArmorMod"] + self.bonus_stats["rFlatArmorModPerLevel"] * (self.level - 1)

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, itemset):
        self.__items = itemset
        self.__bonus_stats = []

    def calculate_autoattack_dps(self, target=None):
        """
        Calculates Champion auto attack damage per second.
        :param target: Champion-instance of target
        :return DamageSet-instance
        """
        # TODO: Calculate with target items (randuins omen ect.)
        # TODO: Percent armor reduction (Black cleaver)
        # TODO: Armor under 0.0 (Flat armor reduction, e.x. Rammus taunt)

        attack_damage = self.derived_base_attack_damage + self.derived_bonus_attack_damage

        # From lol wiki: [Crit] Damage multiplier = 1 + (Critical chance × (1 + Bonus critical damage))
        crit_damage_multiplier = 1.0 + self.derived_total_crit_chance * self.derived_total_crit_damage

        if target is not None:
            target_armor_perceived = (target.derived_base_armor +
                                      (target.derived_bonus_armor *
                                       (1.0 - self.bonus_stats["rPercentArmorPenetrationMod"])) -
                                      self.bonus_stats["rFlatArmorPenetrationMod"])
            target_armor_perceived = target_armor_perceived if target_armor_perceived >= 0.0 else 0.0

        else:
            target_armor_perceived = 0.0
        armor_multiplier = 100.0 / (target_armor_perceived + 100.0)

        physical_dps = attack_damage * self.derived_total_attack_speed * crit_damage_multiplier * armor_multiplier

        return DamageSet(physical=physical_dps, magic=0.0, pure=0.0)

    # Utility functions
    def _calculate_scaled_damage(self, ability):
        if ability=='q':
            scaling = self._q_scaling
        elif ability=='w':
            scaling = self._w_scaling
        elif ability=='e':
            scaling = self._e_scaling
        elif ability=='r':
            scaling = self._r_scaling
        else:
            raise Exception('Scaling not defined for ability: %s.' % ability)
        ph, ma, pu = 0, 0, 0
        for k, v in scaling.items():
            if k=='spelldamage':
                ma += 0.9



    def _calculate_resisted_damage(self, damageset, target):
        physical_damage, magic_damage, pure_damage = 0, 0, 0
        if damageset['physical'] > 0:
            target_armor_perceived = (target.derived_base_armor +
                                      (target.derived_bonus_armor *
                                       (1.0 - self.bonus_stats["rPercentArmorPenetrationMod"])) -
                                      self.bonus_stats["rFlatArmorPenetrationMod"])
            target_armor_perceived = target_armor_perceived if target_armor_perceived >= 0.0 else 0.0
            armor_multiplier = 100.0 / (target_armor_perceived + 100.0)
            physical_damage = damageset['physical'] * armor_multiplier
        if damageset['magic'] > 0:
            magic_damage = damageset['magic']
        if damageset['pure'] > 0:
            pure_damage = damageset['pure']
        return DamageSet(physical=physical_damage, magic=magic_damage, pure=pure_damage)

"""
class Lucian(Champion):
    def __init__(self):
        stats = dict(attackDamage=50, attackSpeed=0.625)
        super().__init__(stats)

    def calculate_autoattack_dps(self):
        pass
"""