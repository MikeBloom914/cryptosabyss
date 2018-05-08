import dash
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
from pandas_datareader.data import DataReader
import time

app = dash.Dash('stock-tickers')
server = app.server

app.scripts.config.serve_locally = False
#dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

df_symbol = pd.read_csv('stocklist.csv')

app.layout = html.Div([
    html.Div([
        html.H2('Anacott Steel',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Div([
            dcc.DatePickerRange(
                id='date-range',
                start_date=dt.date(2017, 1, 1),
                end_date=dt.date.today(),
            ),
        ], style={'clear': 'left', 'padding-top': '10px'},
        ),
        html.Img(src="https://img.etsystatic.com/il/816ca7/1430618519/il_570xN.1430618519_mwz6.jpg?version=1",
                 style={
                     'height': '200px',
                     'float': 'right'
                 },
                 ),
    ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': str(s[1])}
                 for s in zip(df_symbol.Company, df_symbol.Symbol)],
        multi=True
    ),
    html.Div(id='graphs')
], className="container")


def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band


@app.callback(
    dash.dependencies.Output('graphs', 'children'),
    [dash.dependencies.Input('stock-ticker-input', 'value'), dash.dependencies.Input('date-range', 'start_date'), dash.dependencies.Input('date-range', 'end_date')])
def update_graph(tickers, start_date, end_date):

    if not tickers:
        return []

    graphs = []
    for i, ticker in enumerate(tickers):
        try:
            df = DataReader(str(ticker), 'quandl',
                            dt.datetime.strptime(start_date, '%Y-%m-%d'),
                            dt.datetime.strptime(end_date, '%Y-%m-%d'))

        except:
            graphs.append(html.H3(
                'Data is not available for {}'.format(ticker),
                style={'marginTop': 20, 'marginBottom': 20}
            ))
            continue

        candlestick = {
            'x': df.index,
            'open': df['Open'],
            'high': df['High'],
            'low': df['Low'],
            'close': df['Close'],
            'type': 'candlestick',
            'name': ticker,
            'legendgroup': ticker,
            'increasing': {'line': {'color': colorscale[0]}},
            'decreasing': {'line': {'color': colorscale[1]}}
        }
        bb_bands = bbands(df.Close)
        bollinger_traces = [{
            'x': df.index, 'y': y,
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[(i * 2) % len(colorscale)]},
            'hoverinfo': 'none',
            'legendgroup': ticker,
            'showlegend': True if i == 0 else False,
            'name': '{} - bollinger bands'.format(ticker)
        } for i, y in enumerate(bb_bands)]
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data': [candlestick] + bollinger_traces,
                'layout': {
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))

    return graphs


external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

###make sure you connect this to FLASK and not DASH if I add FLASK pages###
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
