from dash import dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import os, webbrowser, time
from threading import Timer

app = dash.Dash(__name__)

x = [i for i in range(5)]
y = [4-i for i in range(5)]
interval = 1000

trace = go.Scatter(x=x, y=y, mode='markers', marker=dict(size=15, color='LightSkyBlue'), name="acvs")

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
        'duration': interval / 2.5,
        'easing': 'cubic-in-out'
    }
)

fig = go.Figure(data=[trace], layout=layout)

app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
    dcc.Interval(
        id='data-update',
        interval=interval,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='range-update',
        interval=interval,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('graph', 'figure', allow_duplicate=True), [Input('data-update', 'n_intervals')], prevent_initial_call=True)
def update_data(n):
    x = np.copy(fig['data'][0]['x'])
    x = np.add(x, np.ones(5))

    fig['data'][0]['x'] = x

    return fig

@app.callback(Output('graph', 'figure'), [Input('range-update', 'n_intervals')])
def update_range(n):
    time.sleep(0.1)
    x = np.copy(fig['data'][0]['x'])
    
    fig['layout']['xaxis']['range'] = (x[0]-3, x[len(x)-1]+3)

    return fig

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)