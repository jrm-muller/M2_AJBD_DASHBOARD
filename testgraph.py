import glob
from numpy import trace
from plotly.express import scatter
import plotly.graph_objects as go
from function import metrics, speed_areas, speed_time
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Live adjustable subplot-width'),
    dcc.Graph(id="graph"),
    html.P("Subplots Width:"),
    dcc.Slider(
        id='my-slider', min=.1, max=.9,
        value=0.5, step=0.1)
])


@app.callback(
    Output("graph", "figure"),
    Input("my-slider", "value"))

def customize_width():
    players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")
    df = metrics(players)
    df.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2

    speedP1 = speed_time(df, 0, 10, "Aaron RAMSEY")
    speedP2 = speed_time(df, 0, 10, "Gael CLICHY")

    areas = ["z1", "z2", "z3", "z4", "z5"]
    areasP1 = speed_areas(df, 0, 10, "Aaron RAMSEY")
    areasP2 = speed_areas(df, 0, 10, "Gael CLICHY")

    fig = make_subplots (rows=2,cols=1, vertical_spacing=0.2,
                             specs=[[{"type": "scatter"}], [{"type": "bar"}]])

    fig.add_trace(go.Scatter(name="Aaron RAMSEY", x=speedP1["Time"], y=speedP1["Aaron RAMSEY_speed"]),
            row=1, col=1
        )

    fig.add_trace(go.Scatter(name="Gael CLICHY", x=speedP2["Time"], y=speedP2["Gael CLICHY_speed"]),
            row=1, col=1
        )

    fig.add_trace(go.Bar(name='Aaron RAMSEY', x=areas, y=areasP1),
                 row=2, col=1)

    fig.add_trace(go.Bar(name='Gael CLICHY', x=areas, y=areasP2),
                 row=2, col=1)

    fig.update_layout(barmode='group')

    # Change the bar mode
    fig.show()
    return fig


app.run_server(debug=True)




