# M2_AJBD_DASHBOARD

## Contexte - Problématique :

L'objectif de ce travail est une de montrer une ébauche des possibilités qu'offrent Python dans la visualisation des données. Les rapports d'une vingtaines de pages ne rendent pas la visualisation des données faciles pour l'entraîneur et cela prend du temps de rechercher les informations que l'on souhaite.
Ici, j'ai souhaité montrer que l'on peut donner à l'entraîneur la possibilités de choisir personnellement ce qu'il souhaite voir comme données (interaction avec son pc).

Les visualisations n'ont pas de réelles valeurs en pratique sur ce travail, elles sont là uniquement pour schématiser une partie de ce qu'il est possible de faire avec python sans utiliser des librairies qui sont déjà préconçus pour le traitement de données en football notamment via StatBomb.
Étant donné que vous n'êtes pas spéciliasé dans le football et que le travail demandé est de montrer ce que l'on s'est faire un python, je n'ai pas fait d'analyse des graphes et ne vous ai pas fournit des dizaines de graphiques différents. Je pars du principe que si l'on arrive à afficher un line plot, on peut afficher un radar plot, scatter plot, etc...

## Utilisation :
Lancer le script app.py puis cliquer sur le lien qui s'affichera dans la console (un Dashboard va apparaître dans votre navigateur web).

Il est possible de:
- Sélectionner les deux joueurs (dans l'objectif de les comparer)
- Définir le temps de début et de fin de la séquence souhaitée (dans l'objectif de revisionner une séquence spécifique d'un match par exemple)
- Sélectionner l'évènement (dans l'objectif de voir l'emplacement du déroulement des évènements sur le terrain).

## Données utilisées
Jeu de données 1 : Arsenal & City (events + tracking joueurs)
Jeu de données 2 : Inconnue (tracking joueurs + tracking ballon)

- Animation2D : données de tracking d'un autre match (pour obtenir une animation avec ballon où les données ne sont pas disponibles pour le premier jeu de données.
        - Radar, scatter, bar plot : events et données de tracking joueurs (Arsenal & City)
