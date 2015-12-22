from collections import namedtuple, defaultdict

__author__ = 'Vegard'


class ItemSet:
    pass

DamageSet = namedtuple('DamageSet', ['physical', 'magic', 'pure'])
DamageSet.__new__.__defaults__ = (0, 0, 0)  # In order for values to default to 0. E.g. DamageSet(magic=5).

def add_damage_sets(ds1, ds2):
    """
    :param ds2: DamageSet
    :param ds1: DamageSet
    :rtype: DamageSet
    """
    return DamageSet(physical=ds1.physical + ds2.physical, magic=ds1.magic + ds2.magic, pure=ds1.pure + ds2.pure)

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

        self._q_cooldown = champion_data['spells'][0]['cooldown']
        self._w_cooldown = champion_data['spells'][1]['cooldown']
        self._e_cooldown = champion_data['spells'][2]['cooldown']
        self._r_cooldown = champion_data['spells'][3]['cooldown']

        self._q_damage_category = None
        self._w_damage_category = None
        self._e_damage_category = None
        self._r_damage_category = None

        # Private variables
        self.__bonus_stats = []
        self.__items = []

    # For implementations of Champion, override these. Another option is to implement an AbstractChampion class that
    # provide the interface to the Champion-class (for readability).
    def direct_damage_q(self, skill_level=1, target=None):
        if self._q_damage_category == 'physical':
            dmg = add_damage_sets(DamageSet(physical=self._q_damage[skill_level-1]),
                                  self._calculate_scaled_damage('q', skill_level))
        elif self._q_damage_category == 'magic':
            dmg = add_damage_sets(DamageSet(magic=self._q_damage[skill_level-1]),
                                  self._calculate_scaled_damage('q', skill_level))
        elif self._q_damage_category == 'pure':
            dmg = add_damage_sets(DamageSet(pure=self._q_damage[skill_level-1]),
                                  self._calculate_scaled_damage('q', skill_level))
        else:
            raise AttributeError('Damage Category not defined for Q for champion %s' % self.name)
        if target is None:
            return dmg
        else:
            return self._calculate_resisted_damage(dmg, target)

    def direct_damage_w(self, skill_level=1, target=None):
        if self._w_damage_category == 'physical':
            dmg = add_damage_sets(DamageSet(physical=self._w_damage[skill_level-1]),
                                  self._calculate_scaled_damage('w', skill_level))
        elif self._w_damage_category == 'magic':
            dmg = add_damage_sets(DamageSet(magic=self._w_damage[skill_level-1]),
                                  self._calculate_scaled_damage('w', skill_level))
        elif self._w_damage_category == 'pure':
            dmg = add_damage_sets(DamageSet(pure=self._w_damage[skill_level-1]),
                                  self._calculate_scaled_damage('w', skill_level))
        else:
            raise AttributeError('Damage Category not defined for W for champion %s' % self.name)
        if target is None:
            return dmg
        else:
            return self._calculate_resisted_damage(dmg, target)


    def direct_damage_e(self, skill_level=1, target=None):
        if self._w_damage_category == 'physical':
            dmg = add_damage_sets(DamageSet(physical=self._e_damage[skill_level-1]),
                                  self._calculate_scaled_damage('e', skill_level))
        elif self._w_damage_category == 'magic':
            dmg = add_damage_sets(DamageSet(magic=self._e_damage[skill_level-1]),
                                  self._calculate_scaled_damage('e', skill_level))
        elif self._w_damage_category == 'pure':
            dmg = add_damage_sets(DamageSet(pure=self._e_damage[skill_level-1]),
                                  self._calculate_scaled_damage('e', skill_level))
        else:
            raise AttributeError('Damage Category not defined for E for champion %s' % self.name)
        if target is None:
            return dmg
        else:
            return self._calculate_resisted_damage(dmg, target)

    def direct_damage_r(self, skill_level=1, target=None):
        if self._r_damage_category == 'physical':
            dmg = add_damage_sets(DamageSet(physical=self._r_damage[skill_level-1]),
                                  self._calculate_scaled_damage('r', skill_level))
        elif self._r_damage_category == 'magic':
            dmg = add_damage_sets(DamageSet(magic=self._r_damage[skill_level-1]),
                                  self._calculate_scaled_damage('r', skill_level))
        elif self._r_damage_category == 'pure':
            dmg = add_damage_sets(DamageSet(pure=self._r_damage[skill_level-1]),
                                  self._calculate_scaled_damage('r', skill_level))
        else:
            raise AttributeError('Damage Category not defined for R for champion %s' % self.name)
        if target is None:
            return dmg
        else:
            return self._calculate_resisted_damage(dmg, target)

    # Damage over time returns the duration (default 0.0) and damage over time for a given ability. Override these.
    def damage_over_time_q(self, skill_level=1, target=None):
        return 0.0, DamageSet()

    def damage_over_time_w(self, skill_level=1, target=None):
        return 0.0, DamageSet()

    def damage_over_time_e(self, skill_level=1, target=None):
        return 0.0, DamageSet()

    def damage_over_time_r(self, skill_level=1, target=None):
        return 0.0, DamageSet()

    @property
    def bonus_stats(self):
        if not self.__bonus_stats:
            # Populated by item ids of each unique item that has been processed in order to check for unique effects
            # unique_items = []

            # Matches item stat properties from "../data/all_items.json"
            # TODO: Keep this list of stats somewhere. When using defaultdict, it is not necessary to initialize with 0.
            # The list is however useful as a lookup-table.
            self.__bonus_stats = defaultdict(float)
            self.__bonus_stats.update({
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
            })

            # Collecting stats from items
            for item in self.__items:
                for key, value in item["stats"].items():
                    if key == "rPercentArmorPenetrationMod" or key == "FlatCritDamageMod":
                        self.__bonus_stats[key] = max(value, self.__bonus_stats[key])
                    else:
                        self.__bonus_stats[key] += value
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

    # MAGIC RESIST
    @property
    def derived_magic_resist(self):
        return (self.basestats["spellblock"] +
                self.basestats["spellblockperlevel"] * (self.level - 1) +
                self.bonus_stats["FlatSpellBlockMod"] +
                self.bonus_stats["rFlatSpellBlockModPerLevel"] * (self.level - 1)
                ) * (1.0 + self.bonus_stats["PercentSpellBlockMod"])

    # ABILITIES
    # Ability Power
    @property
    def derived_ability_power(self):
        return 0

    # Magic Penetration
    #              "rFlatMagicPenetrationMod": 0.0,
    #           "rFlatMagicPenetrationModPerLevel": 0.0,
    #           "rPercentMagicPenetrationMod": 0.0,
    #                  "rPercentMagicPenetrationModPerLevel": 0.0,
    # TODO: Implement derived_percent_magic_penetration
    @property
    def derived_percent_magic_penetration(self):
        return 0.0

    # TODO: Implement derived_flat_magic_penetration
    @property
    def derived_flat_magic_penetration(self):
        return 0.0


    @property
    def derived_cooldown_reduction(self):
        return self.bonus_stats['rPercentCooldownMod'] + self.bonus_stats['rPercentCooldownModPerLevel'] * self.level

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, itemset):
        self.__items = itemset
        self.__bonus_stats = []

    def calculate_autoattack_damage(self, target=None):
        if target is None:
            return DamageSet(physical=self.derived_base_attack_damage + self.derived_bonus_attack_damage)
        else:
            return self._calculate_resisted_damage(
            DamageSet(physical=self.derived_base_attack_damage + self.derived_bonus_attack_damage), target)


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

    def calculate_scaled_damage_q(self, skill_level=1):
        return self._calculate_scaled_damage('q', skill_level=skill_level)

    def calculate_scaled_damage_w(self, skill_level=1):
        return self._calculate_scaled_damage('w', skill_level=skill_level)

    def calculate_scaled_damage_e(self, skill_level=1):
        return self._calculate_scaled_damage('e', skill_level=skill_level)

    def calculate_scaled_damage_r(self, skill_level=1):
        return self._calculate_scaled_damage('r', skill_level=skill_level)

    # Utility functions
    def _calculate_scaled_damage(self, ability, skill_level=0):
        """
        This is a seperate function from calculate_scaled_damage_X in order to be able to override specific
        calculate_scaled_damage-function.
        :param ability: q,w,e,r
        :return:
        """
        if ability == 'q':
            scaling = self._q_scaling
        elif ability == 'w':
            scaling = self._w_scaling
        elif ability == 'e':
            scaling = self._e_scaling
        elif ability == 'r':
            scaling = self._r_scaling
        else:
            raise Exception('Scaling not defined for ability: %s.' % ability)
        ph, ma, pu = 0, 0, 0
        for entry in scaling:
            if entry.get('link', None) == 'spelldamage':
                ma += entry['coeff'][0 if len(entry['coeff']) == 1 else skill_level - 1] * self.derived_ability_power
            elif  entry.get('link', None) == 'attackdamage':
                ph += entry['coeff'][0 if len(entry['coeff']) == 1 else skill_level - 1] * \
                      (self.derived_bonus_attack_damage + self.derived_base_attack_damage)
        return DamageSet(physical=ph, magic=ma, pure=pu)

    def _calculate_resisted_damage(self, damageset, target):
        if target is None:
            raise ValueError('target cannot be None.')
        physical_damage, magic_damage, pure_damage = 0, 0, 0
        if damageset.physical > 0:
            target_armor_perceived = (target.derived_base_armor +
                                      (target.derived_bonus_armor *
                                       (1.0 - self.bonus_stats["rPercentArmorPenetrationMod"])) -
                                      self.bonus_stats["rFlatArmorPenetrationMod"])
            target_armor_perceived = target_armor_perceived if target_armor_perceived >= 0.0 else 0.0
            armor_multiplier = 100.0 / (target_armor_perceived + 100.0)
            physical_damage = damageset['physical'] * armor_multiplier
        if damageset['magic'] > 0:
            # TODO: Implement magic resist reduction
            # From wiki:
            # 1. Magic reduction, flat. (can reduce mr < 0) (debuff on target)
            # 2. Magic reduction, percentage. (only > 0) (debuff on target)
            # 3. Magic penetration, percentage. (only > 0)
            # 4. Magic penetration, flat. (only > 0)
            target_MR_perceived = (target.derived_magic_resist *
                                   (1.0 - self.derived_percent_magic_penetration) -
                                   self.derived_flat_magic_penetration)
            if target_MR_perceived < 0:
                magic_damage = damageset['magic'] * (2 - 100.0/(100.0 - target_MR_perceived))
            else:
                magic_damage = damageset['magic'] * (1 - 100.0/(100.0 + target_MR_perceived))
        if damageset['pure'] > 0:
            pure_damage = damageset['pure']
        return DamageSet(physical=physical_damage, magic=magic_damage, pure=pure_damage)

    def calculate_continuous_rotation(self, order, skill_levels, target=None, tmax=10):
        CAST_TIME = 0.25
        cdr = self.derived_cooldown_reduction
        q = [(0, val) for val in order]
        t = 0
        out = []
        while True:
            et, skill = q.pop(0)
            skill_index = order.index(skill)
            t = max(t, et) + CAST_TIME
            if t > tmax:
                break
            if skill == 'q':
                damage_dealt = self.direct_damage_q(skill_levels[skill_index], target)
                t_cd = self._q_cooldown[skill_levels[skill_index]-1] * (1 - cdr)
            elif skill == 'w':
                damage_dealt = self.direct_damage_w(skill_levels[skill_index], target)
                t_cd = self._w_cooldown[skill_levels[skill_index]-1] * (1 - cdr)
            elif skill == 'e':
                damage_dealt = self.direct_damage_e(skill_levels[skill_index], target)
                t_cd = self._e_cooldown[skill_levels[skill_index]-1] * (1 - cdr)
            elif skill == 'r':
                damage_dealt = self.direct_damage_r(skill_levels[skill_index], target)
                t_cd = self._r_cooldown[skill_levels[skill_index]-1] * (1 - cdr)
            else:
                raise ValueError('Could not find spell named: %s' % skill)
            out.append((t, skill, damage_dealt))
            insert_location = ([key for key, val in enumerate(q) if val[0] > t + t_cd] or [len(q)])[0]
            q.insert(insert_location, (t + t_cd, skill))
        return out

    def calculate_rotation(self, rotation, skill_levels, target=None):
        tot = DamageSet()
        for spell in rotation:
            if spell=='q':
                tot = add_damage_sets(tot, self.direct_damage_q(skill_levels['q'], target))
            elif spell=='w':
                tot = add_damage_sets(tot, self.direct_damage_w(skill_levels['w'], target))
            elif spell=='e':
                tot = add_damage_sets(tot, self.direct_damage_w(skill_levels['e'], target))
            elif spell=='r':
                tot = add_damage_sets(tot, self.direct_damage_r(skill_levels['r'], target))
            elif spell=='aa':
                #TODO: implement aa damage
                tot = add_damage_sets(tot, self.calculate_autoattack_damage(target))
            else:
                raise ValueError('Could not find spell named: %s' % spell)
        return tot



"""
t = 0
while t < tmax
    et,skill = queue.pop()
    t = max(last t, et)+ cast time
    dmg.append(skill.damage)
    tstamp.append(t)
    insert(t,skill) into queue


CAST_TIME = 0.25
cd = [0]*len(order)
cdr = self.derived_cooldown_reduction
event_queue = [[0.0, o] for o in order]

time_stamps = []
damages = []
t = 0
while t < tmax:
    next_ability = event_queue.pop(0)
    spell_name = next_ability[1]
    if  spell_name == 'q':
        next_time_available = (1-cdr) * self._q_cooldown[skill_levels[order.index[spell_name]]]
        for i, e in enumerate(event_queue):
            if e[0] > next_time_available:
                event_queue.insert(i, [next_time_available, spell_name])
    time_stamps.append(next_ability[0])
    if next_ability[1] == 'q':
"""
