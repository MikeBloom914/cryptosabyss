#!usr/bin/env python3

import json
import requests
import csv
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

try:
    os.remove('stock.csv')
    os.remove('bit_dates.csv')
    os.remove('combined.csv')
    os.remove('all.csv')

except OSError:
    pass

###GET DATA###

#### Write stock symbol####
stock = 'aapl'
####### Write start and end dates in a STRING in the format YYYY-MM-DD #######
start_date = '2017-04-30'
end_date = '2018-04-30'
###############################################################################

api_key = 'ZxbbrDjmsCg4vFZC1Uu5'

deep_link = 'https://api.coindesk.com/v1/bpi/historical/close.json?start={start}&end={end}'.format(start=start_date, end=end_date)
response = json.loads(requests.get(deep_link).text)
bpi_good = (response['bpi'])


deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/{stock}.json?start_date={start_date}&end_date={end_date}&api_key={api_key}'.format(stock=stock, start_date=start_date, end_date=end_date, api_key=api_key)
response = json.loads(requests.get(deep_link).text)
whole = (response['dataset'])


a = []
x = [[k, v] for k, v in whole.items()]
y = x[17][1]
for i in y:
    key = (i[0])
    value = (i[4])
    a.append((key, value))

stockl = sorted(a)
bipdic = dict(stockl)
# print(stockl)

###THIS IS COMPARE FORUMLA###
d = []
for key in bipdic:
    if key in bpi_good:
        c = (key, bpi_good[key])
        d.append(c)
stockdic = dict(d)

##trying to make 1 dict first###
ds = [stockdic, bipdic]
d = {}
l = []
for k in stockdic.keys():
    d[k] = list(d[k] for d in ds)
    l.append(d[k])
# print(d)

###Make CSV FILES for both with same dates###

os.system('touch bit_dates.csv')
os.system('touch combined.csv')
os.system('touch stock.csv')

with open('bit_dates.csv', 'r+') as f:
    dates = csv.writer(f)
    dates.writerow(["Date", "Bitcoin"])
    for key, value in stockdic.items():
        dates.writerow([key, value])


with open('stock.csv', 'r+') as g:
    dates = csv.writer(g)
    dates.writerow(["Date", "Stock"])
    for key, value in bipdic.items():
        dates.writerow([key, value])

#######REPLACE STOCK PRICES WITH WHATEVER ETF PRICES#######


a = pd.read_csv("bit_dates.csv")
b = pd.read_csv("stock.csv")
b = b.dropna(axis=1)
dfcomb = a.merge(b, on='Date')
dfcomb.to_csv("combined.csv", index=False)
# print(df)


####NORMALIZE Bitcoin####

####READ DATA FROM FILE####
ok = pd.read_csv('combined.csv', header=0)
# print(series)
series = ok.ix[:, ['Bitcoin']]
# print(series)
values = series.values
values = values.reshape((len(values), 1))
# print(values)         (row   ,   columns)

scaler = MinMaxScaler(feature_range=(0, 1))
# print(scaler)
scaler = scaler.fit(values)
# print(scaler)
normalized = scaler.transform(values)
h = []

for i in range(len(values)):
    h.append(float(normalized[i]))

# print(h)


####NORMALIZE Stock####
counts = ok.ix[:, ['Stock']]
# print(counts)
nums = counts.values
nums = nums.reshape((len(nums), 1))
# print(values)

norm = MinMaxScaler(feature_range=(0, 1))
# print(scaler)
norm = norm.fit(nums)
# print(scaler)
fixed = norm.transform(nums)
g = []

for x in range(len(nums)):
    g.append(float(fixed[x]))

# print(g)

### CREAT DataFrames for everything so it is easy to merge what I want ###

dfbitnorm = pd.DataFrame(np.array(h).reshape(len(values), 1), columns=list("B"))
# print(dfbitnorm)

dfstocknorm = pd.DataFrame(np.array(g).reshape(len(values), 1), columns=list("S"))
# print(dfstocknorm)


df4 = dfcomb.join(dfbitnorm)
dfall = df4.join(dfstocknorm)

corr1 = dfall['Stock'].corr(dfall['Bitcoin'])
corr2 = dfall['S'].corr(dfall['B'])

dfall.to_csv('all.csv')

###there shouldn't be, but a test between corr of prices and normalized prices###
print(corr1)

#### TODO: MAKE 1 CSV WITH ALL 5 COLUMNS ###
