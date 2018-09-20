import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from festivalTools import *
import json
import pandas as pd

app = dash.Dash()

app.layout = html.Div([
    html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
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
    )
], className="row")


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(
    Output('graph', 'figure'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):

    df = getTop10Festivals(input_value, "Brooklyn")


    #handle case of low results - simply leave map empty
    emptyFigure={
        'data': [{
            'lat': df['Latitude'], 'lon': df['Longitude'], 'text': df['Event Name'] + ", " + df['City']
            , 'type': 'scattermapbox'
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
            'lat': df['Latitude'], 'lon': df['Longitude'], 'text': df['Event Name'] + ", " + df['City']
            , 'type': 'scattermapbox'
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



if __name__ == '__main__':
    app.run_server(debug=True)
