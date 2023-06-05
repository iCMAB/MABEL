from dash import dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from threading import Timer

import numpy as np
import os, webbrowser, time

import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, update_title='Loading...')

locations = []
speeds = []
distances = []
ignores = []
modifications = []
crashes = []

time_interval = 1000
fig = None
range_padding = 15
tick_interval = 5

normal_colors = ['lightSkyBlue']
mod_color = 'yellow'
crash_color = 'red'
ignore_color = 'green'
marker_stroke = 3
    
def start_visualizer(loc_list: list, speed_list: dict, dist_list: dict, ignore_list: dict, mod_dict: dict, crash_list: list, model_name: str):
    global locations, speeds, distances, ignores, modifications, crashes

    locations = loc_list
    speeds = speed_list
    distances = dist_list
    ignores = ignore_list
    modifications = mod_dict
    crashes = crash_list

    create_graph(model_name)
    Timer(1, open_browser).start()
    app.run(host='0.0.0.0')
    

def create_graph(model_name: str):
    global app, locations, time_interval, fig, normal_colors
    
    acv_count = len(locations[0])
    total_iterations = len(locations)
    normal_colors *= acv_count
    y = [(acv_count - 1) - i for i in range(acv_count)]

    trace = go.Scatter(
        name="acvs",
        x=locations[0], 
        y=y, mode='markers', 
        customdata=[[speeds[0][i], distances[0][i], "Unmodified", ""] for i in range(acv_count)],
        marker=dict(
            size=25, 
            color='lightSkyBlue',
            symbol="arrow-right",
            line=dict(
                width=0,
                color=crash_color
            )
        ),
        hovertemplate=
        '<b>%{y}</b>' +
        '<br>Position: %{x}' +
        '<br>Speed: %{customdata[0]}' +
        '<br>Dist Sensor: %{customdata[1]}' +
        '<br>%{customdata[2]}' +
        '<br>%{customdata[3]}' +
        '<extra></extra>'
    )

    layout = go.Layout(
        title=dict(
            text='MABEL Simulation - ' + model_name,
            font=dict(size=20)
        ),
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
        transition={
            'duration': time_interval / 3,
            'easing': 'cubic-in-out'
        },
    )

    fig = go.Figure(data=[trace], layout=layout)

    app.layout = html.Div([
        dcc.Graph(id='graph', figure=fig, style={'height': '70vh'}),
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
            max=total_iterations,
            value=0,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": False}
        ),
        html.Button('<<', id='backward', style={'width': '5%', 'margin-top': '5px'}),
        html.Button('Play', id='play', style={'width': '20%', 'margin-top': '5px'}),
        html.Button('>>', id='forward', style={'width': '5%', 'margin-top': '5px'}),
        html.Br(),
        html.Button('Skip to Next Modification', id='skip', style={'width': '15%', 'margin-top': '25px', 'text-align': 'center'}),
    ], style={'textAlign': 'center'})    

@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Output('year-slider', 'value'),
    Output('iteration', 'children'),
    Input('data-update', 'n_intervals'),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def data_update(n, value):
    index = value + 1

    if (index >= len(locations)):
        return dash.no_update, dash.no_update, dash.no_update

    new_iteration_data_update(index)

    return fig, index, "Iteration: " + str(index)


@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Input('range-update', 'n_intervals'),
    Input('year-slider', 'value'),
    prevent_initial_call='initial_duplicate'
)
def update_range(n, value):
    time.sleep(time_interval / 3000)
    x = np.copy(fig['data'][0]['x'])

    range = (min(x) - range_padding, max(x) + range_padding)

    fig['layout']['xaxis']['range'] = range

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
    new_iteration_data_update(index)

    return fig, "Iteration: " + str(index)


@app.callback(
    Output("data-update", "disabled"),
    Output("range-update", "disabled"),
    Output("play", "children"),
    Input("play", "n_clicks"),
    State("data-update", "disabled"),
    prevent_initial_call=True
)
def toggle_play(n, playing):
    if n:
        paused = not playing
        text = "Play" if paused else "Pause" 

        return paused, paused, text
    else:
        return dash.no_update, dash.no_update, dash.no_update

@app.callback(
    Output('year-slider', 'value', allow_duplicate=True),
    Input("forward", "n_clicks"),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def forward(n, value):
    if (n):
        return value + 1
    else:
        return dash.no_update

@app.callback(
    Output('year-slider', 'value', allow_duplicate=True),
    Input("backward", "n_clicks"),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def backward(n, value):
    if (n):
        return value - 1
    else:
        return dash.no_update

@app.callback(
    Output('year-slider', 'value', allow_duplicate=True),
    Input("skip", "n_clicks"),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def skip(n, value):
    if (n):
        greater_mods = filter(lambda k: k > value, modifications.keys())
        next_mod = next(greater_mods, None)

        result = next_mod if next_mod is not None else dash.no_update
        return result
    else:
        return dash.no_update

def new_iteration_data_update(index: int):
    x = locations[index]
    spd = speeds[index]
    dist = distances[index]
    mods = ["Unmodified"] * len(spd)
    ignr = [""] * len(spd)

    fig.update_yaxes(categoryorder='array', categoryarray= ['ACV 0', 'ACV 1', 'ACV 2', 'ACV 3'])

    colors = normal_colors.copy()
    line_widths = [0] * len(x)
    
    # Dist Modifications
    if (index in modifications):
        change_index = modifications[index][0]

        mod_text = "<b>Sensor modified</b> (x" + str(modifications[index][1]) + ")"
        ignore_text = ""
        new_color = mod_color

        ignored = True if change_index in ignores[index] else False 
        if (ignored):
            new_color = ignore_color
            ignore_text = "<b>Sensor value ignored</b>"
            
        colors[change_index] = new_color
        mods[change_index] = mod_text
        ignr[change_index] = ignore_text

    # Crashes
    crash = [c for c in crashes if c[0] == index]
    if (crash != []):
        change_indices = crash[0][1][0]
        line_widths[change_indices[0]] = marker_stroke
        line_widths[change_indices[1]] = marker_stroke

    dist[0] = 'N/A'

    fig['data'][0]['customdata'] = [[spd[i], dist[i], mods[i], ignr[i]] for i in range(len(spd))]
    fig['data'][0]['marker']['color'] = colors
    fig['data'][0]['marker']['line']['width'] = line_widths
    fig['data'][0]['x'] = x

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    acv_vals = [[col_idx + row_idx for col_idx in range(5)] for row_idx in range(100)]
    start_visualizer(acv_vals, None, None, "TEST")