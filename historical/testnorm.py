#! usr/bin/env python3

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import csv
import numpy as np

####NORMALIZE Bitcoin####

####READ DATA FROM FILE####
ok = pd.read_csv('combined.csv', header=0)
series = ok.ix[:, ['Bitcoin']]
values = series.values
values = values.reshape((len(values), 1))
###             (row   ,   columns)

scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(values)
normalized = scaler.transform(values)
h = []

for i in range(len(values)):
    h.append(float(normalized[i]))
    return h


counts = ok.ix[:, ['Stock']]
nums = counts.values

####NORMALIZE Stock####
norm = MinMaxScaler(feature_range=(0, 1))
norm = norm.fit(nums)
fixed = norm.transform(nums)
g = []

for x in range(len(nums)):
    g.append(float(fixed[x]))
    return g


### CREAT DataFrames for everything so it is easy to merge what I want ###

dfbitnorm = pd.DataFrame(np.array(h).reshape(len(values), 1), columns=list("B"))

dfstocknorm = pd.DataFrame(np.array(g).reshape(len(values), 1), columns=list("S"))

df4 = dfcomb.join(dfbitnorm)
dfall = df4.join(dfstocknorm)

corr1 = dfall['Stock'].corr(dfall['Bitcoin'])
rdcorr = round(corr1, 2)

dfall.to_csv('all.csv')

print(rdcorr)
