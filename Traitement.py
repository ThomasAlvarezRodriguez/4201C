# Ce fichier a pour but de traiter les données des csv pour abtenir des meilleurs informations

import pandas as pd
import numpy as np
import re
from pymongo import MongoClient

df = pd.read_csv('Data.csv') # Read the data
dfM = pd.read_csv('traitement.csv', sep=';') # Read the data
nom = df['name'].astype(str) # Get the name of the product
#on extrait chaque ligne pour en faire une chaine de caractère  qu'on stocke dans une liste


# Définir l'expression régulière pour extraire la capacité de stockage
regex_capacite = r'(?<!Tours|tours)(\d+)(\s*Go|\s*To|\s*TB|\s*go|\s*GB|\s*TO)'



# Fonction pour extraire la capacité de stockage
def extraire_capacite(texte):
    match = re.search(regex_capacite, texte)
    if match:
        capacite = match.group(1) + match.group(2)
        return capacite
    else:
        return None

# Appliquer la fonction extraire_capacite à la colonne 'Titre' pour créer une nouvelle colonne 'Capacité'
df['capacity'] = nom.apply(extraire_capacite)

# Supprimer les lignes qui n'ont pas de capacité de stockage
df = df[df['capacity'].notnull()]

# Afficher le dataframe résultant

Cap = df['capacity'].astype(str) # Get the capacity of the product

# Maintenant on va harmoniser les capacités de stockage en les mettant en Go
# Si la capacité est en To ou TB, on la multiplie par 1000 pour l'avoir en Go
# Si la capacité est en Mo, on la divise par 1000 pour l'avoir en Go

# Fonction pour harmoniser les capacités de stockage
def harmoniser_capacite(texte):
    if 'To' in texte or 'TB' in texte or 'to' in texte or 'TO' in texte:
        capacite = float(texte[:-2].replace(',', '.')) * 1000
        return capacite
    elif 'Go' in texte or 'GB' in texte or 'go' in texte or 'Gb' in texte:
        capacite = float(texte[:-2].replace(',', '.'))
        return capacite
    elif 'Mo' in texte or 'MB' in texte or 'mo' in texte or 'Mb' in texte:
        capacite = float(texte[:-2].replace(',', '.')) / 1000
        return capacite
    else:
        raise ValueError('Unité de mesure non reconnue')

# Appliquer la fonction harmoniser_capacite à la colonne 'Capacité' pour créer une nouvelle colonne 'Capacité harmonisée'
df['harmonized_capacity'] = Cap.apply(harmoniser_capacite)

#Harmonisation du type de données des colonnes stars et rating_count
df['stars']=df['stars'].astype(str)
df['rating_count']=df['rating_count'].astype(str)

# on transforme les espaces insécables en espaces normaux dans l'ensemble des colonnes contenant des chaînes de caractères
df['name'] = df['name'].str.replace(u'\xa0', u' ') 
#supprimer les virgules dans le nom
df['name'] = df['name'].str.replace(u',', u' ')
df['stars'] = df['stars'].str.replace(u'\xa0', u' ')
df['rating_count'] = df['rating_count'].str.replace(u'\xa0', u' ')

# on remplace les chaines de caractères 'nan' par des "Inconnu"
df['stars'] = df['stars'].replace('nan', 'Inconnu')
df['rating_count'] = df['rating_count'].replace('nan', 'Inconnu')
        
# On combine df et dfPrice pour avoir les prix des produits avec la colonne asin en clé
df = pd.merge(df, dfM, on='asin', how='left')
# on supprime les lignes dupliquées
df = df.drop_duplicates(subset=['asin'])

# On supprime la colonne price_x et on renomme la colonne price_y en price
df = df.drop(columns=['price_x'])
df = df.rename(columns={'price_y': 'price'})

#Suppression des lignes "Inconnu" dans la colonne "stars"
df = df[df['stars'] != 'Inconnu']

# on modifie la colonne "stars" pour ne garder que les 3 premiers caractères
df['stars'] = df['stars'].str[:3]
# on modifie la colonne "rating_count" pour supprimer les espaces
df['rating_count'] = df['rating_count'].str.replace(' ','')
# on modifie la colonne "rating_count" pour ajouter un espace avant "é"
df['rating_count'] = df['rating_count'].str.replace('é',' é')
# on modifie la colonne "rating_count" pour ne garder que les chiffres
df['rating_count'] = df['rating_count'].str.replace(r'\D','')


#On modifie la colonne "stars" pour transformer les valeurs "4,5" en "4.5"
df['stars'] = df['stars'].str.replace(',','.')
# On transforme les colonnes "stars" et "rating_count" en float
df['stars'] = df['stars'].astype(float)
df['rating_count'] = df['rating_count'].astype(float)

# on sauvegarde le fichier
df.to_csv('DataTraite.csv',sep=";",index=False)

# Lecture du fichier csv
df = pd.read_csv('DataTraite.csv', sep=';')

# Connection à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['4201C']

# Drop de la collection si elle existe déjà
db['SSD-HDD'].drop()

# Insert des données dans la collection
db['SSD-HDD'].insert_many(df.to_dict('records'))

# Test
print(db['SSD-HDD'].find_one())