#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 00:36:41 2018

@author: RAhmed

really good seaborn documenation at
https://seaborn.pydata.org/tutorial/distributions.html
"""

# libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random

# standard matplotlib doc text
# create data
x = np.random.normal(size=50000)
y = x * 3 + np.random.normal(size=50000)

# Big bins
plt.hist2d(x, y, bins=(50, 50), cmap=plt.cm.jet)
# plt.show()

# Small bins
plt.hist2d(x, y, bins=(300, 300), cmap=plt.cm.jet)
# plt.show()

# If you do not set the same values for X and Y, the bins aren't square !
plt.hist2d(x, y, bins=(300, 30), cmap=plt.cm.jet)
# plt.show()

# my own data
height = [random.gauss(180, 40) for x in range(1000)]
weight = []
for h in height:
    weight.append(0.5*h + random.gauss(0, 25))
plt.hist2d(height, weight, bins=(20, 20), cmap=plt.cm.gist_yarg)  # <= find another color map

# naturally in seaborn (since close to pandas) this only works if is a pandas object
# or an np.array, since pandas built on np. Seaborn gives you additional info also
sns.jointplot(np.array(height), np.array(weight), kind="hex", cmap=plt.cm.binary)

# always need this
plt.show()
