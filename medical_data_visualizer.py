import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column

bmi = (df['weight']) / ((df['height'] / 100) ** 2)
df['overweight'] = [1 if value >25 else 0 for value in bmi]

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = [0 if value == 1 else 1 for value in df['cholesterol']]
df['gluc'] = [0 if value == 1 else 1 for value in df['gluc']]


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat =  df_cat =  pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=[
            'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'
        ])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().rename('total').reset_index()

    # Draw the catplot with 'sns.catplot()'
    cat_plot = sns.catplot(data = df_cat, x = 'variable', y = 'total', kind = 'bar', hue = 'value', col = 'cardio')

    fig = cat_plot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                (df['height'] >= df['height'].quantile(0.025)) & 
                (df['height'] <= df['height'].quantile(0.975)) & 
                (df['weight'] >= df['weight'].quantile(0.025)) & 
                (df['weight'] <= df['weight'].quantile(0.975)) ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize = (20,10) )

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, vmax=.3, center=0,
              square=True, linewidths=.9, cbar_kws={"shrink": .5})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
