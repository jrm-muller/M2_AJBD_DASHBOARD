import os
import dash
import pandas as pd
from plotly import animation
import plotly.graph_objects as go
import glob
from dash import Input, Output, dcc, html
from function import football2D, get_events, invert_get_events, metrics, speed_areas, speed_time
from plotly.subplots import make_subplots
import plotly.express as px

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

# Chargement des données de l'équipe à domicile
df_away = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv", skiprows=2)
df_home = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv", skiprows=2)
events_path = "./data/Sample_Game_1/Event.csv"

events = get_events(events_path)
invert_events = invert_get_events(events)

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
                            html.H4("DASHBOARD + TEST FOOTBALL2D ANIMATION", className="app__header__title"),
                            html.P(
                                "This app continually queries a SQL database and displays live charts of wind speed and wind direction.",
                                className="app__header__title--grey",
                                ),
                            ],
                        className="app__header__desc",
                        ),
                    html.Div(
                        [
                            html.A(
                                html.Button("SOURCE CODE", className="link-button"),
                                href="https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-wind-streaming",
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
                    value=None,
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
                    value=None,
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
                    value=None,
                    style=
                    {
                        "margin-right": "73px",
                        }
                    ),
                dcc.Input(
                    id="time-max",
                    placeholder="Entrer fin de séquence...",
                    type="number",
                    value=None,
                    style={
                      'background-color': 'white',
                     }
                    ),
                ], className="link-button-2"),
        html.Div(
                [
                    # wind speed
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
                            # histogram
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
                            # wind direction
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
                                        # figure=football2D(df_home, df_away, 50, 55)
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
@app.callback(
        Output("graph2", "figure"),
        Input("dropdown", "value"),
        Input("dropdown2", "value"),
        Input("time-min", "value"),
        Input("time-max", "value"),
        )

def update_movement(player1, player2, min, max):

    players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")
    df = metrics(players)
    df.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2

    speedP1 = speed_time(df, min, max, player1)
    speedP2 = speed_time(df, min, max, player2)
    print(speedP1.columns)
    # Plot
    # fig = go.Figure(data=[
        #     go.Scatter(go.Scatter(name=player1, x=speedP1[f"{player1}_x"], y=speedP1[f"{player1}_y"], mode="markers",
                                    #                           marker= dict(size=1, color=['#d7e832' if s < 6 else '#d043de' for s in speedP1[f"{player1}_speed"]]))),
        #     go.Scatter(go.Scatter(name=player2, x=speedP2[f"{player2}_x"], y=speedP2[f"{player2}_y"])),
        #     ])

    # Change the bar mode
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=player1, x=speedP1["Time"], y=speedP1[f"{player1}_speed"]),
                  )

    fig.add_trace(go.Scatter(name=player2, x=speedP2["Time"], y=speedP2[f"{player2}_speed"]),
                  )
    fig.update_layout(barmode="group", template="plotly_dark",
                      )

    return fig

@app.callback(
        Output("graph3", "figure"),
        Input("dropdown", "value"),
        Input("dropdown2", "value"),
        Input("time-min", "value"),
        Input("time-max", "value"),
        )

def update_speed_areas(player1, player2, min, max):

    players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")
    df = metrics(players)
    df.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2

    areas = ["z1", "z2", "z3", "z4", "z5"]
    areasP1 = speed_areas(df, min, max, player1)
    areasP2 = speed_areas(df, min, max, player2)

    fig = go.Figure(data=[
        go.Bar(go.Bar(name=player1, x=areas, y=areasP1)),
        go.Bar(go.Bar(name=player2, x=areas, y=areasP2)),
        ])

    # Change the bar mode

    fig.update_layout(barmode="group", template="plotly_dark",
                      height=516
                      )

    return fig
# def update_speed_areas(player1, player2, min, max):
#
#     players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")
#     df = metrics(players)
#     df.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2
#
#     speedP1 = speed_time(df, min, max, player1)
#     speedP2 = speed_time(df, min, max, player2)
#
#     areas = ["z1", "z2", "z3", "z4", "z5"]
#     areasP1 = speed_areas(df, min, max, player1)
#     areasP2 = speed_areas(df, min, max, player2)
#
#     fig = make_subplots (rows=2,cols=1, vertical_spacing=0.2,
                           #                              specs=[[{"type": "scatter"}], [{"type": "bar"}]])
#
#     fig.add_trace(go.Scatter(name=player1, x=speedP1["Time"], y=speedP1[f"{player1}_speed"]),
                    #             row=1, col=1
                    #         )
#
#     fig.add_trace(go.Scatter(name=player2, x=speedP2["Time"], y=speedP2[f"{player2}_speed"]),
                    #             row=1, col=1
                    #         )
#
#     fig.add_trace(go.Bar(name=player1, x=areas, y=areasP1),
                    #                  row=2, col=1)
#
#     fig.add_trace(go.Bar(name=player2, x=areas, y=areasP2),
                    #                  row=2, col=1)
#
#     fig.update_layout(template="plotly_dark",
                        #                       height=700,
                        #                       )
#
#     return fig

@app.callback(
        Output("animation-2D", "figure"),
        Input("time-min", "value"),
        Input("time-max", "value")
        )

def update_animation_2D(min, max):
    df_away = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv", skiprows=2)
    df_home = pd.read_csv("./data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv", skiprows=2)
    fig=football2D(df_home, df_away, min, max)
    return fig

@app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"),
        Input("dropdown2", "value"))

def update_radar_chart(player, player2):

    df = get_events(events_path)
    df = df[["Players", "Shot", "Dribble", "Foul", "Block", "Tackle", "Header",]]
    df = invert_get_events(df)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df[player],
        theta=df.index,
        fill='toself',
        name=player,
        ))
    fig.add_trace(go.Scatterpolar(
        r=df[player2],
        theta=df.index,
        fill='toself',
        name=player2
        ))
    fig.update_layout(
            template="plotly_dark",
            polar=dict(
                radialaxis=dict(
                    visible=True
                    ),
                ),
            # showlegend=False
            )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
