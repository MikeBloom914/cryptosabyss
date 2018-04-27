#!usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv('/Users/bloom/bitcompare/combined.csv')


app.layout = html.Div(children=[
    html.H2(children='Stock vs Bitcoin'),
    dcc.Graph(
        id='Stock vs Bitcoin',
        figure={
            'data': [
                go.Scatter(
                    x=df['Date'],
                    y=df['Stock'],
                    # text=df['StockPrice'],
                    # hoverinfo='text',
                    mode='line',
                    opacity=0.7,
                    # marker={
                    #    'size': 15,
                    #    'line': {'width': 0.5, 'color': 'white'}
                    #},

                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Date'},
                yaxis={'title': 'Normalized Price'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                # hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()
