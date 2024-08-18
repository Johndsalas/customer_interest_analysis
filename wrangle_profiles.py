''' holds wrangle code for customer profiles'''

# Imports

# python libraries
import pandas as pd
import regex as re
import numpy as np
import matplotlib.pyplot as plt



import wrangle as w


# ignore warnings
import warnings
warnings.filterwarnings("ignore")


def wrangle_profiles():

    # aquire and prepare data
    
    df = w.get_prepared_data()

    # set index to datetime
    df = w.set_datetime_as_index(df)

    # get item counts by caregory
    df = get_category_counts(df)

    df = df.groupby('id').agg(sum)

    return df

def get_category_counts(df):

    # seperate item counts by category into differint dataframes
    df_acc = df[a.accessory_list]
    df_bg = df[b.board_game_list]
    df_f = df[f.food_list]
    df_ps = df[p.paint_supplies_list]
    df_rpg = df[r.rpg_list]
    df_tm = df[m.table_minis_list]
    df_tcg = df[t.tcg_list]

    # get total counts for each category by summing across each row
    df_acc['accessories'] = df_acc.sum(axis=1)
    df_bg['board_games'] = df_bg.sum(axis=1)
    df_f['concessions'] = df_f.sum(axis=1)
    df_ps['modeling_supplies'] = df_ps.sum(axis=1)
    df_rpg['role_playing_games'] = df_rpg.sum(axis=1)
    df_tm['minis_models'] = df_tm.sum(axis=1)
    df_tcg['trading_card_games'] = df_tcg.sum(axis=1)

    # drop all other rows
    df_acc = df_acc[['accessories']]
    df_bg = df_bg[['board_games']]
    df_f = df_f[['concessions']]
    df_ps = df_ps[['modeling_supplies']]
    df_rpg = df_rpg[['role_playing_games']]
    df_tm = df_tm[['minis_models']]
    df_tcg = df_tcg[['trading_card_games']]

    # get id and net_sales from original dataframe

    df = df[['id','net_sales']]

    # merge summed rows onto dataframe

    df_list = [df_acc, df_bg, df_f, df_ps, df_rpg, df_tm, df_tcg]

    for new_df in df_list:
        
        df = df.merge(new_df, right_index = True, left_index = True)

    return df


