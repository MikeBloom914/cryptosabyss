#!/usr/bin/env python3

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly
import os
import csv
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np


def graph(symbol):
    app = dash.Dash()
    #symbol = 'GBDK'
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

    counts = ok.ix[:, ['{symbol}'.format(symbol=symbol)]]
    nums = counts.values

    ####NORMALIZE symbol####
    norm = MinMaxScaler(feature_range=(0, 1))
    norm = norm.fit(nums)
    fixed = norm.transform(nums)
    g = []

    for x in range(len(nums)):
        g.append(float(fixed[x]))
        # return g

    ### CREATE DataFrames for everything so it is easy to merge what I want ###

    dfbitnorm = pd.DataFrame(np.array(h).reshape(len(values), 1), columns=["Bit"])

    dfsymbolnorm = pd.DataFrame(np.array(g).reshape(len(values), 1), columns=["symbol"])
    DF_Price = pd.read_csv('oneyearwkly.csv')
    df4 = dfsymbolnorm.join(dfbitnorm)
    DF_All = DF_Price.join(df4)
    # print(DF_All)
    corr1 = DF_All['{symbol}'.format(symbol=symbol)].corr(DF_All['Bitcoin'])
    rdcorr = round(corr1, 3)

    # df = DF_All.to_csv('{symbol}.csv'.format(symbol=symbol))

    # print(rdcorr)

    # df1 = pd.read_csv('{symbol}.csv.'.format(symbol=symbol))

    ####TO DO####
    ### HAVE A CHECKLIST/DROPDOWN ###
    app.layout = html.Div(children=[
        html.H2(children="Bitcoin vs {symbol} has a correlation of {rdcorr} from {start_date} through {end_date}".format(symbol=symbol, rdcorr=rdcorr, start_date=start_date, end_date=end_date)),
        html.H4('*Hover over lines to show prices'),
        html.H4('*Click and drag over graph to zoom in; double click to zoom out'),
        dcc.Graph(
            id="'{symbol}' vs Bitcoin".format(symbol=symbol),
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
                        'y': DF_All['symbol'],
                        'type': 'line',
                        'name': '{symbol}'.format(symbol=symbol),
                        'text': DF_Price['{symbol}'.format(symbol=symbol)],
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
    app.run_server(debug=True, host='0.0.0.0', port=9000)
