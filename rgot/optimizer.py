__author__ = 'Vegard'

def brute_force_for_itemsets(friendlychampion, enemychampion, itembase, analysis, filters=None):
    # generate combinations of all baseitems (up to 6)
    # for each itemset, compute output according to analysis
    # return OptimizerOutput
    return


class OptimizerOutput:
    def __init__(self):
        self.itemsets = []
        self.results = []

    def sort(self, ascending=True):
        pass

    def write_to_json_file(self, filename):
        pass

    def write_to_csv_file(self, filename):
        pass

    def as_dict(self):
        return {'itemsets': self.itemsets, 'results': self.results}