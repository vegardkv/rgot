from itertools import combinations_with_replacement
import csv
import json

__author__ = 'Vegard'

MAX_ITEMS = 6

def brute_force_for_itemsets(friendlychampion, enemychampion, itembase, analysis, filters=None, **kwargs):
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
    minGoldCost = -1 if 'minGoldCost' not in filters else filters['minGoldCost']
    maxGoldCost = float('inf') if 'maxGoldCost' not in filters else filters['maxGoldCost']
    output = OptimizerOutput()
    counter = 0
    for n_itms in range(minNumberOfItems, maxNumberOfItems+1):
        print('Computing combinations of %i items' % n_itms)
        for item_tuple in combinations_with_replacement(itembase, n_itms):
            friendlychampion.items = list(item_tuple)
            if minGoldCost < sum([int(i['gold']['total']) for i in item_tuple]) < maxGoldCost:
                if analysis == 'autoAttackDPS':
                    output.results.append(friendlychampion.calculate_autoattack_dps(target=enemychampion))
                    output.itemsets.append(item_tuple)
                elif analysis == 'spellRotation' and 'rotation' in kwargs and 'skillLevels' in kwargs:
                    output.results.append(friendlychampion.calculate_rotation(kwargs['rotation'], kwargs['skillLevels']))
                    output.itemsets.append(item_tuple)
                else:
                    raise NotImplementedError('Analysis named %s not implemented' % analysis)
            if not counter % 100:
                print(counter)
            counter += 1
            if len(item_tuple)==1:
                print(item_tuple[0]['name'])
    return output


class OptimizerOutput:
    def __init__(self):
        self.itemsets = []
        self.results = []

    def sort_permanently(self, ascending=True):
        new_order = sorted(range(len(self.results)), key=self.results.__getitem__)
        self.itemsets = [self.itemsets[i] for i in new_order]
        self.results = [self.results[i] for i in new_order]

    def write_to_json_file(self, filename):
        json.dump(self.as_dict(), open(filename, 'w'))

    def write_to_csv_file(self, filename):
        with open(filename, 'w') as outf:
            writer = csv.DictWriter(outf, ['items', 'value'], lineterminator='\n')
            writer.writeheader()
            for i in range(len(self.itemsets)):
                writer.writerow({'items': ','.join([ii['name'] for ii in self.itemsets[i]]), 'value': sum(self.results[i])})

    def as_dict(self):
        return {'itemsets': self.itemsets, 'results': self.results}