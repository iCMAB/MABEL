from dash import dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import os, webbrowser, time
from threading import Timer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
fig = None

records = [[col_idx + row_idx for col_idx in range(5)] for row_idx in range(100)]
y = [4-i for i in range(5)]
time_interval = 1000

trace = go.Scatter(x=records[0], y=y, mode='markers', marker=dict(size=15, color='LightSkyBlue'), name="acvs")

layout = go.Layout(
    title='ACV Simulation',
    xaxis=dict(
        title='Position', 
        tickmode = 'linear',
        dtick = 0.5
    ),
    yaxis=dict(
        title='ACVs',
        type='category',
        categoryorder='total descending',
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4],
        ticktext=['ACV 0', 'ACV 1', 'ACV 2', 'ACV 3', 'ACV 4']
    ),
    height=500,
    transition={
        'duration': time_interval / 2.5,
        'easing': 'cubic-in-out'
    }
)

fig = go.Figure(data=[trace], layout=layout)

app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
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
    html.Div(id='iteration', style={'margin-top': 20}),
    html.Button('Play', id='play')
])    

@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Output('iteration', 'children'),
    Output('year-slider', 'value'),
    Input('data-update', 'n_intervals'),
    State('year-slider', 'value'),
    prevent_initial_call=True
)
def update_data(n, value):
    index = value + 1
    x = records[index]

    fig['data'][0]['x'] = x

    return fig, index, index

@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Input('range-update', 'n_intervals'),
    prevent_initial_call='initial_duplicate'
)
def update_range(n):
    time.sleep(time_interval / 4000)
    x = np.copy(fig['data'][0]['x'])
    
    fig['layout']['xaxis']['range'] = (x[0]-5, x[len(x)-1]+5)

    return fig

@app.callback(
    Output('graph', 'figure', allow_duplicate=True), 
    Output('iteration', 'children', allow_duplicate=True),
    Input('year-slider', 'value'),
    State('iteration', 'children'),
    prevent_initial_call=True
)
def slider_update(value, iteration):
    if (iteration == value):
        return dash.no_update, dash.no_update

    index = value
    x = records[index]
    fig['data'][0]['x'] = x
    fig['layout']['xaxis']['range'] = (x[0]-5, x[len(x)-1]+5)

    return fig, index
        

@app.callback(
    Output("data-update", "disabled"),
    Output("range-update", "disabled"),
    Output("play", "children"),
    Input("play", "n_clicks"),
    State("data-update", "disabled"),
)
def toggle(n, playing):
    if n:
        state = not playing
        text = "Play" if state else "Pause" 

        return state, state, text
    else:
        return playing, playing, "Play"

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)