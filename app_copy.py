import os
import dash
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, dcc, html
from function import football2D, get_events, invert_get_events

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
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("WIND SPEED (MPH)", className="graph__title")]
                        ),
                        dcc.Dropdown(
                            id="dropdown",
                            options=invert_events.columns,
                            value="Jack WILSHERE",
                            clearable=False,
                            ),
                        dcc.Dropdown(
                            id="dropdown2",
                            options=invert_events.columns,
                            value="Gael CLICHY",
                            clearable=False,
                            ),
                        dcc.Graph(id="graph2"),
                        dcc.Interval(
                            id="wind-speed-update-2",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                        dcc.Input(
                            id="time-min",
                            placeholder="Enter a value...",
                            type="number",
                            value=50,
                            ),
                        dcc.Input(
                            id="time-max",
                            placeholder="Enter a value...",
                            type="number",
                            value=51
                            ),
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
    Output("animation-2D", "figure"),
    Input("time-min", "value"),
    Input("time-max", "value"))

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
