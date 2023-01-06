import os
import dash
import pandas as pd
import glob
from dash import Input, Output, dcc, html
from data_functions import football2D, get_events, invert_get_events, metrics, speed_areas, speed_time
from plot_functions import animation_2D, bar_plot, radar_chart, scatter_plot
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#  Path data
df_away = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv", skiprows=2)
df_home = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv", skiprows=2)
events_path = "./data/Sample_Game_1/Event.csv"
players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")

# Load data : radar_chart
events = get_events(events_path)
invert_events = invert_get_events(events)

# Load data : animation_2D
data_animation = football2D(df_home, df_away)

# Data subplot : scatter + bar
df_update_movement = metrics(players)
df_update_movement.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2

# Layout
app = dash.Dash(

        __name__,
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
        )
app.title = "Wind Speed Dashboard"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
        [
            # header
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("DASHBOARD + FOOTBALL2D ANIMATION", className="app__header__title"),
                            html.P(
                                "This application displays a dashboard for football. The Python language was used for the data processing part and the Dash and Plotly libraries for their visualization and interaction.",
                                className="app__header__title--grey",
                                ),
                            ],
                        className="app__header__desc",
                        ),
                    html.Div(
                        [
                            html.A(
                                html.Button("SOURCE CODE", className="link-button"),
                                href="https://github.com/jrm-muller/M2_AJBD_DASHBOARD",
                                target="_blank"
                                ),
                            ],
                        ),
                    ],
                className="app__header",
                ),

            html.Div([
                html.Div(
                    dcc.Dropdown(
                        id="dropdown",
                        placeholder="Sélectionner joueur...",
                        options=invert_events.columns,
                        value="Gael CLICHY",
                        clearable=False,
                        style=
                        {
                            "width": "100%",
                            }
                        ), className="link-button-3"),
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown2",
                            placeholder="Sélectionner joueur...",
                            options=invert_events.columns,
                            value="Alexis SANCHEZ",
                            clearable=False,
                            style=
                            {
                                "width": "100%",
                                }
                            ), className="link-button-3"),
                        dcc.Input(
                            id="time-min",
                            placeholder="Entrer début séquence...",
                            type="number",
                            value=0,
                            style=
                            {
                                "margin-right": "73px",
                                }
                            ),
                        dcc.Input(
                            id="time-max",
                            placeholder="Entrer fin de séquence...",
                            type="number",
                            value=5,
                            style={
                                'background-color': 'white',
                                }
                            ),
                        ], className="link-button-2"),
        html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [html.H6("SPEED OF MOVEMENT & DISTANCE/INTENSITY ZONE", className="graph__title")],
                                ),
                            dcc.Graph(id="graph2"),
                            dcc.Graph(id="graph3"),
                            ],
                        className="two-thirds column wind__speed__container",
                        ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "COMPARISON STATS PLAYERS",
                                                className="graph__title",
                                                )
                                            ]
                                        ),
                                    dcc.Graph(id="graph"),
                                    dcc.Interval(
                                        id="wind-speed-update",
                                        interval=int(GRAPH_INTERVAL),
                                        n_intervals=0,
                                        ),
                                    ],
                                className="graph__container first",
                                ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "ANIMATION FOOTBALL 2D", className="graph__title"
                                                )
                                            ]
                                        ),
                                    dcc.Graph(
                                        id="animation-2D",
                                        ),
                                    ],
                                className="graph__container second",
                                ),
                            ],
                        className="one-third column histogram__direction",
                        ),
                    ],
            className="app__content",
        ),
    ],
    className="app__container",
)

# Callback - Update plots

@app.callback(
        Output("graph2", "figure"),
        Output("graph3", "figure"),
        Input("dropdown", "value"),  # player1
        Input("dropdown2", "value"),  # player2
        Input("time-min", "value"),  # min
        Input("time-max", "value"),  # max
        )

def update_movement_speed(player1, player2, min, max):
    # Setup data
    speedP1 = speed_time(df_update_movement, min, max, player1)
    speedP2 = speed_time(df_update_movement, min, max, player2)

    areasP1 = speed_areas(df_update_movement, min, max, player1)
    areasP2 = speed_areas(df_update_movement, min, max, player2)

    # Load plots
    scatter = scatter_plot(speedP1, speedP2, player1, player2)
    bar = bar_plot(areasP1, areasP2, player1, player2)

    return scatter, bar

@app.callback(
        Output("animation-2D", "figure"),
        Input("time-min", "value"),  # min
        Input("time-max", "value"),  # max
        )

def update_animation_2D(min, max):
    # Load plot
    fig = animation_2D(data_animation, min, max)

    return fig

@app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"),  # player
        Input("dropdown2", "value"),  # player2
        )

def update_radar_chart(player, player2):
    # Setup data
    data = events[["Players", "Shot", "Dribble", "Foul", "Block", "Tackle", "Header"]]
    df_radar = invert_get_events(data)

    # Load plot
    fig = radar_chart(df_radar, player, player2)

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
