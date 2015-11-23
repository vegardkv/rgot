import copy
import json

__author__ = 'Vegard'

input_filename = '../data/all_items.json'
output_filename = '../data/all_items_parsed.json'

"""
rFlatArmorPenetrationMod
rFlatPhysicalDamageModPerLevel
rPercentArmorPenetrationMod
rPercentBonusArmorPenetrationMod (egendefinert)
FlatCritChanceMod
FlatCritDamageMod
FlatPhysicalDamageMod
PercentAttackSpeedMod
"""

all_items = json.load(open(input_filename, 'r'))

################### Copy Black Cleaver with stacks ####################
for item in all_items['data'].values():
    if item['name'] == 'The Black Cleaver':
        bc_copy = copy.deepcopy(item)
        bc_copy['id'] = 30711
        bc_copy['name'] = 'The Black Cleaver (full stacks)'
        all_items['data']['30711'] = bc_copy
        break

################### Fill in missing data ##################
for item in all_items['data'].values():
    if item['name'] == 'Infinity Edge':
        item['stats']['FlatCritDamageMod'] = float(item['effect']['Effect1Amount'])
    elif item['name'] == 'Youmuu\'s Ghostblade':
        item['stats']['rFlatArmorPenetrationMod'] = float(item['effect']['Effect2Amount'])
    elif item['name'] == 'Last Whisper':
        item['stats']['rPercentArmorPenetrationMod'] = float(item['effect']['Effect1Amount'])
    elif item['name'] == 'Mortal Reminder':
        item['stats']['rPercentBonusArmorPenetrationMod'] = float(item['effect']['Effect2Amount'])
    elif item['name'] == 'Serrated Dirk':
        item['stats']['rPercentArmorPenetrationMod'] = float(item['effect']['Effect2Amount'])
    elif item['name'] == 'Lord Dominik\'s Regards':
        item['stats']['rPercentBonusArmorPenetrationMod'] = float(item['effect']['Effect1Amount'])
    elif item['name'] == 'The Black Cleaver (full stacks)':
        item['stats']['rPercentArmorReductionMod'] = float(item['effect']['Effect5Amount'])
    elif item['name'] == 'Maw of Malmortius':
        item['stats']['rFlatArmorPenetrationMod'] = 10

json.dump(all_items, open(output_filename, 'w'))