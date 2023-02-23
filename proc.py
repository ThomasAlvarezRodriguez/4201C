import pandas as pd
import numpy as np
import re

df = pd.read_csv('DataTraite.csv',sep=";") # Read the data

# on vire les lignes qui on "Inconnu" dans la colonne "stars"
df = df[df['stars'] != 'Inconnu']

# on modifie la colonne "stars" pour ne garder que les 3 premiers caractères
df['stars'] = df['stars'].str[:3]
# on modifie la colonne "rating_count" pour ne garder que les chiffres
df['rating_count'] = df['rating_count'].str.extract('(\d+)', expand=False)
#On modifie la colonne "stars" pour transformer les valeurs "4,5" en "4.5"
df['stars'] = df['stars'].str.replace(',','.')
# On transforme les colonnes "stars" et "rating_count" en float
df['stars'] = df['stars'].astype(float)
df['rating_count'] = df['rating_count'].astype(float)

print(df.head(10))

# on sauvegarde le fichier
df.to_csv('DataTraite.csv',sep=";",index=False)