#!usr/bin/env python3

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
#import json
import pandas as pd
import numpy as np
import plotly

app = dash.Dash()
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1('Welcome to Bloom\'s Page!'),
    dcc.Link('CryposAbyss', href='/page-1'),
    html.Br(),
    dcc.Link('Anacott Steel', href='/page-2'),
])


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

page_1_layout = html.Div([
    html.H2('CryptosAbyss'),
    html.H4('Google and Yahoo represent the interest of the chosen words/terms that were searched in Google / Youtube over the time frame presented.'),
    html.H6('--The amount of interest is represented with numbers on a scale from 0-100 having 100 being the moment in the time frame where there was the most interest in searching Google or Yahoo with the word/term presented, and 0 being the least amount of interest shown.'),
    html.H6('--These numbers as well as stock/etf prices were then normalized on a scale of 0-1 which will show the price/interest over the course of time for each item.'),
    html.H4('After converting all the numbers to normalized numbers on an equal 0-1 scale, the number shown under correlation represents the percentage amount of movement that each of the given items move over time ALL compared to the price of Bitcoin'),
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
    #], className="container"),
    #     dcc.Dropdown(
    #         id='page-1-dropdown',
    #         options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    #         value='LA'
    #     ),
    # html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Anacott Steel', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    # ])
], className="container")


@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
# @app.callback(dash.dependencies.Output('page-1-content', 'children'),
#               [dash.dependencies.Input('page-1-dropdown', 'value')])
# def page_1_dropdown(value):
#     return 'You have selected "{}"'.format(value)
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


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('CryptosAbyss', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page


# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=12000)
