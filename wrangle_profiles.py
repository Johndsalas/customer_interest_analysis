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

   #  # set index to date time
   #  df['datetime'] = pd.to_datetime(df.index)
   #  df = df.set_index('datetime')

   df = pd.read_csv('prepared_store_data.csv')

    # get relevent columns
   df = df[['cust_id', 
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

   df = df[df.event_type == 'Payment']
   df = df.drop(columns = 'event_type')

    # revove purchases not tied to an id number
   df = df[df.cust_id != 'unknown']
    
   # group data by id drop column and reset the index
   df = df.groupby('cust_id').agg(sum)
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
                    'all_items']

   to_scale_df = df[cols_to_scale]

   scaler = StandardScaler().fit(to_scale_df)

   scaled_array = scaler.transform(to_scale_df)

   scaled_df = pd.DataFrame(scaled_array, columns = cols_to_scale)

   for col in cols_to_scale:

      scaled_df = scaled_df.rename(columns={col: col + "_scaled"})

   df = df.join(scaled_df)

   return df