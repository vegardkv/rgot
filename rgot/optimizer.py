from itertools import combinations_with_replacement
import csv
import json

__author__ = 'Vegard'

MAX_ITEMS = 6

def brute_force_for_itemsets(friendlychampion, enemychampion, itembase, analysis, filters=None):
    """
    Iterates all combinations of items in itembase.
    :param friendlychampion: Champion-instance of self
    :param enemychampion: Champion-instance of target champion
    :param itembase: list of items
    :param analysis: supports autoAttackDPS
    :param filters: supports minNumberOfItems, maxNumberOfItems, minGoldCost, maxGoldCost
    :return:
    """
    global MAX_ITEMS
    if filters is None:
        filters = {}
    minNumberOfItems = 0 if 'minNumberOfItems' not in filters else filters['minNumberOfItems']
    maxNumberOfItems = MAX_ITEMS if 'maxNumberOfItems' not in filters else filters['maxNumberOfItems']
    minGoldCost = 0 if 'minGoldCost' not in filters else filters['minGoldCost']
    maxGoldCost = float('inf') if 'maxGoldCost' not in filters else filters['maxGoldCost']
    output = OptimizerOutput()
    for n_itms in range(minNumberOfItems, maxNumberOfItems+1):
        for item_tuple in combinations_with_replacement(itembase, n_itms):
            if minGoldCost < sum([int(i['gold']['total']) for i in item_tuple]) < maxGoldCost:
                if analysis == 'autoAttackDPS':
                    output.results.append(friendlychampion.calculate_autoattack_dps(target=enemychampion))
                    output.itemsets.append(item_tuple)
    return output


class OptimizerOutput:
    def __init__(self):
        self.itemsets = []
        self.results = []

    def sort_permanently(self, ascending=True):
        self.itemsets = sorted(self.itemsets, key=self.results.__getitem__(), reverse=ascending)
        self.results = sorted(self.results, reverse=ascending)

    def write_to_json_file(self, filename):
        json.dump(self.as_dict(), open(filename, 'w'))

    def write_to_csv_file(self, filename):
        with open(filename, 'r') as outf:
            writer = csv.DictWriter(outf, ['items', 'value'])
            writer.writeheader()
            for i in range(len(self.itemsets)):
                writer.writerow({'items': self.itemsets[i]['name'], 'value': self.results[i]})

    def as_dict(self):
        return {'itemsets': self.itemsets, 'results': self.results}