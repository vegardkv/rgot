import json
import rgot.champion
from rgot.implementations.lucian import Lucian

__author__ = 'Vegard'

class ItemBaseGenerator:
    def __init__(self, filename):
        self.all_items = json.load(open(filename, 'r'))['data']

    def generate(self, or_tags=None):
        if or_tags is None:
            or_tags = []
        filtered_items = []
        for item in self.all_items.values():
            if or_tags:
                if 'tags' in item:
                    for tag in item['tags']:
                        if tag in or_tags:
                            filtered_items.append(item)
                            break
            else:
                filtered_items.append(item)
        return filtered_items

    # Could use __getitem__ instead, depending on the implementation of the Item-class
    def get(self, name=None, index=None):
        """
        Returns an item by name or index. At least one of the inputs is required
        :param name: item name
        :param index: league defined id
        :return:
        """
        it = None
        if name is not None:
            it = [i for i in self.all_items.values() if i['name'] == name][0]
        elif index is not None:
            it = self.all_items[str(index)]
        return it


class ChampionGenerator:
    def __init__(self, filename):
        self.all_champions = json.load(open(filename,'r'))['data']

    def stats_for_champion(self, name):
        return self.all_champions[name]['stats']

    def all_data_for_champion(self, name):
        return self.all_champions[name]

    def create_champion(self, name):
        if name=='Lucian':
            return Lucian(self.all_champions[name])
        else:
            return rgot.champion.Champion(self.all_champions[name])