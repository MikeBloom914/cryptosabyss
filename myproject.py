import creds
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import flask
from flask import Flask
import pandas as pd
import numpy as np
import plotly


plotly.tools.set_credentials_file(username=creds.username, api_key=creds.api_key)

#app = dash.Dash()
app_flask = flask.Flask(__name__)
app = dash.Dash(__name__, server=app_flask)

#server = app.server

app.scripts.config.serve_locally = True

DF_TableBit = pd.read_csv('newchart.csv')

DF_TableBit = DF_TableBit[DF_TableBit['Term'] == '05/01/17-04/30/18']
DF_TableBit.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [-1, -.6, -.2, .2, .6, 1],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]


app.layout = html.Div([
    html.H5('CryptosAbyss is an statistical data analyzing project which involves an interactive table that produces three time series bar charts showing the relationship between the price of Bitcoin and other contemporary phenomena over the course of time.'),
    html.H6('-Google and YouTube represent the popularity of the search term mentioned under "description" relative throughout the time period.'),
    html.H6('--Correlation numbers represent a one percent movement on a normalized scale from -1 to 1.'),
    html.H6("""---For example, the correlation between Bitcoin and GCRYPT was .84. If you look at a graph of the price of Bitcoin and a graph of the popularity of the search term "Crypto" in google throughout the same time period, their movements on the x and y axis' match up 84% of the time. """),
    html.H6('----The three columns represent correlation at the same time, with "var X" one week and one month before Bitcoin respectfully...any questions please feel free to email me at mikebloom914@gmail.com.'),
    html.H6('*Ticker Symbols for social media are those of BloomsEdge.com and not official'),
    dt.DataTable(
        rows=DF_TableBit.to_dict('records'),

        # optional - sets the order of columns
        # columns=sorted(DF_TableBit.columns),

        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-crypto'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-crypto'
    ),
], className="container")


@app.callback(
    Output('datatable-crypto', 'selected_row_indices'),
    [Input('graph-crypto', 'clickData')],
    [State('datatable-crypto', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-crypto', 'figure'),
    [Input('datatable-crypto', 'rows'),
     Input('datatable-crypto', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Correlation to Price of Bitcoin', 'Correlation one week ahead of the price of the Bitcoin', 'Correlation one month ahead of the price of Bitcoin',),
        shared_xaxes=False)
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['Ticker'],
        'y': dff['Correlation'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['Ticker'],
        'y': dff['Corr1week'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['Ticker'],
        'y': dff['Corr1month'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 1400
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app_flask.run(debug=True)
