
__author__'knutanha'

class Item:
    def __init__(self, iteminfo):
        for key, value in iteminfo["stats"].items():
            if key == "rPercentArmorPenetrationMod" or key == "FlatCritDamageMod":
                temp_bonus_stats[key] = max(value, temp_bonus_stats[key])
            else:
                temp_bonus_stats[key] += value
        self.__bonus_stats = temp_bonus_stats