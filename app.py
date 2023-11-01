from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from verdin import tinybird
import json

with open('data-project/.tinyb') as tb:
    tb_token = json.load(tb)['token']

tb_client = tinybird.Client(
    token=tb_token, api="https://api.us-east.tinybird.co")
airlines = tb_client.pipe("airlines")
meals = tb_client.pipe("meals")
flight_bookings_by_minute = tb_client.pipe("flight_bookings_by_minute")


airlines: tinybird.PipeJsonResponse = airlines.query()
airlines_options = pd.json_normalize(airlines.data)

meals: tinybird.PipeJsonResponse = meals.query()
meal_options = pd.json_normalize(meals.data)

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

colors = {
    'background': '#000000',
    'text': '#ffffff'
}

app.layout = html.Div(style={'padding': '2rem'}, children=[
    html.H1(children='A real-time Python dashboard built with Tinybird and Dash',
            style={
                'textAlign': 'left',
                'paddingLeft': '5rem'
            }
            ),
    html.Div(style={'display': 'flex', 'width': '100%', 'paddingLeft': '5rem', 'marginTop': '2rem'},
             children=[
        dcc.Dropdown(airlines_options.airline,
                     multi=True,
                     id='airline-selector',
                     placeholder="Filter by airline(s)",
                     style={'width': 'auto',
                            'minWidth': '250px',
                            'margin': '0.1em'}
                     ),
        dcc.Dropdown(meal_options.meal_preference,
                     id='meal-selector',
                     placeholder="Filter by meal preference",
                     style={'width': 'auto',
                            'minWidth': '250px',
                            'margin': '0.1em'}
                     ),
        html.Div(style={'maxWidth': '100px', 'padding': '0.5em'}, children=[
            html.P(children='Lookback', style={'margin': 'auto'})
        ],),
        dcc.Input(id='lookback-input',
                  type="number",
                  debounce=True,
                  value=1,
                  style={'maxWidth': '50px',
                         'margin': '0.1em',
                         'border': '1px solid #ccc',
                         'borderRadius': '4px'}

                  ),
        html.Div(style={'maxWidth': '100px', 'padding': '0.5em'}, children=[
            html.P(children='hrs', style={'margin': 'auto'})
        ],),
    ]),
    dcc.Interval(interval=5000,
                 n_intervals=0,
                 id='refresh-interval'
                 ),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    [Input('airline-selector', 'value'),
     Input('meal-selector', 'value'),
     Input('lookback-input', 'value'),
     Input('refresh-interval', 'n_intervals')]
)
def update_graph(airlines, meal, lookback, n):
    if airlines:
        airlines = ','.join(airlines)
    response: tinybird.PipeJSONResponse = flight_bookings_by_minute.query({
        "airlines": airlines,
        "meal_preference": meal,
        "lookback": lookback
    })
    df = response.data.copy()
    return px.line(df, x='minute', y='count', color='airline')


if __name__ == '__main__':
    app.run(debug=True)
