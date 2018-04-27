#! usr/bin/env python3

################ NORMALIZES AND WRITES A NEW CSV WITH NORMALIZED PRICES#######
################ FOR 1 COLUMN ONLY###############
################ TODO: HAVE IT READ FROM 1 FILE WITH BOTH NORMALIZED PRICES#######

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import csv

####READ DATA FROM FILE####
series = pd.read_csv('/Users/bloom/bitcompare/stock.csv', header=0)
# print(series)

values = series.values
values = values.reshape((len(values), +1))
# print(values)

####NORMALIZE####
scaler = MinMaxScaler(feature_range=(0, 1))
# print(scaler)
scaler = scaler.fit(values)
# print(scaler)
normalized = scaler.transform(values)
h = []

for i in range(len(values)):
    h.append(float(normalized[i]))

print(h)

os.system('touch stocknorm.csv')
with open('/Users/bloom/bitcompare/stocknorm.csv', 'r+') as f:
    dates = csv.writer(f)
    dates.writerow(["Stock"])
    for i in h:
        dates.writerow([i])

# file = pd.read_csv('/Users/bloom/bitcompare/combined.csv', header=0)

# dates = file.values

# cars = dates.reshape(len(dates), 1)

# i = []
# for j in range(len(cars)):
#     i.append([j])
