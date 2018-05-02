#! usr/bin/env python3
#### GRAPH COMPARING STOCK VS BITCOIN NORMALIZED ####

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import testhist
from testhist import rdcorr, start_date, end_date

stock = 'DIA'
app = dash.Dash()
#stock = 'c'
df = pd.read_csv('all.csv')
#dfall = df
####TO DO####
# HAVE A CHECKLIST/DROPDOWN for 5 year, 1 year, 6 mo
app.layout = html.Div(children=[
    html.H2(children="Bitcoin vs {stock} has a correlation of {rdcorr} during the year {start_date} - {end_date}".format(stock=stock, rdcorr=rdcorr, start_date=start_date, end_date=end_date)),
    dcc.Graph(
        id="'{stock}' vs Bitcoin".format(stock=stock),
        figure={
            'data': [
                {
                    'x': df['Date'],
                    'y': df['B'],
                    'type': 'line',
                    'name': 'Bitcoin',
                    'text': df['Bitcoin'],
                    'hoverinfo': 'text'

                },
                {
                    'x': df['Date'],
                    'y': df['S'],
                    'type': 'line',
                    'name': '{stock}'.format(stock=stock),
                    'text': df['{stock}'.format(stock=stock)],
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
