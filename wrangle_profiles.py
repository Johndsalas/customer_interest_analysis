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
            'other',
            'game_room_rental', 
            'all_items',
            'net_sales']]

   # fill null values
   df = df[df.event_type == 'Payment']
   df = df.drop(columns = 'event_type')

   # remove purchases not tied to an id number
   df = df[df.cust_id != 'unknown']

   # calculate tenure based on earliest and latest transaction date
   df['start_date'] = df.cust_id.apply(get_start_date)
   df['last_date'] = df.cust_id.apply(get_last_date)

   df['tenure'] = df['last_date'].dt.to_period('M').astype(int) - df['start_date'].dt.to_period('M').astype(int)

   df.drop(columns = ['start_date', 'last_date'])

   # add column to count number of transactions
   df['trans_count'] = 1 

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
                                 'other' : 'sum',
                                 'game_room_rental' : 'sum', 
                                 'all_items' : 'sum',
                                 'net_sales' : 'sum',
                                 'trans_count' : 'sum',
                                 'tenure' : 'max'})

   df = df.reset_index()
   df = df.drop(columns = ['cust_id'])

   # scale catagory columns
   cols_to_scale = ['accessories', 
                    'board_games', 
                    'concessions', 
                    'modeling_supplies',
                    'role_playing_games', 
                    'minis_models', 
                    'trading_card_games', 
                    'other',
                    'game_room_rental', 
                    'all_items',
                    'trans_count',
                    'tenure']

   to_scale_df = df[cols_to_scale]

   scaler = StandardScaler().fit(to_scale_df)

   scaled_array = scaler.transform(to_scale_df)

   scaled_df = pd.DataFrame(scaled_array, columns = cols_to_scale)

   for col in cols_to_scale:

      scaled_df = scaled_df.rename(columns={col: col + "_scaled"})

   df = df.join(scaled_df)

   return df