#!usr/bin/env python3

import json
import requests
import csv
import os
import pandas as pd
# stock = input('Please enter stock symbol you want to compare:  ')

# start_date = input('Enter start date: ')

# end_date = input('Enter end date: ')

try:
    os.remove('bit_dates.csv')
except OSError:
    pass

try:
    os.remove('stock.csv')
except OSError:
    pass

try:
    os.remove('combined.csv')
except OSError:
    pass

deep_link = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=2018-01-01&end=2018-01-08&api_key=ZxbbrDjmsCg4vFZC1Uu5'
# deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/{stock}.json?start_date={start_date}&end_date={end_date}&api_key={api_key}'.format(stock=stock, start_date=start_date, end_date=end_date, api_key=api_key)
response = json.loads(requests.get(deep_link).text)
bpi_good = (response['bpi'])

deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?&start_date=2018-01-01&end_date=2018-01-08&api_key=ZxbbrDjmsCg4vFZC1Uu5'
# deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/{stock}.json?start_date={start_date}&end_date={end_date}&api_key={api_key}'.format(stock=stock, start_date=start_date, end_date=end_date, api_key=api_key)
response = json.loads(requests.get(deep_link).text)
whole = (response['dataset'])

print(whole)


a = []
x = [[k, v] for k, v in whole.items()]
y = x[17][1]
for i in y:
    key = (i[0])
    value = (i[4])
    a.append((key, value))

stockl = sorted(a)
bipdic = dict(stockl)


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
# print(l)

# result_dict = {}
# for x in y:
#     if x.key not in result_dict:
#         result_dict[x.key] = []
#     result_dict[x.key].append(x.value)


###Make Excel Sheets for both with same dates###


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

a = pd.read_csv("bit_dates.csv")
b = pd.read_csv("stock.csv")
b = b.dropna(axis=1)
df = a.merge(b, on='Date')
df.to_csv("combined.csv", index=False)
print(df)
# with open('combined.csv', 'r+') as comb:
#     writer = csv.writer(comb)
#     writer.writerow(["Date", "AdjClose Bitcoin", "AdjClose Stock"])
#     with open('bit_dates.csv', 'r+') as f:
#         reader = csv.reader(f)
#         writer.writerows(row + row[:0] for row in reader)
#     with open('stock.csv', 'r+') as f:
#         reader = csv.reader(f)
#         writer.writerows(row[2:] + row[1:3] for row in reader)
# for i in l:
# writer.writerow(i)
# writer.writerows(row + row[0] for row in l)
# with open('bit_dates.csv', 'r+') as f:
#     reader = csv.reader(f)
#     # writer.writerows(row + [0] for row in reader)
#     writer.writerows(row for row in reader)
# with open('stock.csv', 'r+') as f:
#     reader = csv.reader(f)
#     writer.writerows(row[1:] for row in reader)
#     # writer.writerows(row[:2] for row in reader)
# print(bipdic)
# print(stockdic)
