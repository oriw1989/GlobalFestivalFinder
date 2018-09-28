import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from festivalTools import *
import json
import pandas as pd

app = dash.Dash()
df = []

def generate_table(dataframe, max_rows=10, columnNames = True):

    if columnNames:
        table = [html.Tr([html.Th(col) for col in dataframe.columns])] + [html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))]

    else:

        table = [html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))]

    return html.Table(table)


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
                            'pk.eyJ1Ijoib3JpdzE5ODkiLCJhIjoiY2ptNzg3OGR0MDg0MzN3bn'
                            +'R2ZXNubjFidyJ9.4X65Eb3vkDZosAIbP9k5ZQ'
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

    global topEvents
    global bottomEvents

    df = getAllTopFestivals(input_value, "Brooklyn")
    topEvents = df[0:3]
    bottomEvents = df[-21:-19]

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
            'lat': topEvents['Latitude'], 'lon': topEvents['Longitude'],
            'text': topEvents['Date'] + "<br>" + topEvents['Event Name'] +
            ", " + topEvents['City'],
            'mode':'markers',
            'name': 'Go!',
            'color': 'Blue',
            'marker': dict(
            size=11
            ),
            'type': 'scattermapbox'
        },
        {
            'lat': bottomEvents['Latitude'], 'lon': bottomEvents['Longitude'],
            'text': bottomEvents['Date'] + "<br>" + bottomEvents['Event Name'] +
            ", " + bottomEvents['City'],
            'mode':'markers',
            'name': 'Do Not Go',
            'color': 'Red',
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

    return [html.H6(generate_table(topEvents.drop(columns=['Cluster Scores', 'Latitude', 'Longitude'])),
        style={'color': 'Blue'}),
        html.H6(generate_table(bottomEvents.drop(columns=['Cluster Scores', 'Latitude', 'Longitude']), columnNames=False),
        style={'color': 'Orange'})]


if __name__ == '__main__':
    app.run_server(debug=True)
