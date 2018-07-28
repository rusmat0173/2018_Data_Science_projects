"""
Created on Sat 09 June 2018

@author: rahmed

RA Note pandas, etc. practice for Course01/Wee03 of Wesleyan MOOC
Using British Survey of Attitudes 2016, /Users/RAhmed/WesleyanMOOC/Course01/Week02/UKDA-8252-tab/bsa16_to_ukda.csv'
Use data dictionary at /Users/RAhmed/WesleyanMOOC/Course01/Week02/.../UKDA-8252-tab/bsa16_to_ukda_ukda_data_dictionary.rtf

I want to get:
i). bar chart of a categorical variable with seaborn
ii). do same for a selected geographical area
> I will use Spend1 categorical variable that has 11 main categories, plus others (98, 99)
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# function I made to do all printing stuff


def common_plot(dataframe, x_var, y_lim_max, ticks, x_label, sup_title, custom_title, annotation, annotation_height, palette):
    pal = sns.color_palette(palette)
    g = sns.countplot(x=x_var, data=dataframe, palette=palette)
    plt.ylim(0, y_lim_max)
    plt.xlim(0.5, None)
    g.set_xticklabels(labels=ticks, rotation=45)
    g.set(xlabel=x_label)
    plt.suptitle(sup_title, fontsize=14)
    plt.title(custom_title)
    g.text(7, annotation_height, annotation)
    plt.show()


# = = = develop and work under here = = =
# read file as dataframe
df = pd.read_csv(
    '/Users/RAhmed/WesleyanMOOC/Course01/Week02/UKDA-8252-tab/bsa16_to_ukda.csv', low_memory=False)
print(len(df.columns))  # number of variables (columns)

# set seaborn background colour. see https://seaborn.pydata.org/tutorial/aesthetics.html?highlight=style
sns.set_style("dark")

# ensure the variables are categorical
df['Spend1'] = df['Spend1'].astype('category')
df['GOR_ID'] = df['GOR_ID'].astype('category')
# get a frequency table for the Spend1 responses
category1 = df['Spend1'].value_counts(sort=False)
print (category1)

# if you only want to look at selected observations (e.g.) just for a single geopgraphical region
# you do this by creating a subset of whole dataframe just for those observations
subdf = df[(df['GOR_ID'] == 7)]  # <= 7 is London
print(len(subdf))
# ^ above is simple and powerful
# could make more complex by adding other 'constraints' such as (e.g.)   ... & (df['RageCat'] == 3) ...]
# e.g.:
# <= GOR_ID 7 is London, RAgeCAt 6&7 are ages 60+
subdf2 = df[(df['GOR_ID'] == 7) & (df['RAgeCat'] >= 6) & (df['RAgeCat'] < 8)]
# can't do (5< df['RAgeCat'] < 8) - doesn't work
print(len(subdf2))

# noted here only> set color palette. see http://jose-coto.com/styling-with-seaborn
# here a simple one-liner way to do this
# pal = sns.color_palette('Purples_r') # _r reverses

# common variables for common_plot function
ticks = ['DNS', 'Edu', 'Def', 'Hea', 'Hou', 'Tra', 'Roa', 'Pol', 'SSB', 'Ind', 'Aid', 'Non']
x_label = "Priority area for spending"
x_var = 'Spend1'
sup_title = 'British Social Attitudes Survey 2016'
annotation = "Note that less than a third\nof people expressed an opinion\nfor this question"

# ALL YOU NEED TO DO is comment out the frames you will NOT use, below. The common_plot function will do the rest
# (main) dataframe details
# dataframe = df
# palette = sns.color_palette('Greens')
# y_lim_max = 550
# annotation_height = 470
# custom_title = "\nWhere govt. should target additional spending, raw count - national"

# (sub) dataframe details
# dataframe = subdf
# palette = sns.color_palette('Reds')
# y_lim_max = 50
# annotation_height = 43
# custom_title = "\nWhere govt. should target additional spending, raw count - London"

# another (sub) dataframe details
dataframe = subdf2
palette = sns.color_palette('Blues')
y_lim_max = 15
annotation_height = 13
custom_title = "\nWhere govt. should target additional  spending, raw count - London 65+"

common_plot(dataframe, x_var, y_lim_max, ticks, x_label, sup_title,
            custom_title, annotation, annotation_height, palette)
