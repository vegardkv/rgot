import json

__author__ = 'Vegard'

class ItemBaseGenerator:
    def __init__(self, filename):
        self.all_items = json.load(open(filename, 'r'))['data']

    def generate(self, or_tags=None):
        if or_tags is None:
            or_tags = {}
        filtered_items = []
        for item in self.all_items:
            if or_tags:
                for tag in self.all_items['tags']:
                    if tag in or_tags:
                        filtered_items.append(item)
            else:
                filtered_items.append(item)