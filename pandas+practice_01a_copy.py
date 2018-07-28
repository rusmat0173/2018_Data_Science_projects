import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt


# pandas works on series and data frames. https://khashtamov.com/en/pandas-data-analysis/
# Series here
random.seed(1)
my_series = [(1000 * (1.03)**x + random.randrange(-5, 5)) for x in range(10)]
print(my_series)

my_series1 = pd.Series(my_series)
print(my_series1)
print(my_series1[3])
print(my_series1.values)
print(my_series1.index)
# idx_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
idx_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
my_series2 = pd.Series([997, 1034, 1056.9, 1091.727, 1121.50881,
                        1161.2740743, 1196.05229653, 1231.87386542, 1267.77008139, 1302.77318383], index=idx_list)
print(my_series2)

# turn a dictionary into a series
my_dict = {'a': 5, 'b': 6, 'c': 7, 'd': 8}
my_series3 = pd.Series(my_dict)
print(my_series3)

# naming
my_series2.name = 'gdp_values'
my_series2.index.name = 'years'
my_series2  # <= interesting no print command or ()

# now, data frames: basically a table. Each COLUMN is a Series object!
inflation = [(2.5 + random.uniform(-1, 2)) for x in range(10)]
print(inflation)
my_data = pd.DataFrame({'year': idx_list, 'gdp': my_series2.values, 'inflation': inflation})
print(my_data)
print()
print(my_data['year'])
print(type(my_data['gdp']))  # <= you can see each column is a Series object
print(type(my_data['inflation']))
my_data.index = [str(2001 + x) for x in range(10)]
my_data.index.name = 'year'
print(my_data)

# get a whole row, just parts
print(my_data.loc["2001"])
print(my_data.iloc[1])
print(my_data.loc[:])
print(my_data.loc["2004": "2005"])
print(my_data.loc[["2008", "2009"]])
print(my_data.loc[["2008", "2009"], "gdp"])

# smart filtering
print(my_data[my_data.gdp > 1200])
print(my_data[my_data.gdp > 1200][["gdp"]])
print(my_data[my_data.gdp > 1250][["gdp", "inflation"]])

# add new column about target inflation
my_data['foo'] = [True for x in range(10)]
print(my_data)

# now delete
del my_data['foo']
print(my_data)

# create a more interesting column
inflation_controlled = []
for item in my_data['inflation']:
    if item <= 2.5:
        inflation_controlled.append(1)
    else:
        inflation_controlled.append(0)
print(inflation_controlled)
my_data['inflation controlled'] = inflation_controlled
print(my_data)
print()
print(my_data.groupby('inflation').size())  # <= sorts one column by inflation column

# want to make as a categorical type
my_data['inflation controlled'] = my_data['inflation controlled'].astype('category')

# seaborn looks better than pyplot (that = matplotlib), but needs no additional commands, just importing
# how to customise seaborn @: http://hookedondata.org/Better-Plotting-in-Python-with-Seaborn/
# also, seaborn tightly integrated with pandas
sns.countplot(x='inflation controlled', data=my_data)  # <= don't need a plot.show()
# plt.xlabel("Was inflation under control?") # <= this changes the x label
plt.title("Was inflation under control?")
plt.show()  # <= needed in pycharm; in spyder shows in console

# want to create a quantitative variable to plot
#norm_var = [random.gauss(100, 40) for x in range(100)]
#seaborn.distplot(norm_var, rug=True, bins=10)
norm_var1 = [random.gauss(100, 40) for x in range(100)]
sns.distplot(norm_var1, hist=False, rug=True, bins=10)

# want to create bivariate plots
height = [random.gauss(180, 40) for x in range(1000)]
weight = []
for h in height:
    weight.append(0.5*h + random.gauss(0, 25))
body_frame = pd.DataFrame({'height': height, 'weight': weight})
#sns.jointplot(x="height", y="weight", data=body_frame)
