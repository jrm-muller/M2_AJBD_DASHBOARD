from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from function import get_events, invert_get_events, set_col_names
import glob
from functools import reduce

def motion_speed_dist(path_home, path_away):
    speed = pd.DataFrame()
    distance = pd.DataFrame()

    # Chargement des données de l'équipe à domicile
    df_away = pd.read_csv(path_away, skiprows=2)
    df_home = pd.read_csv(path_home, skiprows=2)

    # Chargement des données de l'équipe adverse
    df_away.sort_values('Time [s]', inplace=True)

    # Chargement des données de l'équipe à domicile
    df_home.sort_values('Time [s]', inplace=True)

    # Reset les noms de colonnes
    set_col_names(df_home)
    set_col_names(df_away)
    df = pd.merge(df_home, df_away)

    df["Time [s]"] = df["Time [s]"] * 0.015517241
    df.rename({"Time [s]" : "Time [min]"}, axis=1, inplace=True)

    for n in range(1, 29):
        numero = str(n)
        dist = np.sqrt(np.diff(df[f"Player{numero}_x"])**2 + np.diff(df[f"Player{numero}_y"])**2)
        distance[f"Player{numero}_dist"] = dist
        speed[f"Player{numero}_speed"] = (dist/np.diff(df["Time [min]"])*3.6)

    objs = [df["Time [min]"], df["Player10_x"], df["Player10_y"], speed, distance]
    df = pd.concat(objs, axis=1)
    df.drop(71267, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2
    return df

# Retourner un csv avec le temps + une colonne x, y, distance/frame, vitesse/frame
def metrics(dataFiles):
    df = pd.DataFrame()
    # lire l'ensemble des fichiers de notre listData
    for files in dataFiles:
        csv = pd.read_csv(f"{files}", delimiter=",")

        # récupérer le nom des joueurs
        playerName = csv.loc[1, "Player1Name"]

        # calculer la distance de course parcourue
        dist = np.sqrt(np.diff(csv["XPos"])**2 + np.diff(csv["Ypos"])**2)

        # calculer la vitesse (aucun intérêt pour l'instant)
        vit = (dist/0.1)*3.6

        # calculer le temps de jeu pour
        time = sum(np.diff(csv["Time"]))

        df["Time"] = csv["Time"]
        df[f"{playerName}_x"] = csv["XPos"]
        df[f"{playerName}_y"] = csv["Ypos"]
        df[f"{playerName}_dist"] = pd.Series(dist)
        df[f"{playerName}_speed"] = pd.Series(vit)
    return df

players = glob.glob("./data/Sample_Game_1/players/*Trajectory.csv")
test = metrics(players)
test.drop(27646, axis=0, inplace=True) # Transition des données entre la MT1 et la MT2

# Bar chart = nom de la zon de vitesse en x et sa valeur en y
# Line chart = besoin de x et y

def speed_areas(dataframe, min, max, player_name):
    df = dataframe

    # Récupérer les données du joueur sélectionné
    df = [df["Time"], df.filter(like=player_name)]

    # Faire un nouveau dataframe à partir de ces données
    df = pd.concat(df, axis=1) # new dataframe player select

    # Récupérer le temps de jeu du joueur
    tPlay = round(sum(np.diff(df["Time"]))/60, 2)

    # Mettre le temps de jeu en minute
    df["Time"] = df["Time"]/60

    # Sélectionner les données par rapport à la séquence de temps choisie en paramètre
    df = df.loc[(df["Time"] >= min) & (df["Time"] <= max)]

    # z1 = df.loc[df[f"{player_name}_speed"] < 6, f"{player_name}_dist"].sum(axis=0) # une méthode classique qui peut être utilisé
    z1 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y < 6), 2)
    z2 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 6 and y < 10), 2)
    z3 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 10 and y < 14), 2)
    z4 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 14 and y < 20), 2)
    z5 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 20), 2)

    return [z1, z2, z3, z4, z5]

test = speed_areas(test, 0, 30, "Aaron RAMSEY")
