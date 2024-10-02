''' holds wrangle code for customer profiles'''

# Imports
import pandas as pd
from sklearn.preprocessing import StandardScaler

import os

def get_prepared_profiles_data():
    '''Check local file for prepared data
       if not found prepare data using csv files in local file
       Return prepared data'''

    if os.path.exists('prepared_profile_data.csv'):

       df = pd.read_csv('prepared_profile_data.csv')

    else:

        df = get_profiles_data()

        df.to_csv('prepared_profile_data.csv', index_label=False)

    return df

def get_profiles_data():
   '''Takes in dataframe of store data after general preparation
      Returns df of store data prepared for profiles project'''

   # read in store data
   df = pd.read_csv('prepared_store_data.csv')

   # get relevent columns
   df = df[['year',
            'cust_id', 
            'event_type',
            'accessories', 
            'board_games', 
            'concessions', 
            'modeling_supplies',
            'role_playing_games', 
            'minis_models', 
            'trading_card_games', 
            'game_room_rental',
            'net_sales']]

   # fill null values
   df = df[df.event_type == 'Payment']
   df = df.drop(columns = 'event_type')

   # remove purchases not tied to an id number
   df = df[df.cust_id != 'unknown']

   # restrict data to 2023
   df = df[df.year == 2023]

   df = df.drop(columns = 'year')

   # group data by id drop column and reset the index
   df = df.groupby('cust_id').agg({'accessories' : 'sum', 
                                   'board_games' : 'sum', 
                                   'concessions' : 'sum', 
                                   'modeling_supplies' : 'sum',
                                   'role_playing_games' : 'sum', 
                                   'minis_models' : 'sum', 
                                   'trading_card_games' : 'sum', 
                                   'game_room_rental' : 'sum', 
                                   'net_sales' : 'sum'})

   df = df.reset_index()
   df = df.drop(columns = ['cust_id'])

   return df