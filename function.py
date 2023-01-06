import glob
"""
=========
Animation
=========

This example shows how to animate tracking data from
`metricasports <https://github.com/metrica-sports/sample-data>`_.
"""

import numpy as np
import pandas as pd
import plotly.express as px

# Renommer les colomnes pour avoir x and y en suffixes
def set_col_names(df):
    """ Renames the columns to have x and y suffixes."""
    cols = list(np.repeat(df.columns[3::2], 2))
    cols = [col+'_x' if i % 2 == 0 else col+'_y' for i, col in enumerate(cols)]
    cols = np.concatenate([df.columns[:3], cols])
    df.columns = cols

# Convertir mon fichier de format long à wide
def to_long_form(df):
    """ Pivots a dataframe from wide-form (each player as a separate column) to long form (rows)"""
    df = pd.melt(df, id_vars=df.columns[:3], value_vars=df.columns[3:], var_name='player')
    df.loc[df.player.str.contains('_x'), 'coordinate'] = 'x'
    df.loc[df.player.str.contains('_y'), 'coordinate'] = 'y'
    df = df.dropna(axis=0, how='any')
    df['player'] = df.player.str[6:-2]
    df = (df.set_index(['Period', 'Frame', 'Time [min]', 'player', 'coordinate'])['value']
          .unstack()
          .reset_index()
          .rename_axis(None, axis=1))
    return df

# Créer une animation 2D du match à partir des données de position des joueurs
def football2D(home_file, away_file, time_min, time_max):
    # Chargement des données de l'équipe adverse
    df_away = away_file
    df_away.sort_values('Time [s]', inplace=True)

    # Chargement des données de l'équipe à domicile
    df_home = home_file
    df_home.sort_values('Time [s]', inplace=True)

    # Reset les noms de colonnes
    set_col_names(df_home)
    set_col_names(df_away)
    df = pd.merge(df_home, df_away)

    df["Time [s]"] = df["Time [s]"] * 0.015517241
    df.rename({"Time [s]" : "Time [min]"}, axis=1, inplace=True)

    # Calculer la moyenne des valeurs de x et y tous les 25 éléments (25Hz)
    n = 20
    df_mean = pd.DataFrame(df.groupby(np.arange(len(df))//n).mean())

    ##############################################################################
    # Subset 2 seconds of data
    df_mean = df_mean[(df_mean['Time [min]'] >= time_min) & (df_mean['Time [min]'] <= time_max)].copy()

    df_mean.to_csv("./data/Sample_Game_1/df_mean.csv")

    df_mean.rename(columns={'Ball_x':'Player30_x', 'Ball_y':'Player30_y'}, inplace=True)

    # Convertir les dotaframes en format long pour que chaques lignes correspondent aux coordonnées d'un joueur pour une seule frame
    df_mean = to_long_form(df_mean)
    df_mean.to_csv("./trash.csv")
    df = df_mean
    df_mean = df_mean.astype({'player': 'float'})

    # create a list of our conditions
    conditions = [
        (df_mean['player'] <= 14),
        (df_mean['player'] > 14) & (df_mean['player'] <= 29),
        (df_mean['player'] == 30)
        ]

    # create a list of the values we want to assign for each condition
    values = ['home', 'away', 'ball']

    # create a new column and use np.select to assign values to it using our lists as arguments
    df_mean['team'] = np.select(conditions, values)
    df_mean['size'] = np.where(df_mean['player'] != 30, 0.5, 0.2)
    df_mean.to_csv("./data/Sample_Game_1/df_mean.csv")
    df_mean["Time [min]"] = round(df_mean["Time [min]"], 2)

    # create plot with plotly.express
    fig = px.scatter(df_mean, x="x", y="y", animation_frame="Time [min]", color="team",
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

# Obtenir les events pour tous les joueurs
def get_events(csv_path):
    df = pd.read_csv(csv_path, delimiter=",")

    cols = df["EventName"].unique()
    players = df["Player1Name"].unique()
    df_events = pd.DataFrame(0, index=players, columns=cols, )
    df_events.insert(0, "Players", players)

    for i in range(0, len(df)):
        index = df_events.index[df_events["Players"] == df["Player1Name"][i]].tolist()
        df_events.loc[index, df["EventName"][i]] += 1
    return df_events

def invert_get_events(dataframe):
    df = dataframe
    df = df.T
    df = df.rename(columns={np.nan: 'type'})
    df.drop(index="Players", axis=0, inplace=True)
    df.to_csv("./trash.csv")
    df = df.astype("int")
    return df

def metrics(dataFiles):
    df = pd.DataFrame()
    # lire l'ensemble des fichiers de notre listData
    for files in dataFiles:
        csv = pd.read_csv(f"{files}", delimiter=",")

        # récupérer le nom des joueurs
        playerName = csv.loc[1, "Player1Name"]

        # calculer la distance de course parcourue
        dist = np.sqrt(np.diff(csv["XPos"])**2 + np.diff(csv["Ypos"])**2)

        # calculer la vitesse
        vit = (dist/0.1)*3.6

        # calculer le temps de jeu pour
        csv.loc[csv["Half"] == "First Half", "Time"] = csv["Time"]/60
        csv.loc[csv["Half"] == "Second Half", "Time"] = (csv["Time"]/60)+45

        df["Time"] = csv["Time"]
        df[f"{playerName}_x"] = csv["XPos"]
        df[f"{playerName}_y"] = csv["Ypos"]
        df[f"{playerName}_dist"] = pd.Series(dist)
        df[f"{playerName}_speed"] = pd.Series(vit)
    return df

def speed_time(dataframe, min, max, player_name):
    df = dataframe

    # Récupérer les données du joueur sélectionné
    df = [df["Time"], df.filter(like=player_name)]

    # Faire un nouveau dataframe à partir de ces données
    df = pd.concat(df, axis=1) # new dataframe player select

    # Sélectionner les données par rapport à la séquence de temps choisie en paramètre
    df = df.loc[(df["Time"] >= min) & (df["Time"] <= max)]

    return df

def speed_areas(dataframe, min, max, player_name):
    df = dataframe

    # Récupérer les données du joueur sélectionné
    df = [df["Time"], df.filter(like=player_name)]

    # Faire un nouveau datafram0e à partir de ces données
    df = pd.concat(df, axis=1) # new dataframe player select

    # Sélectionner les données par rapport à la séquence de temps choisie en paramètre
    df = df.loc[(df["Time"] >= min) & (df["Time"] <= max)]

    # z1 = df.loc[df[f"{player_name}_speed"] < 6, f"{player_name}_dist"].sum(axis=0) # une méthode classique qui peut être utilisé
    z1 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y < 6), 2)
    z2 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 6 and y < 10), 2)
    z3 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 10 and y < 14), 2)
    z4 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 14 and y < 20), 2)
    z5 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 20), 2)

    return z1, z2, z3, z4, z5
