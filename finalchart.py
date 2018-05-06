import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
#from bitetfgraph import ref
app = dash.Dash()
# print(ref)
app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

#DF_Bitcoin = pd.read_csv('test.csv')

DF_ChartBit = pd.read_csv('chartinfo.csv')

DF_ChartBit.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    #'y': [4, 3, 1, 2, 3, 6],
    'y': [0, .2, .4, .6, .8, 1],
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
    html.H4('CryptosAbyss'),
    html.H6('*Google and Yahoo represent the interest of those words/terms vs the price of Bitcoin over time'),
    html.H6('*Correlation numbers are calculated on a 0-1 scale, with a negative number meaning inversly correlated...to the price of Bitcoin over time'),
    dt.DataTable(
        rows=DF_ChartBit.to_dict('records'),
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('', '', 'Class',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    # fig.append_trace({
    #     'x': dff['Type'],
    #     'y': dff['Correlation to Bitcoin'],
    #     'type': 'bar',
    #     'marker': marker
    # }, 3, 1)
    # fig.append_trace({
    #     'x': dff['Type'],
    #     'y': dff['Correlation to Bitcoin'],
    #     'type': 'bar',
    #     'marker': marker
    # }, 2, 1)
    fig.append_trace({
        'x': dff['Type'],
        'y': dff['Correlation'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 1000
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
    app.run_server(debug=True, host='0.0.0.0', port=5000)
