'''Aquire and prepare data for analysis'''

import pandas as pd
import regex as re

import os

# created files
import cata_lists.accessories as a
import cata_lists.board_games as b
import cata_lists.concessions as c
import cata_lists.paint_supplies as p
import cata_lists.rpg as r
import cata_lists.table_minis as m
import cata_lists.tcg as t
import cata_lists.other as o

def get_prepared_data():
    '''Check local file for prepared data
       if not found prepare data using csv files in local file
       Return prepared data'''

    if os.path.exists('prepared_store_data.csv'):

        df = pd.read_csv('prepared_store_data.csv')

    else:

        df = wrangle_data()

        df.to_csv('prepared_store_data.csv', index_label=False)

    return df


def wrangle_data():
    '''Prepare data for analysis using data from local csv files'''

    #Aquire and merge data from local csv files
    df = aquire()

    #Removes non-payment rows and drops payment column
    df = remove_non_payments(df)

    #Add columns indicating year, month, day, and weekend
    #Add datetime column and set as the index
    df = get_datetime_groupings(df)

    # rename relevent columns and drop the others
    df = get_relevent_columns(df)

    #Convert net_sales to float
    #Clean id column
    df = clean_rows(df)
    
    #fill nans in id and discount columns
    df = get_filled_nan(df)
    
    # convert values in cart from string to list
    df['cart'] = df.cart.apply(get_values_as_list)

    # get master list of products
    master_list = get_master_list(df)

    # get a column for each item in master list containing the number of times that item was bought
    df = get_item_counts(df, master_list)

    # get a catagorie for each type of item showing the number of that type that was bought 
    df = get_major_groupings(df, master_list)

    return df


def aquire():
    '''Aquire and merge data from local csv files'''

    # read in yearly dataframes 
    df_2021 = pd.read_csv('raw_data/2021-2022.csv').sort_values('Date')
    df_2022 = pd.read_csv('raw_data/2022-2023.csv').sort_values('Date')
    df_2023 = pd.read_csv('raw_data/2023-2024.csv').sort_values('Date')

    # concat yearly dataframes
    df = pd.concat([df_2021, df_2022, df_2023]).sort_values('Date')

    return df


def remove_non_payments(df):
    '''Remove non-payment rows and drops payment column'''
    
    df = df[df.event == 'Payment']

    df = df.drop(columns=['event'])
    
    return df


def get_datetime_groupings(df):
    ''' Takes in a dataframe with a date and tiem column
        Add columns indicating year, month, day, and weekend
        Add datetime column and set as the index
        Returns dataframe'''

    # ceate datetime column and set index to datetime
    df['datetime'] = df.Date + ' ' + df.Time
    df['datetime'] = pd.to_datetime(df['datetime'])

    # get date group coulmns
    df['year'] = df.datetime.dt.year
    df['month'] = df.datetime.dt.month
    df['day'] = df.datetime.dt.day
    df['weekday'] = df.datetime.dt.day_name()  

    df = df.set_index('datetime').sort_index()

    return df


def get_relevent_columns(df):
    '''Dropps unused columns 
       renames used columns for ease of use'''

    # restrict to relevent columns and rename for ease of use
    df = df[['Customer ID', 
             'Description', 
             'Event Type', 
             'Discount Name',
             'Gross Sales',
             'Discounts',
             'Net Sales', 
             'year', 
             'month', 
             'day', 
             'weekday']]


    df = df.rename(columns={'Description' : 'cart', 
                            'Event Type' : 'event', 
                            'Customer ID' : 'id',
                            'Discount Name' : 'discount',
                            'Gross Sales' : 'gross_sales',
                            'Discounts' : 'discount_amount',
                            'Net Sales' : 'net_sales'})
    
    return df


def clean_rows(df):
    ''' Convert net_sales to float
        Clean id column'''
    
    df['net_sales'] = df['net_sales'].str.replace('$', '').astype(float)

    df['id'] = df['id'].str.replace(',', '')

    return df


def get_values_as_list(values):
    '''Cleans text and get list of items in cart column value'''

    values = str(values)
    values = (values.lower()
                    .replace('(regular)', '')
                    .replace('  - too much caffeine', '')
                    .replace('  - carbonated beverage', '')
                    .replace("'", "")
                    .replace('"', ''))
    
    values = values.split(',')

    values = [value.strip() for value in values]
    
    values = [re.sub(r'\s+', '_', value) for value in values]
    
    return values


def get_filled_nan(df):
    '''fill nans in id and discount columns'''
    
    df['id'] = df.id.fillna('unregistered')
    
    df['discount'] = df.discount.fillna('no_discount')
    
    return df


def get_number_bought(value):
    '''returns number of items bought in cart column'''
    
    total_bought = 0
    
    # for each item in the list
    for item in value:
        
        # look for the number of times it was bought
        num_bought = re.match(r"^(\d+)_x_",item)
        
        # if found add that number to total
        if num_bought != None:
            
            total_bought += int(num_bought.group(1))
            
        # otherwise add 1 to total
        else:
            
            total_bought += 1
        
    return total_bought


def get_master_list(df):
    '''Get list of each product contained in carts lists'''

    # get list of carts in cart column
    li = df.cart.to_list()

    master_list = []

    # for each item in each cart remove number bought indicator and add it to master list
    for cart in li:
        for item in cart:

            master_list.append(re.sub(r"^(\d+_x_)", '', item))

    # remove duplicates and sort list
    master_list = list(set(master_list))

    master_list.sort()

    return master_list


def get_item_counts(df, master_list):
    '''Create a column for each item in master list showing the number of matching items in each list'''

    for item in master_list:
        
        df[f'{item}'] = df['cart'].apply(get_matching_item_count, args=(item,))
        
    return df


def get_matching_item_count(value_list, item):
    '''Return number of items indicated by cart column that match the chosen item'''

    total_item_bought = 0
   
    # for each value in the value list
    for value in value_list:

        # if the item equals the value with the ammount code removed
        if item == re.sub(r"^(\d+_x_)", '' , value):
            
            # locate the amount code 
            num_item_bought = re.match(r"^(\d+)_x_",value)
        
            # if the amount code is present add amount to total 
            if num_item_bought != None:

                total_item_bought += int(num_item_bought.group(1))

            # If amount code is not present add one to total
            else:
            
                total_item_bought += 1

    return total_item_bought


def get_major_groupings(df, master_list):

    # seperate item counts by category into differint dataframes
    df_acc = df[a.accessory_list]
    df_bg = df[b.board_game_list]
    df_con = df[c.concessions_list]
    df_ps = df[p.paint_supplies_list]
    df_rpg = df[r.rpg_list]
    df_tm = df[m.table_minis_list]
    df_tcg = df[t.tcg_list]
    df_other = df[o.other_list]
    df_master = df[master_list]

    # get total counts for each category by summing across each row
    df_acc['accessories'] = df_acc.sum(axis=1)
    df_bg['board_games'] = df_bg.sum(axis=1)
    df_con['concessions'] = df_con.sum(axis=1)
    df_ps['modeling_supplies'] = df_ps.sum(axis=1)
    df_rpg['role_playing_games'] = df_rpg.sum(axis=1)
    df_tm['minis_models'] = df_tm.sum(axis=1)
    df_tcg['trading_card_games'] = df_tcg.sum(axis=1)
    df_other['other'] = df_other.sum(axis=1)
    df_master['all_items'] = df_master.sum(axis=1)

    # drop all other rows
    df_acc = df_acc[['accessories']]
    df_bg = df_bg[['board_games']]
    df_con = df_con[['concessions']]
    df_ps = df_ps[['modeling_supplies']]
    df_rpg = df_rpg[['role_playing_games']]
    df_tm = df_tm[['minis_models']]
    df_tcg = df_tcg[['trading_card_games']]
    df_other = df_other[['other']] 
    df_master = df_master[['all_items']]   

    # merge group counts to original dataframe
    df_list = [df_acc, df_bg, df_con, df_ps, df_rpg, df_tm, df_tcg, df_other, df_master]

    for new_df in df_list:
        
        df = df.merge(new_df, right_index = True, left_index = True)

    return df


