''' Holds code used to visualize data'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import spearmanr
from scipy.stats import chi2_contingency
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN 


def get_desc(df):

    cats = ['accessories', 
            'board_games', 
            'concessions', 
            'modeling_supplies',
            'role_playing_games', 
            'minis_models', 
            'trading_card_games', 
            'game_room_rental',
            'net_sales']

    return df[cats].describe()[1:3]

def cat_appeal(df):

    cats = ['accessories', 
            'board_games', 
            'concessions', 
            'modeling_supplies',
            'role_playing_games', 
            'minis_models', 
            'trading_card_games', 
            'game_room_rental']

    buyers = [round(len(df[df['accessories'] > 0]) / len(df)*100),
              round(len(df[df['board_games'] > 0]) / len(df)*100),
              round(len(df[df['modeling_supplies'] > 0]) / len(df)*100),
              round(len(df[df['role_playing_games'] > 0]) / len(df)*100),
              round(len(df[df['concessions'] > 0]) / len(df)*100),
              round(len(df[df['minis_models'] > 0]) / len(df)*100),
              round(len(df[df['trading_card_games'] > 0]) / len(df)*100),
              round(len(df[df['game_room_rental'] > 0]) / len(df)*100)]
        
    non_buyers = [round(len(df[df['accessories'] == 0]) / len(df)*100),
                  round(len(df[df['board_games'] == 0]) / len(df)*100),
                  round(len(df[df['modeling_supplies'] == 0]) / len(df)*100),
                  round(len(df[df['role_playing_games'] == 0]) / len(df)*100),
                  round(len(df[df['concessions'] == 0]) / len(df)*100),
                  round(len(df[df['minis_models'] == 0]) / len(df)*100),
                  round(len(df[df['trading_card_games'] == 0]) / len(df)*100),
                  round(len(df[df['game_room_rental'] == 0]) / len(df)*100)]

    data = { 'Category':cats,
             'Buyers':buyers,
             'Non_Buyers':non_buyers}

    df_data = pd.DataFrame(data)

    df_data.set_index('Category', inplace=True)

    df_data.plot(kind='bar', figsize=(10, 6), color = ['gold', 'lightgrey'])

    plt.xticks(rotation=40)

    plt.xlabel('')
    plt.ylabel('Percent of Customers Who Purchased from this Category')
    plt.title('Each Category Appeals to a Select Portion of Customers')


    plt.show()


def get_rel(df):

    # get list of categories to examine
    cats = ['accessories', 
            'board_games', 
            'concessions',
            'modeling_supplies', 
            'role_playing_games', 
            'minis_models',
            'trading_card_games']

    bought_cats = []

    # get true/false column for each category for count > 0
    for cat in cats:
        
        bought_cat = f'bought_{cat}'
        
        df[bought_cat] = df[cat] > 0
        
        bought_cats.append(bought_cat)
        
    # get category combinations
    combs = combinations(bought_cats, 2)

    # Get print out fro each singificant relationship
    for comb in combs:
        
        # get categories and make contengency table
        alpha = .05
        cat1 = df[comb[0]]
        cat2 = df[comb[1]]

        ct = pd.crosstab(cat2, cat1)
        
        chi2, p, dof, expected = chi2_contingency(ct)
        
        # if significant relation ship print p value and odds ration
        if p < alpha:

            # get values from crosstab
            true_true = ct.loc[1, 1]
            true_false = ct.loc[1, 0]
            false_false = ct.loc[0, 0]
            false_true = ct.loc[0, 1]

            # calculate odds ratio
            true_ratio = true_true/true_false
            false_ratio = false_true/false_false

            odds_ratio = round(true_ratio/false_ratio,2)
        
        
            # print results     
            print(comb[0], 'and', comb[1])
            print('--------------------------------------------------------')
            print('Chi-Square P-Value:', p)
            print('Odds Ratio:', odds_ratio)
            print()

def get_sales(df):

    cats = ['accessories', 
            'board_games', 
            'concessions',
            'modeling_supplies', 
            'role_playing_games', 
            'minis_models',
            'trading_card_games']

    df_sales = pd.DataFrame({'total' : [df.net_sales.count(),
                                        df.net_sales.mean(),
                                        df.net_sales.std()]})

    for cat in cats:

        bought_cat = f'bought_{cat}'

        df_cat = df[df[bought_cat] == True]

        col = [df_cat.net_sales.count(),
               df_cat.net_sales.mean(),
               df_cat.net_sales.std()]

        df_sales[f'{cat}'] = col

    df_sales.rename(index={0: 'Customers', 1: 'Mean Sales', 2: 'Standard Deviation Sales'}, inplace=True)

    df_sales = df_sales.astype('int')

    return df_sales


def get_major_sales(df):

    cats = ['board_games', 
            'modeling_supplies', 
            'role_playing_games', 
            'minis_models',
            'trading_card_games']

    df_sales = pd.DataFrame({'total' : [df.net_sales.count(),
                                        df.net_sales.mean(),
                                        df.net_sales.std()]})

    for cat in cats:

        bought_cat = f'bought_{cat}'

        df_cat = df[df[bought_cat] == True]

        col = [df_cat.net_sales.count(),
               df_cat.net_sales.mean(),
               df_cat.net_sales.std()]

        df_sales[f'{cat}'] = col

    df_sales.rename(index={0: 'Customers', 1: 'Mean Sales', 2: 'Standard Deviation Sales'}, inplace=True)

    df_sales = df_sales.astype('int')

    return df_sales