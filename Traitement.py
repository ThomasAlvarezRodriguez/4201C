# Ce fichier a pour but de traiter les données des csv pour abtenir des meilleurs informations

import pandas as pd
import numpy as np
import re
df = pd.read_csv('Data.csv') # Read the data
nom = df['name'].astype(str) # Get the name of the product
#on extrait chaque ligne pour en faire une chaine de caractère  qu'on stocke dans une liste


# Définir l'expression régulière pour extraire la capacité de stockage
regex_capacite = r'(\d+)(\s*Go|\s*To|\s*Mo|\s*TB|\s*to|\s*go|\s*GB)'

# Fonction pour extraire la capacité de stockage
def extraire_capacite(texte):
    match = re.search(regex_capacite, texte)
    if match:
        capacite = match.group(1) + match.group(2)
        return capacite
    else:
        return None

# Appliquer la fonction extraire_capacite à la colonne 'Titre' pour créer une nouvelle colonne 'Capacité'
df['Capacité'] = nom.apply(extraire_capacite)

# Supprimer les lignes qui n'ont pas de capacité de stockage
df = df[df['Capacité'].notnull()]

# Afficher le dataframe résultant

Cap = df['Capacité'].astype(str) # Get the capacity of the product

# Maintenant on va harmoniser les capacités de stockage en les mettant en Go
# Si la capacité est en To ou TB, on la multiplie par 1000 pour l'avoir en Go
# Si la capacité est en Mo, on la divise par 1000 pour l'avoir en Go

# Fonction pour harmoniser les capacités de stockage
def harmoniser_capacite(texte):
    if 'To' in texte or 'TB' in texte or 'to' in texte:
        capacite = float(texte[:-2]) * 1000
        return capacite
    elif 'Mo' in texte:
        capacite = float(texte[:-2]) / 1000
        return capacite
    else:
        return float(texte[:-2])
    
# Appliquer la fonction harmoniser_capacite à la colonne 'Capacité' pour créer une nouvelle colonne 'Capacité harmonisée'
df['Capacité harmonisée'] = Cap.apply(harmoniser_capacite)

# on transforme les espaces insécables en espaces normaux dans l'ensemble des colonnes contenant des chaînes de caractères
df['name'] = df['name'].str.replace(u'\xa0', u' ')
#supprimer les virgules dans le nom
df['name'] = df['name'].str.replace(u',', u' ')
df['stars'] = df['stars'].str.replace(u'\xa0', u' ')
df['rating_count'] = df['rating_count'].str.replace(u'\xa0', u' ')


# Afficher le dataframe résultant
print(df)


 # Save the data
df.to_csv('DataTraité.csv', sep=';', index=False)
