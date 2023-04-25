from dash import dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from threading import Timer

import numpy as np
import os, webbrowser, time

import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

locations = []
modifications = []
crashes = []

time_interval = 1000
fig = None
range_padding = 10
tick_interval = 5

normal_colors = ['lightSkyBlue']
mod_color = 'yellow'
crash_color = 'red'
    
def start_visualizer(loc_list: list, mod_dict: dict, crash_list: list):
    global locations, modifications, crashes

    locations = loc_list
    modifications = mod_dict
    crashes = crash_list

    create_graph()
    Timer(1, open_browser).start()
    app.run_server()
    

def create_graph():
    global app, locations, time_interval, fig, normal_colors
    
    acv_count = len(locations[0])
    normal_colors *= acv_count
    y = [(acv_count - 1) - i for i in range(acv_count)]

    trace = go.Scatter(x=locations[0], y=y, mode='markers', marker=dict(size=15, color='LightSkyBlue'), name="acvs")

    layout = go.Layout(
        title='ACV Simulation',
        xaxis=dict(
            title='Position', 
            tickmode = 'linear',
            dtick = tick_interval
        ),
        yaxis=dict(
            title='ACVs',
            type='category',
            categoryorder='total descending',
            tickmode='array',
            tickvals=y,
            ticktext=['ACV 0', 'ACV 1', 'ACV 2', 'ACV 3'],
        ),
        height=500,
        transition={
            'duration': time_interval / 3,
            'easing': 'cubic-in-out'
        }
    )

    fig = go.Figure(data=[trace], layout=layout)

    app.layout = html.Div([
        
        dcc.Graph(id='graph', figure=fig),
        html.Div(id='iteration', style={'font-size': '15px'}),
        dcc.Interval(
            id='data-update',
            interval=time_interval,  # in milliseconds
            disabled=True
        ),
        dcc.Interval(
            id='range-update',
            interval=time_interval,  # in milliseconds
            disabled=True
        ),
        dcc.Slider(
            id="year-slider",
            min=0,
            max=100,
            value=0,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": False}
        ),
        
        html.Button('Play', id='play', style={'width': '20%', 'margin-top': '5px'})
    ], style={'textAlign': 'center'})    

@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Output('year-slider', 'value'),
    Output('iteration', 'children'),
    Input('data-update', 'n_intervals'),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def update_data(n, value):
    index = value + 1

    if (index >= len(locations)):
        return dash.no_update, dash.no_update, dash.no_update

    x = locations[index]

    fig['data'][0]['x'] = x
    fig.update_yaxes(categoryorder='array', categoryarray= ['ACV 0', 'ACV 1', 'ACV 2', 'ACV 3'])

    colors = normal_colors.copy()
    
    # Dist Modifications
    if (index in modifications):
        change_index = modifications[index][0]
        colors[change_index] = mod_color

    # Crashes
    crash = [c for c in crashes if c[0] == index]
    if (crash != []):
        change_indices = crash[0][1][0]
        colors[change_indices[0]] = crash_color
        colors[change_indices[1]] = crash_color

    fig['data'][0]['marker']['color'] = colors

    return fig, index, "Iteration: " + str(index)


@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Input('range-update', 'n_intervals'),
    prevent_initial_call=True
)
def update_range(n):
    time.sleep(time_interval / 3000)
    x = np.copy(fig['data'][0]['x'])
    
    fig['layout']['xaxis']['range'] = pad_range(x)

    return fig


@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Output('iteration', 'children', allow_duplicate=True),
    Input('year-slider', 'value'),
    State('iteration', 'children'),
    prevent_initial_call='initial_duplicate'
)
def slider_update(value, iteration):
    if (iteration != None):
        iteration = int(iteration.split(" ")[1])
        if (iteration == value):
            return dash.no_update, dash.no_update

    index = value
    x = locations[index]
    fig['data'][0]['x'] = x
    fig['layout']['xaxis']['range'] = pad_range(x)
    fig.update_yaxes(categoryorder='array', categoryarray= ['ACV 0', 'ACV 1', 'ACV 2', 'ACV 3'])

    return fig, "Iteration: " + str(index)


@app.callback(
    Output("data-update", "disabled"),
    Output("range-update", "disabled"),
    Output("play", "children"),
    Input("play", "n_clicks"),
    State("data-update", "disabled"),
)
def toggle(n, playing):
    if n:
        paused = not playing
        text = "Play" if paused else "Pause" 

        return paused, paused, text
    else:
        return playing, playing, "Play"


def pad_range(records: list):
    minimum = min(records)
    maximum = max(records)

    return (minimum - range_padding, maximum + range_padding)

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    acv_vals = [[col_idx + row_idx for col_idx in range(5)] for row_idx in range(100)]
    start_visualizer(acv_vals)