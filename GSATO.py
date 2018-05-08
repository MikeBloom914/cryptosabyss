#! usr/bin/env python3
#### GRAPH COMPARING ref VS BITCOIN NORMALIZED ####

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
import sys

ref = 'GSATO'
#ref = sys.argv[0]
start_date = 'May 01, 2017'
end_date = 'Apr 30, 2017'


ok = pd.read_csv('oneyearwkly.csv', header=0)
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

counts = ok.ix[:, ['{ref}'.format(ref=ref)]]
nums = counts.values

####NORMALIZE ref####
norm = MinMaxScaler(feature_range=(0, 1))
norm = norm.fit(nums)
fixed = norm.transform(nums)
g = []

for x in range(len(nums)):
    g.append(float(fixed[x]))
    # return g

### CREAT DataFrames for everything so it is easy to merge what I want ###

dfbitnorm = pd.DataFrame(np.array(h).reshape(len(values), 1), columns=["Bit"])

dfrefnorm = pd.DataFrame(np.array(g).reshape(len(values), 1), columns=["ref"])
DF_Price = pd.read_csv('oneyearwkly.csv')
df4 = dfrefnorm.join(dfbitnorm)
DF_All = DF_Price.join(df4)
# print(DF_All)
corr1 = DF_All['{ref}'.format(ref=ref)].corr(DF_All['Bitcoin'])
rdcorr = round(corr1, 3)

#df = DF_All.to_csv('{ref}.csv'.format(ref=ref))

print(rdcorr)

###dispacher###
app = dash.Dash()

# df1 = pd.read_csv('{ref}.csv.'.format(ref=ref))

####TO DO####
### HAVE A CHECKLIST/DROPDOWN###
app.layout = html.Div(children=[
    html.H2(children="Bitcoin vs {ref} has a correlation of {rdcorr} from {start_date} through {end_date}".format(ref=ref, rdcorr=rdcorr, start_date=start_date, end_date=end_date)),
    html.H4('*Hover over lines to show prices'),
    html.H4('*Click and drag over graph to zoom in; double click to zoom out'),
    dcc.Graph(
        id="'{ref}' vs Bitcoin".format(ref=ref),
        figure={
            'data': [
                {
                    'x': DF_Price['Date'],
                    'y': DF_All['Bit'],
                    'type': 'line',
                    'name': 'Bitcoin',
                    'text': DF_Price['Bitcoin'],
                    'hoverinfo': 'text'

                },
                {
                    'x': DF_Price['Date'],
                    'y': DF_All['ref'],
                    'type': 'line',
                    'name': '{ref}'.format(ref=ref),
                    'text': DF_Price['{ref}'.format(ref=ref)],
                    'hoverinfo': 'text'
                }],

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
    app.run_server(debug=True, host='0.0.0.0', port=5018)
