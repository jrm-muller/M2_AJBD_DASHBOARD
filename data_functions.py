import numpy as np
import pandas as pd

# Renommer les colonnes pour avoir x and y en suffixes
def set_col_names(df):
    cols = list(np.repeat(df.columns[3::2], 2))
    cols = [col+'_x' if i % 2 == 0 else col+'_y' for i, col in enumerate(cols)]
    cols = np.concatenate([df.columns[:3], cols])
    df.columns = cols

# Convertir mon fichier de format long à wide
def to_long_form(df):
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
def football2D(home_file, away_file):
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

    # Passer le temps sur 90 min
    df["Time [s]"] = df["Time [s]"] * 0.015517241
    df.rename({"Time [s]" : "Time [min]"}, axis=1, inplace=True)

    # Calculer la moyenne des valeurs de x et y tous les 25 éléments (25Hz)
    n = 20
    df_mean = pd.DataFrame(df.groupby(np.arange(len(df))//n).mean())

    # Renommer nom de colonne player30 pour Ball
    df_mean.rename(columns={'Ball_x':'Player30_x', 'Ball_y':'Player30_y'}, inplace=True)

    # Convertir les dotaframes en format long pour que chaques lignes correspondent aux coordonnées d'un joueur pour une seule frame
    df_mean = to_long_form(df_mean)
    df_mean = df_mean.astype({'player': 'float'})

    # Créer une liste des conditions
    conditions = [
            (df_mean['player'] <= 14),
            (df_mean['player'] > 14) & (df_mean['player'] <= 29),
            (df_mean['player'] == 30)
            ]

    # créer une liste de valeurs que nous voulons assigner for chaque condition
    values = ['home', 'away', 'ball']

    # créer une nouvelle colonn et utiliser np.select pour lui attribuer sa valeur en utilisant nos listes comme arguments
    df_mean['team'] = np.select(conditions, values)
    df_mean['size'] = np.where(df_mean['player'] != 30, 0.5, 0.2)
    df_mean["Time [min]"] = round(df_mean["Time [min]"], 2)

    return df_mean


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

# Setup get_events pour notre radar
def invert_get_events(dataframe):
    df = dataframe
    df = df.T
    df = df.rename(columns={np.nan: 'type'})
    df.drop(index="Players", axis=0, inplace=True)
    df = df.astype("int")

    return df

# créer une dataframe avec le temps, les coordonnées, la distance + vitesse entre deux frames pour l'ensemble des joueurs
def metrics(dataFiles):
    # Data
    df = pd.DataFrame()

    # Lire l'ensemble des fichiers de notre listData
    for files in dataFiles:
        csv = pd.read_csv(f"{files}", delimiter=",")

        # Récupérer le nom des joueurs
        playerName = csv.loc[1, "Player1Name"]

        # Calculer la distance de course parcourue
        dist = np.sqrt(np.diff(csv["XPos"])**2 + np.diff(csv["Ypos"])**2)

        # Calculer la vitesse
        vit = (dist/0.1)*3.6

        # Mettre le temps de jeu en min
        csv.loc[csv["Half"] == "First Half", "Time"] = csv["Time"]/60
        csv.loc[csv["Half"] == "Second Half", "Time"] = (csv["Time"]/60)+45

        df["Time"] = csv["Time"]
        df[f"{playerName}_x"] = csv["XPos"]
        df[f"{playerName}_y"] = csv["Ypos"]
        df[f"{playerName}_dist"] = pd.Series(dist)
        df[f"{playerName}_speed"] = pd.Series(vit)

    return df

def speed_time(dataframe, min, max, player_name):
    # Data
    df = dataframe

    # Récupérer les données du joueur sélectionné
    df = [df["Time"], df.filter(like=player_name)]

    # Faire un nouveau dataframe à partir de ces données
    df = pd.concat(df, axis=1) # new dataframe player select

    # Sélectionner les données par rapport à la séquence de temps choisie en paramètre
    df = df.loc[(df["Time"] >= min) & (df["Time"] <= max)]

    return df

def speed_areas(dataframe, min, max, player_name):
    # Data
    df = dataframe

    # Récupérer les données du joueur sélectionné
    df = [df["Time"], df.filter(like=player_name)]

    # Faire un nouveau datafram0e à partir de ces données
    df = pd.concat(df, axis=1) # new dataframe player select

    # Sélectionner les données par rapport à la séquence de temps choisie en paramètre
    df = df.loc[(df["Time"] >= min) & (df["Time"] <= max)]

    # Calculer la distance parcourue pour chaque zone d'intensité
    z1 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y < 6), 2)
    z2 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 6 and y < 10), 2)
    z3 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 10 and y < 14), 2)
    z4 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 14 and y < 20), 2)
    z5 = round(sum(x for x, y in zip(df[f"{player_name}_dist"], df[f"{player_name}_speed"]) if y >= 20), 2)

    return z1, z2, z3, z4, z5
