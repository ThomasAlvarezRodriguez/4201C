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
print(df)

#save the data in a csv file
df.to_csv('Capacité.csv', index=False)