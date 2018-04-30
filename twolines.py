#! usr/bin/env python3


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import together

app = dash.Dash()

df = pd.read_csv('all.csv')
#dfall = df
####TO DO####
### HAVE HOVERING INFO BE STOCKPRICE AND BITCOIN PRICE ###
# HAVE A CHECKLIST/DROPDOWN for 5 year, 1 year, 6 mo
app.layout = html.Div(children=[
    html.H2(children='Stock vs Bitcoin'),
    dcc.Graph(
        id='Stock vs Bitcoin',
        figure={
            'data': [
                {
                    'x': df['Date'],
                    'y': df['B'],
                    'type': 'line',
                    'name': 'Bitcoin',
                    #'text': df['StockPrice'],
                    #'hoverinfo': 'text'
                    #'hoverinfo': df['StockPrice']
                },
                {
                    'x': df['Date'],
                    'y': df['S'],
                    'type': 'line',
                    'name': 'Stock',
                    #'text': df['BitcoinPrice'],
                    #'hoverinfo': 'text'
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
    app.run_server(debug=True, host='0.0.0.0')
