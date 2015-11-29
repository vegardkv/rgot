import rgot.database
from rgot import champion as cp
from collections import namedtuple, defaultdict

__author__='knutanha'

class Item:
    def __init__(self, item_data):
        """
        :param item_data:
        :return:
        """
        # Not sure if this should be private or not... Should at least implement as a property?
        self.__item_data = item_data

    def __getitem__(self, item):
        return self.__item_data[item]

    def __contains__(self, item):
        return item in self.__item_data

    @property
    def bonus_stats(self):
        return self['stats']


class ItemSet:
    def __init__(self, items):
        self.__items = items
        self.__total_stats = defaultdict(float)

    def __getitem__(self, item):
        return self.__items[item]

    @property
    def bonus_stats(self):
        if not self.__total_stats:
            for item in self.__items:
                for stat_name, stat_value in item.bonus_stats.items():
                    self.__total_stats[stat_name] += stat_value
        return self.__total_stats






#PassiveEffect = namedtuple('PassiveEffect', ['group', 'type', 'unit', 'amount',
                                       #'minion_cap', 'unique', 'unique_name'])

#ActiveEffect = namedtuple('ActiveEffect',[])

"""
class Item:
    def __init__(self, itemname=None, itemid=None, iteminfo=None):
        if iteminfo is not None:
            self.__item_info = iteminfo
        else:
            item_base = rgot.database.ItemBaseGenerator('../data/all_items_parsed.json')
            if itemname is not None:
                self.__item_info = item_base.get(name=itemname)
            elif itemid is not None:
                self.__item_info = item_base.get(id=itemid)
            else:
                # pls no
                pass
        self.__passive_effect_list
        self.__active_effect_list

        self.__populate_passive_effect_list()
        self.__populate_active_effect_list()


    @property
    def item_info(self):
        return self.__iteminfo

    def __populate_passive_effect_list(self):
        name = self.__item_info['name']
        if name=='Blade of the Ruined King':
            self.effect_list.append(PassiveEffect(
                group="OnAutoAttack", type="physicalDamage", unit="PercentTargetCurrentHP",
                amount=self.__item_info['effect']['Effect1Amount'], minion_cap=60,
                unique=True, unique_name=None))
"""
"""
    Passive Effects:
    group=['OnAutoAttack']
    type=['physicalDamage']
    unit=['PercentTargetCurrentHP']
    amount= <flat_number_matching_unit>
    minion_cap = <flat_number>
    unique=[True,False]
    unique_name=[None, '<unique_effect_name>']
"""


"""
    def __populate_active_effect_list(self):
            self.effect_list.append(PassiveEffect(
                group="activeOnEnemyTarget"
            ))
"""

"""
    Passive Effects:
    group=['OnAutoAttack']
    type=['physicalDamage']
    unit=['PercentTargetCurrentHP']
    amount= <flat_number_matching_unit>
    minion_cap = <flat_number>
    unique=[True,False]
    unique_name=[None, '<unique_effect_name>']
"""



"""


class ItemEffect:
    def __init__(self, item_name):
        # some stuff
        pass

    def getEffect(self):
        return # some object that gives context and effect


class botrk_effect_1(ItemEffect):
    def __init__(self):
"""
