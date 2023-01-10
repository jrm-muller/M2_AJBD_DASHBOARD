from re import template
import plotly.express as px
import plotly.graph_objects as go

def animation_2D(dataframe, time_min, time_max):
    df = dataframe

    # Sélectionner les données à utiliser en fonction de la séquence de jeu définie
    df = df[(df['Time [min]'] >= time_min) & (df['Time [min]'] <= time_max)]

    # Créeer le plot
    fig = px.scatter(df, x="x", y="y", animation_frame="Time [min]", color="team",
                     animation_group="player", template="plotly_dark",
                     # width=800, height=600, size="size", text="player"
                     )
    # Update layout du plot
    fig.update_layout(
            yaxis_range=[-0.1, 1.1],
            xaxis_range=[-0.1, 1.1],
            yaxis=dict(
                title_text = "test"
                ),
            autosize=True,
            legend_title="Teams",
            font=dict(
                family="Open Sans, sans-serif",
                size=10,
                color="#CBCBCB"
                )
            )

    fig.add_shape(type="rect",
                  xref="x domain", yref="y domain",
                  x0=0.1, x1=0.9, y0=0.1, y1=0.9,
                  )
    #x axis
    fig.update_xaxes(visible=False)

    #y axis
    fig.update_yaxes(visible=False)

    return fig

def scatter_plot(df, df2, player1, player2):
    # Créer le plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(name=player1, x=df["Time"], y=df[f"{player1}_speed"]),
                  )

    fig.add_trace(go.Scatter(name=player2, x=df2["Time"], y=df2[f"{player2}_speed"]),
                  )

    # Update layout du plot
    fig.update_layout(
            barmode="group",
            template="plotly_dark",
            title="Speed of movement of the players during the defined sequence",
            xaxis_title="Time (min)",
            yaxis_title="Speed (km/h)",
            legend_title="Players",
            font=dict(
                family="Open Sans, sans-serif",
                size=10,
                color="#CBCBCB"  #506070
                )
            )

    return fig

def bar_plot(df, df2, player1, player2):
    # Définir les valeurs pour x
    areas = ["z1", "z2", "z3", "z4", "z5"]

    # Créer le plot
    fig = go.Figure(data=[
        go.Bar(go.Bar(name=player1, x=areas, y=df)),
        go.Bar(go.Bar(name=player2, x=areas, y=df2)),
        ])

    # Update layout du plot
    fig.update_layout(
            barmode="group",
            template="plotly_dark",
            height=519,
            title="Distance covered according to running intensity",
            xaxis_title="Time (min)",
            yaxis_title="Distance (m)",
            legend_title="Players",
            font=dict(
                family="Open Sans, sans-serif",
                size=10,
                color="#CBCBCB"
                )
            )
    return fig

def radar_chart(df, player, player2):
    # Créer le plot
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

    # Update layout du plot
    fig.update_layout(
            barmode="group",
            template="plotly_dark",
            title="Event statistics for the whole match",
            legend_title="Players",
            font=dict(
                family="Open Sans, sans-serif",
                size=10,
                color="#CBCBCB"
                )
            )
    return fig

def events_position(data):
    # Créer le plot
    fig = px.scatter(data, x="XPosOrigin", y="YPosOrigin")
    fig.update_layout(
            yaxis_range=[-34, 34],
            xaxis_range=[-55, 55],
            template="plotly_dark",
            )
    return fig
