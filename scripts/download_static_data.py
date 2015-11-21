import json
import requests

__author__ = 'Vegard'

champs_filename = '../data/all_champions.json'
items_filename = '../data/all_items.json'

with open('../api_key.txt', 'r') as fin:
    api_key = fin.read()

champion_url ='https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?champData=all&api_key=' + api_key
item_url ='https://global.api.pvp.net/api/lol/static-data/euw/v1.2/item?itemListData=all&api_key=' + api_key

champions = requests.get(champion_url).json()
json.dump(champions, open(champs_filename, 'w'))

items = requests.get(item_url).json()
json.dump(items, open(items_filename, 'w'))