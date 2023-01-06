from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.tools import make_subplots
from t import motion_speed_dist, speed_areas

path_away="./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv"
path_home = "./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv"


app = Dash(__name__)


app.layout = html.Div([
    html.H4('Animated GDP and population over decades'),
    html.P("Select an animation:"),
    dcc.Graph(
        id="graph"
        ),
    dcc.Slider(
        id="my-slider",
        min=0,
        max=5,
        step=0.5,
        value=10,
        ),
])



@app.callback(
    Output("graph", "figure"),
    Input("my-slider", "value"))

def update_chart_slider(min, max):
    test = motion_speed_dist(path_home, path_away)
    print(speed_areas(test, 0, 90, "Player10"))
    # importer le jeu de données que je vais utiliser
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
            go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            row=1, col=1
        )

    fig.add_trace(
            go.Bar(x=[1, 2, 3], y=[4, 5, 6]),
            row=2, col=1
        )

    return fig

def display_animated_graph(selection):
    df = px.data.gapminder() # replace with your own data source
    animations = {
        'GDP - Scatter': px.scatter(
            df, x="gdpPercap", y="lifeExp", animation_frame="year",
            animation_group="country", size="pop", color="continent",
            hover_name="country", log_x=True, size_max=55,
            range_x=[100,100000], range_y=[25,90]),
        'Population - Bar': px.bar(
            df, x="continent", y="pop", color="continent",
            animation_frame="year", animation_group="country",
            range_y=[0,4000000000]),
    }
    return animations[selection]


app.run_server(debug=True)
