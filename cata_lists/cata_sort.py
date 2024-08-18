
'''sort by large catagory '''

import pandas as pd
import regex as re

from accessory import accessory_list
from board_game import board_game_list
from food import food_list
from paint_supplies import paint_supplies_list
from rpg import rpg_list
from table_minis import table_minis_list
from tcg import tcg_list
from unknown import unknown_list


df = pd.read_csv('prepared_store_data.csv')

df.drop(columns = ['id','cart','discount'], inplace = True)
master_list = [col for col in df.columns]

print('***************************************************')
print()
print('***************************************************')
print()
print('***************************************************')
print()
print('***************************************************')
print()
print('***************************************************')
print()
print('***************************************************')
print()
print('***************************************************')
print()

print("Master List Count:", len(master_list))


ledger = [accessory_list,
          board_game_list,
          food_list,
          paint_supplies_list,
          rpg_list,
          table_minis_list,
          tcg_list,
          unknown_list]

ledger_strings = ['accessory_list',
                    'board_game_list',
                    'food_list',
                    'paint_supplies_list',
                    'rpg_list',
                    'table_minis_list',
                    'tcg_list',
                    'unknown_list']

sorted_list = (accessory_list +
                board_game_list +
                food_list +
                paint_supplies_list +
                rpg_list +
                table_minis_list +
                tcg_list +
                unknown_list)

unsorted_list = [item for item in master_list if item not in sorted_list]

for item in unsorted_list:

    # get acccessories
    if ((re.match(r'.*bag.*', item) or
         re.match(r'.*box.*', item) or 
         re.match(r'.*sleeve.*', item) or
         re.match(r'.*die.*', item) or
         re.match(r'.*dice.*', item) or
         re.match(r'.*mat.*', item) or
         re.match(r'.*tower.*', item) or
         re.match(r'.*pouch.*', item) or
         re.match(r'.*ultrapro.*', item) or
         re.match(r'.*album.*', item) or
         re.match(r'.*binder.*', item) or
         re.match(r'.*pocket.*', item) or
         re.match(r'.*pocket.*', item) or
         re.match(r'.*spindownd.*', item) or
         re.match(r'.*d(?:20|12|10|8|6|4).*', item)) and not re.match(r'.*booster.*', item)):  

        accessory_list.append(item)


    # get board games  
    if (re.match(r'.*fluxx.*', item)):

        board_game_list.append(item)

    # get food
        

    # get paint
    if(re.match(r'^gw', item) or
         re.match(r'.*paint.*', item) or
         re.match(r'.*contrast.*', item) or
         re.match(r'^warpaint', item) or
         re.match(r'^citadelcolour', item) or
         re.match(r'^aps', item) or
         re.match(r'^apw', item) or
         re.match(r'.*base.*', item) or
         re.match(r'^apto', item) or 
         re.match(r'^apbr', item)  or
         re.match(r'.*\d{2}ml$', item)):
        
         paint_supplies_list.append(item)


    # get rpg items
    if(re.match(r'.*dnd.*', item) or
         re.match(r'.*d&d.*', item) or
         re.match(r'.*dungeonsanddragons.*', item) or
         re.match(r'.*dungeons&dragons.*', item) or
         re.match(r'.*pathfinder.*', item) or
         re.match(r'.*rpg.*', item) or
         re.match(r'.*roleplayinggame.*', item)):  

        rpg_list.append(item)


    # get table_top_minis
    if (re.match(r'^000', item) or
        re.match(r'^warhammer', item) or 
        re.match(r'^nolzursmarvelousminiatures', item) or
        re.match(r'.*\d{5}$', item)
        
        ):

        table_minis_list.append(item)


    # get tcg cards
    if (re.match(r'.*booster.*', item) or 
          re.match(r'.*collector.*', item) or  
          re.match(r'.*commander.*', item) or 
          re.match(r'.*bundle.*', item) or
          re.match(r'.*yugioh.*', item) or
          re.match(r'.*yu-gi-oh.*', item) or
          re.match(r'.*digimon.*', item) or
          re.match(r'.*pokemon.*', item) or  
          re.match(r'.*flesh&blood.*', item) or
          re.match(r'.*magic.*', item) or
          re.match(r'.*mtg.*', item) or  
          re.match(r'.*pre-release.*', item) or
          re.match(r'.*prerelease.*', item) or
          re.match(r'.*trainer.*', item)  or
          re.match(r'.*challenger.*', item) or 
          re.match(r'.*draftpack.*', item) or
          re.match(r'.*battletech.*', item)): 

        tcg_list.append(item)


sorted_list = (accessory_list +
                board_game_list +
                food_list +
                paint_supplies_list +
                rpg_list +
                table_minis_list +
                tcg_list +
                unknown_list)

unsorted_list = [item for item in master_list if item not in sorted_list]

unsorted_list.sort()

for num,li in enumerate(ledger):

    print()
    print(ledger_strings[num])
    print()

    li = list(set(li))

    li.sort()

    for item in li:

        print (f"'{item}',")


print()
print('Unsorted_list')
print()

for item in unsorted_list:

    print (f"'{item}',")


print()
print('Unsorted Remaining:', len(unsorted_list))
print()