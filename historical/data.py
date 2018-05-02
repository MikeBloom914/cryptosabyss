#! usr/bin/env python3
#### GRAPH COMPARING STOCK VS BITCOIN NORMALIZED ####

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import os
import csv
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

stock = 'FDN'

start_date = 'May 01, 2017'
end_date = 'Apr 30, 2017'


ok = pd.read_csv('oneyear.csv', header=0)
series = ok.ix[:, ['Bitcoin']]
values = series.values
values = values.reshape((len(values), 1))
# (row   ,   columns)
scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(values)
normalized = scaler.transform(values)
h = []

for i in range(len(values)):
    h.append(float(normalized[i]))

counts = ok.ix[:, ['{stock}'.format(stock=stock)]]
nums = counts.values

####NORMALIZE Stock####
norm = MinMaxScaler(feature_range=(0, 1))
norm = norm.fit(nums)
fixed = norm.transform(nums)
g = []

for x in range(len(nums)):
    g.append(float(fixed[x]))
    # return g

### CREAT DataFrames for everything so it is easy to merge what I want ###

dfbitnorm = pd.DataFrame(np.array(h).reshape(len(values), 1), columns=list("B"))

dfstocknorm = pd.DataFrame(np.array(g).reshape(len(values), 1), columns=list("N"))
dfprice = pd.read_csv('oneyear.csv')
df4 = dfstocknorm.join(dfbitnorm)
dfall = dfprice.join(df4)
print(dfall)
corr1 = dfall['{stock}'.format(stock=stock)].corr(dfall['Bitcoin'])
rdcorr = round(corr1, 2)

df = dfall.to_csv('{stock}.csv'.format(stock=stock))

print(rdcorr)

app = dash.Dash()

# df1 = pd.read_csv('{stock}.csv.'.format(stock=stock))

####TO DO####
# HAVE A CHECKLIST/DROPDOWN for 5 year, 1 year, 6 mo
app.layout = html.Div(children=[
    html.H2(children="Bitcoin vs {stock} has a correlation of {rdcorr} from {start_date} through {end_date}".format(stock=stock, rdcorr=rdcorr, start_date=start_date, end_date=end_date)),
    dcc.Graph(
        id="'{stock}' vs Bitcoin".format(stock=stock),
        figure={
            'data': [
                {
                    'x': dfprice['Date'],
                    'y': dfall['B'],
                    'type': 'line',
                    'name': 'Bitcoin',
                    'text': dfprice['Bitcoin'],
                    'hoverinfo': 'text'

                },
                {
                    'x': dfprice['Date'],
                    'y': dfall['N'],
                    'type': 'line',
                    'name': 'N',
                    'text': dfprice['{stock}'.format(stock=stock)],
                    'hoverinfo': 'text'
                }
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Normalized Price'},
                margin={'l': 60, 'b': 100, 't': 10, 'r': 40},
                legend={'x': 0, 'y': 1},
            )

        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=5000)
