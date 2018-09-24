import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from festivalTools import *
import json
import pandas as pd

app = dash.Dash()
df = []

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    html.Div([
    dcc.Input(id='my-id', value='My Favorite Festival..', type='text'),
    html.Div(id='my-div'),
    html.Button(id='submit-button', n_clicks=0, children='Find Me A Festival!')
    ]),


    html.Div(
        className="nine columns",
        children=dcc.Graph(
            id='graph',
            figure={
                'data': [{
                    'lat': [], 'lon': [], 'text': [], 'type': 'scattermapbox'
                }],
                'layout': {
                    'mapbox': {
                        'accesstoken': (
                            'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                            'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                        )
                    },
                    'margin': {
                        'l': 0, 'r': 0, 'b': 0, 't': 0
                    },
                }
            }
        )
    ),

    html.Div(id='my-table'),

], className="row")


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    Output('graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State(component_id='my-id', component_property='value')]
)
def update_output_div(n_clicks, input_value):

    global df
    df = getTop10Festivals(input_value, "Brooklyn")


    #handle case of low results - simply leave map empty
    emptyFigure={
        'data': [{
            'lat': [], 'lon': [], 'text': [], 'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': (
                    'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                    'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                )
            },
            'margin': {
                'l': 0, 'r': 0, 'b': 0, 't': 0
            },
        }
    }

    if df is None:
        return emptyFigure



    #otherwise, populate map
    figure={
        'data': [{
            'lat': df['Latitude'], 'lon': df['Longitude'],
            'text': df['Date'] + "<br>" + df['Event Name'] +
            ", " + df['City'],
            'mode':'markers',
            'marker': dict(
            size=11
            ),
            'type': 'scattermapbox'
        }],
        'layout': {
            'mapbox': {
                'accesstoken': (
                    'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                    'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                )
            },
            'margin': {
                'l': 0, 'r': 0, 'b': 0, 't': 0
            },
        }
    }

    return figure

@app.callback(
    Output(component_id='my-table', component_property='children'),
    [Input('graph', 'figure')],
    [State(component_id='my-id', component_property='value')]
)
def update_output_div(graph_update, input_value):
    return [html.H6(generate_table(df.drop(columns=['Cluster Scores', 'Latitude', 'Longitude'])))]


if __name__ == '__main__':
    app.run_server(debug=True)
