''' holds wrangle code for customer profiles'''

# Imports
import pandas as pd
from sklearn.preprocessing import StandardScaler

def get_profiles_data(df):
    '''Takes in dataframe of store data after general preparation
       Returns df of store data prepared for profiles project'''

    # set index to date time
    df['datetime'] = pd.to_datetime(df.index)
    df = df.set_index('datetime')

    # get relevent columns
    df = df[['id', 
       'accessories',
       'board_games', 
       'concessions', 
       'modeling_supplies', 
       'role_playing_games',
       'minis_models', 
       'trading_card_games',
       'net_sales']]

    # restrict data to data from 2023
    df = df.loc['2023']

    # revove purchases not tied to an id number
    df = df[df.id != 'unregistered']
    df = df[df.id != ' ']

    # group data by id drop column and reset the index
    cata_df = df.groupby('id').agg(sum)
    df = df.reset_index()
    df = df.drop(columns = ['id', 'datetime'])


    # scale catagory columns
    cols_to_scale = ['accessories',
                    'board_games', 
                    'concessions', 
                    'modeling_supplies', 
                    'role_playing_games',
                    'minis_models', 
                    'trading_card_games']

    to_scale_df = df[cols_to_scale]

    scaler = StandardScaler().fit(to_scale_df)
    
    scaled_array = scaler.transform(to_scale_df)

    scaled_df = pd.DataFrame(scaled_array, columns = cols_to_scale)

    for col in cols_to_scale:
    
        scaled_df = scaled_df.rename(columns={col: col + "_scaled"})
    
    df = df.join(scaled_df)

    return df
