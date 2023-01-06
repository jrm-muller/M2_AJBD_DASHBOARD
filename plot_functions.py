import plotly.express as px
import plotly.graph_objects as go

def animation_2D(dataframe, time_min, time_max):

    df = dataframe

    df = df[(df['Time [min]'] >= time_min) & (df['Time [min]'] <= time_max)]

    # create plot with plotly.express
    fig = px.scatter(df, x="x", y="y", animation_frame="Time [min]", color="team",
                     animation_group="player", template="plotly_dark",
                     # width=800, height=600, size="size", text="player"
                     )
    fig.update_layout(
            xaxis_range=[-0.1, 1.1],
            yaxis_range=[-0.1, 1.1],
            yaxis=dict(
                title_text = "test"
                ),
            autosize=True,
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
    fig = go.Figure()
    fig.add_trace(go.Scatter(name=player1, x=df["Time"], y=df[f"{player1}_speed"]),
                  )

    fig.add_trace(go.Scatter(name=player2, x=df2["Time"], y=df2[f"{player2}_speed"]),
                  )
    fig.update_layout(barmode="group", template="plotly_dark",
                      )
    return fig

def bar_plot(df, df2, player1, player2):

    areas = ["z1", "z2", "z3", "z4", "z5"]

    fig = go.Figure(data=[
        go.Bar(go.Bar(name=player1, x=areas, y=df)),
        go.Bar(go.Bar(name=player2, x=areas, y=df2)),
        ])

    fig.update_layout(barmode="group", template="plotly_dark",
                      height=516
                      )
    return fig

def radar_chart(df, player, player2):

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
            )
    return fig
