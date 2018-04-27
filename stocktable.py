#!usr/env/bin python3
#import datetime
import pandas_datareader.data as web
#import json
#import requests
# deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json?&start_date=2018-01-01&end_date=2018-01-08&api_key=ZxbbrDjmsCg4vFZC1Uu5'
# #deep_link = 'https://www.quandl.com/api/v3/datasets/WIKI/{stock}.json?start_date={start_date}&end_date={end_date}&api_key={api_key}'.format(stock=stock, start_date=start_date, end_date=end_date, api_key=api_key)
# response = json.loads(requests.get(deep_link).text)
# whole = (response['dataset'])

###Have usr input dates in that format###
start = '2017-01-01'
end = '2018-01-01'
#start = datetime.datetime(2015, 1, 1)
#end = datetime.datetime.now()
df = web.DataReader("TSLA", 'quandl', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
# axis 0 = row
# axis 1 = column
df = df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], axis=1)

print(df.head())
