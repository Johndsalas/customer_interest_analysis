''' File containing helper functions for netrunner_agendas_and_accesses notebook '''

# imports
import pandas as pd
import regex as re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def get_my_data():
    '''
        read in agenda matrix data
        return full dataframe 
        and two subset dataframes separating 
        normal and let them dream agenda types 
    '''


    # read in data
    df = pd.read_excel('agenda_matrix.xlsx')

    # exclude let them dream type builds where no replacements occured
    df = df[~((df.agenda_type == 'Let Them Dream') & (df.let_them_dream_count == 0))]

    # rename columns for ease of understanding
    df = df.rename(columns={'old_col2' : 'new_col2',
                            'let_them_dream_count' : 'ltd_count',
                            'average_accesses' : 'access_threshold',
                            'num_agendas' : 'agenda_count'})
    
    # add seperate columns for count of one, two, and three point agendas 
    df['three_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search('\[(\d+),', x).group(1)))
    df['two_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search(', (\d+),', x).group(1)))
    df['one_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search(', (\d+)\]', x).group(1)))

    # data validation
    # add column calculating agenda point total 
    df['calc_agenda_points'] = (df['three_point_agendas'] * 3) + (df['two_point_agendas'] * 2) + (df['one_point_agendas']) + (df['ltd_count'])

    # check that calculated agenda point total matches assigned agenda point total
    # if yes drop redundant columns
    # if no raise exception
    if (df.agenda_points == df.calc_agenda_points).all():

        df.drop(columns = ['agenda_counts', 'agenda_points', 'calc_agenda_points'])
        
    else:
        
        raise Exception("Agenda Point Mismatch!!!")
    
    # add agenda density column round to 5 decimals for color mapping
    df['agenda_density'] = round(df['agenda_points'] / df['deck_size'], 6)
    
    # split data into normal and Let Them Dream data sets
    df_normal = df[df.agenda_type == 'Normal']
    df_ltd = df[df.agenda_type == 'Let Them Dream']

    return df, df_normal, df_ltd


def get_my_thresholds(df_normal, df_ltd):
    '''
        Plots and displays count of possible builds by access threshold
    '''

    # set framework for charts
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)

    # set colors for right chart
    colors1 = { '14' :   'skyblue',
                '15' : '#779ECB',
                '16' : '#779ECB',
                '17' : '#779ECB',
                '18' :   'skyblue',
                '19' :   'skyblue',}
    
    # plot right chart
    sns.countplot(x='access_threshold', data=df_normal, ax=ax1, palette=colors1)
    ax1.set_title('Normal Agendas')
    ax1.set(xlabel='', ylabel='')

    # set colors for left chart
    colors2 = { '15' :   'skyblue',
                '16' :   'skyblue',
                '17' : '#779ECB',
                '18' : '#779ECB',
                '19' : '#779ECB',
                '20' : '#779ECB',}

    # plot right chart
    sns.countplot(x='access_threshold', data=df_ltd, ax=ax2, palette=colors2)
    ax2.set_title('Let Them Dream')
    ax2.set(xlabel='', ylabel='')

    # set super title and labels
    fig.suptitle('Strong Contrast Between Common and Uncommon Access Threshold Values', fontweight='bold')
    fig.supxlabel('Access Threshold')
    fig.supylabel('Count of Distinct Builds')

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_my_density_chart(df):
    '''
        Plots and disploys agenda density chart using dataframe
    '''

    # label clusters by color
    colors = {
                0.407407 : '#E09ECB',
                0.408163 : '#E09ECB',
                0.409091 : '#E09ECB',   
        
                0.425926 : '#E69A39',   
                0.428571 : '#E69A39',   
                0.431818 : '#E69A39',   
        
                0.440000 : '#E6BC53',   
        
                0.444444 : '#54D29C',   
                0.450000 : '#54D29C',   
        
                0.460000 : '#4AAAD1',   
        
                0.466667 : '#D99BFF',   
        
                0.475000 : '#2D3142'
            }

    # plot chart
    sns.scatterplot(data=df, x='agenda_density', y='access_threshold', hue='agenda_density', palette=colors)
    
    plt.title('Agenda Density Sets a Range of 3-4 Values for Access Threshold', fontweight='bold')

    plt.xlabel("Agenda Density")
    plt.ylabel("Access Threshold")

    # remove legend
    plt.legend([], [], frameon=False)

    plt.show()


def get_min_deck_chart(df):
    '''
        Plots and displays scatterplot of possible access thresholds at each minimum deck size
    '''

    # Get rows using minimum deck size
    df_min = df[df.deck_size.isin([40, 45, 50])]

    # plot chart
    df_min.plot.scatter(x='deck_size', y='access_threshold',figsize=(4, 5), color='#779ECB')
    plt.title('Minimum Deck Size Caps Maximum Access Threshold at 18', fontweight='bold', pad=15)
    
    # set ticks and tick limits
    plt.xticks([40, 45, 50])
    plt.xlim(37.5, 52.5)

    plt.yticks(range(14, 20)) 
    plt.ylim(13, 19.5)  

    # set labels
    plt.xlabel("Deck Size")
    plt.ylabel("Access Threshold")

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_margin_chart(df):
    '''
        Plots and displays charts comparing possible access thresholds at each minimum deck size with decks that use the four card margin
    '''


    # get dataframes containing the correct card count
    df_small = df[df['deck_size'].between(40,44)]
    df_mid = df[df.deck_size.between(45,49)]
    df_lg = df[df.deck_size.between(50,54)]

    # set framework for charts
    fig, axes = plt.subplots(ncols=3, figsize=(6,5), constrained_layout=True, sharey=True)

    # plot first chart
    df_small.plot.scatter(x='deck_size', y='access_threshold', title='40-44', xlabel='', ylabel='', color='#779ECB', ax=axes[0])
    axes[0].set_xticks([40, 44])
    axes[0].set_xlim(39, 45)
    axes[0].set_ylim(13, 21)
    axes[0].set_yticks(range(14, 21))

    # plot second chart
    df_mid.plot.scatter(x='deck_size', y='access_threshold', title='45-49', xlabel='', ylabel='', color='#779ECB', ax=axes[1])
    axes[1].set_xticks([45, 49])
    axes[1].set_xlim(44, 50)

    # plot third chart
    df_lg.plot.scatter(x='deck_size', y='access_threshold', title='50-54', xlabel='', ylabel='', color='#779ECB', ax=axes[2])
    axes[2].set_xticks([50, 54])
    axes[2].set_xlim(49, 55)

    # set super labels and title
    fig.suptitle('Range of Access Thresholds Shift Up When Using the 4 Card Margin', fontweight='bold')

    fig.supxlabel('Deck Size')
    fig.supylabel('Access Threshold')

    fig.align_ylabels()

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_my_min_agenda_chart(df):
    '''
        Plots and displays charts comparing possible access thresholds at each deck size using the minimum agenda point total 
        and those adding an extra agenda point
    '''

    # set plot framework
    fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(10,4), sharey=True)

    # set counter to adjust xlim to the correct agenda point values
    xlim = 0

    # list of deck values to filter through
    values = [40,44,45,49,50,54]
        
    for i in range(0,6):

        # get sub dataframe filtering for i value in values list
        sub = df[df['deck_size'] == values[i]]

        # generate subplot
        sub.plot.scatter(x='agenda_points', 
                         y='access_threshold', 
                         ax=axes[i], 
                         marker='o',
                         s=20,
                         color='#779ECB',
                         title=f"{'Deck Size'} {values[i]}")

        # set xticks and margins
        #axes[i].xaxis.set_major_locator(MaxNLocator(integer=True))
            
        # getting max and nim values for subplot
        sub_x_min = int(sub['agenda_points'].min())
        sub_x_max = int(sub['agenda_points'].max())
            
        # Add symmetric padding (1 unit) to the left and right sides
        padding = .5
        
        # Apply the balanced limits directly to this specific axis object
        axes[i].set_xlim(sub_x_min - padding, sub_x_max + padding)

        # set ylimits
        plt.ylim(13.5, 20.5)

        axes[i].set(xlabel='', ylabel='')

    # set super labels and title
    fig.suptitle('Range of Access Thresholds Shift Down When an Extra Agenda Point is Included', fontweight='bold')
    fig.supxlabel('Agenda Points')
    fig.supylabel('Access Threshold')

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_my_agenda_count_chart(df):
    '''
        Displays chart of possible access thresholds at each agenda count
    '''

    # label clusters in different colors
    colors = {
                6  : '#E05A47',
        
                7  : '#E59738',
        
                8  : '#56B4E9',
        
                9  : '#009E73', 
                10 : '#009E73', 
                11 : '#009E73',

                12 : '#CC79A7', 
                13 : '#CC79A7',
                14 : '#CC79A7',

                15 : '#F0E442',
                16 : '#F0E442',
                17 : '#F0E442',

                18 : '#5A4FCF',

                19 : '#5C6B73'
            }

    # plot chart
    sns.scatterplot(data=df,
                    x='agenda_count', 
                    y='access_threshold',
                    hue='agenda_count',
                    palette=colors)
    
    # add title, labels, and remove legend
    plt.title('Number of Agendas Set a Range of 2-4 Values for Access Threshold', fontweight='bold')

    plt.xlabel('Agenda Count')
    plt.ylabel('Access Threshold')

    plt.legend([], [], frameon=False)

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_my_threes_chart(df):
    '''
    Plots and displays chart of possible access thresholds by number of one-point agendas
    '''

    # plot chart 
    df.plot.scatter(x='three_point_agendas', 
                    y='access_threshold', 
                    color='#779ECB',
                    title='Count of Three-Point Agendas Has a Small Positive Effect on Access Threshold')
    
    # set title and labels
    plt.title('Three-Point Agenda Count has a Small Positive Relationship with Access Threshold', fontweight='bold')
    plt.xlabel('Three-Point Agenda Count')
    plt.ylabel('Access Threshold')


def get_my_first_outlier_df(df):
    '''
    Displays dataframe of outliers for three-point agendas
    '''

    # get desired data
    df_example = df[(df.access_threshold == 18) & (df.three_point_agendas == 0)]

    df_example = df_example[['deck_size',
                             'agenda_points',
                             'one_point_agendas',
                             'two_point_agendas',
                             'three_point_agendas',
                             'access_threshold']]
    
    return df_example


def get_my_ones_chart(df):
    '''
    Plots and displays chart of possible access threholds by number of one-point agendas
    '''

    # label cluster in red other in blue
    colors = {
                    19 : '#E05A47',
                    18 : '#E05A47',

                    17 : '#779ECB',
                    16 : '#779ECB',
                    15 : '#779ECB',
                    14 : '#779ECB'

             }

    # plot chart
    sns.scatterplot(data=df,
                    x='one_point_agendas', 
                    y='access_threshold',
                    hue = 'access_threshold',
                    palette=colors)

    # set title, labels, and remove legend
    plt.title('Builds with more than 2 One-Point Agendas Cap Access Threshold at 17', fontweight='bold')

    plt.xlabel('One-Point Agenda Count')
    plt.ylabel('Access Threshold')

    plt.legend([], [], frameon=False)

    # make pretty and display
    plt.tight_layout()
    plt.show()


def get_my_second_outlier_df(df):
    '''
    Displays dataframe of outliers for one-point agendas
    '''

    # get desired data 
    df_example = df[(df.access_threshold == 14) & (df.one_point_agendas == 0)]

    df_example = df_example[['deck_size',
                            'agenda_points',
                            'one_point_agendas',
                            'two_point_agendas',
                            'three_point_agendas',
                            'access_threshold']]
    
    return df_example


def get_my_ltd_data(df):
    '''
    Plots and displays a chart of possible access thresholds by number of two-point agendas replaced by Let Them Dream agendas
    '''

    # plot chart
    ax = sns.scatterplot(data=df,
                         x= 'ltd_count', 
                         y='access_threshold',
                         color= '#779ECB')

    # set ticks to integers
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # set labels and Title
    plt.xlabel('Let Them Dream Count')
    plt.ylabel('Access Threshold')

    plt.title('Each Let Them Dream Replacement Raises Access Threshold by About 1', fontweight='bold')

    # make pretty and display
    plt.tight_layout()
    plt.show()