''' Holds code used to explore and visualize project data'''

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
    ''' Get abriged discribe table'''

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
    ''' Get chart of category buying habbits'''

    cats = ['accessories', 
            'board_games', 
            'concessions', 
            'modeling_supplies',
            'role_playing_games', 
            'minis_models', 
            'trading_card_games', 
            'game_room_rental']

    # buyer and non-buyer percentages 
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

    # create dataframe
    data = { 'Category':cats,
             'Buyers':buyers,
             'Non_Buyers':non_buyers}

    df_data = pd.DataFrame(data)

    df_data.set_index('Category', inplace=True)

    # get dataframe from chart
    df_data.plot(kind='bar', figsize=(10, 6), color = ['gold', 'lightgrey'])

    plt.xticks(rotation=40)

    plt.xlabel('')
    plt.ylabel('Percent of Customers Who Purchased from this Category')
    plt.title('Each Category Appeals to a Select Portion of Customers')


    plt.show()


def get_rel(df):
    ''' Takes in a dataframe
        Prints the results of chi-square test and odds ratio for every combination of category listed in function
        Only prints results if p-value from chi-square test is below .05'''

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
    ''' Prints table for customer groups
        Shows count of group and the mean and standard deviation for net sales'''


    cats = ['accessories', 
            'board_games', 
            'concessions',
            'modeling_supplies', 
            'role_playing_games', 
            'minis_models',
            'trading_card_games']

    # get datafram with column for all customers
    df_sales = pd.DataFrame({'all_customers' : [df.net_sales.count(),
                                                df.net_sales.mean(),
                                                df.net_sales.std()]})

    # for each category
    for cat in cats:

        # get a dataframe with only customers from that group
        bought_cat = f'bought_{cat}'

        df_cat = df[df[bought_cat] == True]

        # add a column with count, mean, and std for this group
        col = [df_cat.net_sales.count(),
               df_cat.net_sales.mean(),
               df_cat.net_sales.std()]

        df_sales[f'{cat}'] = col

    # rename index with row names 
    df_sales.rename(index={0: 'Customers', 1: 'Mean Sales', 2: 'Standard Deviation Sales'}, inplace=True)

    # cast df as int type
    df_sales = df_sales.astype('int')

    return df_sales


def get_major_sales(df):
    ''' Prints table for major interest customer groups
        Shows count of group and the mean and standard deviation for net sales'''

    cats = ['board_games', 
            'modeling_supplies', 
            'role_playing_games', 
            'minis_models',
            'trading_card_games']

     # get datafram with column for all customers
    df_sales = pd.DataFrame({'all_customers' : [df.net_sales.count(),
                                                df.net_sales.mean(),
                                                df.net_sales.std()]})

    # for each category
    for cat in cats:

        # get a dataframe with only customers from that group
        bought_cat = f'bought_{cat}'

        df_cat = df[df[bought_cat] == True]

        # add a column with count, mean, and std for this group
        col = [df_cat.net_sales.count(),
               df_cat.net_sales.mean(),
               df_cat.net_sales.std()]

        df_sales[f'{cat}'] = col

    # rename index with row names 
    df_sales.rename(index={0: 'Customers', 1: 'Mean Sales', 2: 'Standard Deviation Sales'}, inplace=True)

    # cast df as int type
    df_sales = df_sales.astype('int')

    return df_sales

def get_sales_dist(df):
    '''Get boxplot of Net Sales'''

    plt.boxplot(df.net_sales)
    plt.title("Overall Net Sales Contain Many Outliers")
    plt.show()


def get_high_mod_sales(df):
    '''Takes in a dataframe 
       returns two datafromes split into high and moderate spending groups using IQR rule'''

    # get quantiles and calculatre IQR and upper limit
    q1 = df.net_sales.quantile(.25)
    q3 = df.net_sales.quantile(.75)

    iqr = q3 - q1

    upper = q3 + (1.5 * iqr)

    # split dataframe at upper limit
    df_mod = df[(df.net_sales <= upper)]
    df_high = df[(df.net_sales > upper)]

    return df_mod, df_high


def get_grouped_sales_dists(df_mod, df_high):
    '''Takes in a dataframe for moderate and high spending customers
       shows side by side box plots of net sales distributions for each'''
    # Create subplots
    fig, axs = plt.subplots(1, 2) 

    # Plot the first box plot
    df_mod.boxplot(column='net_sales', ax=axs[0])
    axs[0].set_title('Moderate Spenders')

    # Plot the second box plot
    df_high.boxplot(column='net_sales', ax=axs[1])
    axs[1].set_title('High Spenders')

    plt.tight_layout() 
    plt.show()


def get_spending_effecs(df, df_mod, df_high):
    ''' Takes in full dataframe and two sub dataframes containing a split of the data 
        prints message showing the percent of customers in each group and each groups percent of net sales'''

    # get counts of groups
    mod_count = len(df_mod)
    high_count = len(df_high)
    all_count = len(df)

    # get means of high and mod group
    mod_mean_sales = df_mod.mean()
    high_mean_sales = df_high.mean()

    # calculate percent of customers for both groups
    mod_pcust = round(mod_count / all_count, 2) * 100
    high_pcust = round(high_count / all_count, 2) * 100

    # get total sales for full df and both groups
    tot_sales = df.net_sales.sum()
    mod_sales = df_mod.net_sales.sum()
    high_sales = df_high.net_sales.sum()
    
    # calculate percent of sales for each group
    mod_psales = round(mod_sales / tot_sales, 2) * 100
    high_psales = round(high_sales / tot_sales, 2) * 100

    # print message
    print(f'Moderate Spenders represent {mod_pcust}% of total customers and {mod_psales}% of total net sales')
    print(f'High Spenders represent {high_pcust}% of total customers and {high_psales}% of total net sales')