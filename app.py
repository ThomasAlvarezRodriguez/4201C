#Fichier app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import plotly
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Si la requête est une requête POST, extraire la valeur du paramètre 'page' du formulaire
        page = request.form.get('page', 'home')

        # Rediriger vers la page appropriée
        return redirect(url_for('index', page=page))
    else:
        # Si la requête est une requête GET, extraire la valeur du paramètre 'page' de l'URL
        page = request.args.get('page', 'home')

        # Afficher la page appropriée
        if page == 'table':
            # Connexion à la base de données MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())
            return render_template('table.html', data=data)
        elif page == 'graph':

            # Connexion à la base de données MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())

            # Extraction des données pour les graphiques
            ssd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'SSD'] # Liste des capacités des SSD
            ssd_price = [d['price'] for d in data if d['keyword'] == 'SSD'] # Liste des prix des SSD
            hdd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'HDD'] # Liste des capacités des HDD
            hdd_price = [d['price'] for d in data if d['keyword'] == 'HDD'] # Liste des prix des HDD
            ssd_stars = [d['stars'] for d in data if d['keyword'] == 'SSD'] # Liste des étoiles des SSD
            hdd_stars = [d['stars'] for d in data if d['keyword'] == 'HDD'] # Liste des étoiles des HDD
        
            return render_template('graph.html', data=data, ssd_storage=ssd_storage, ssd_price=ssd_price, hdd_storage=hdd_storage, hdd_price=hdd_price, ssd_stars=ssd_stars, hdd_stars=hdd_stars) # Passer les données aux templates


        elif page == 'text': # Afficher la page text.html

            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())

            ssd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'SSD'] 
            ssd_mean_storage = round (sum(ssd_storage)/len(ssd_storage))
            ssd_price = [d['price'] for d in data if d['keyword'] == 'SSD']
            hdd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'HDD']
            hdd_mean_storage = round (sum(hdd_storage)/len(hdd_storage))
            hdd_price = [d['price'] for d in data if d['keyword'] == 'HDD']
            ssd_stars = [d['stars'] for d in data if d['keyword'] == 'SSD']
            hdd_stars = [d['stars'] for d in data if d['keyword'] == 'HDD']

            # Calcul de la moyenne du prix par Go pour les SSD et les HDD
            ssd_mean_price_per_gb = round(sum(ssd_price) / sum(ssd_storage),4) 
            hdd_mean_price_per_gb = round(sum(hdd_price) / sum(hdd_storage),4)

            # Calcul de la moyenne des étoiles pour les SSD et les HDD
            ssd_mean_rating = round(sum(ssd_stars) / len(ssd_stars),2) # Moyenne des étoiles des SSD
            hdd_mean_rating = round(sum(hdd_stars) / len(hdd_stars),2) # Moyenne des étoiles des HDD

            ssd_data = [d for d in data if d['keyword'] == 'SSD'] # Liste des SSD
            top3_ssd = sorted(ssd_data, key=lambda d: d['price']/d['harmonized_capacity'])[:3] # Liste des 3 SSD les moins chers par Go
            hdd_data = [d for d in data if d['keyword'] == 'HDD'] # Liste des HDD
            top3_hdd = sorted(hdd_data, key=lambda d: d['price']/d['harmonized_capacity'])[:3] # Liste des 3 HDD les moins chers par Go

            return render_template('text.html', data=data, top3_hdd=top3_hdd, top3_ssd=top3_ssd, ssd_mean_storage=ssd_mean_storage,hdd_mean_storage=hdd_mean_storage,ssd_mean_price_per_gb=ssd_mean_price_per_gb, hdd_mean_price_per_gb=hdd_mean_price_per_gb, hdd_mean_rating=hdd_mean_rating, ssd_mean_rating=ssd_mean_rating)
      
        elif page == 'top_10': # Afficher la page top_10.html
            # Connexion à la base de données MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())

            # Paramètre pour filtrer les produits avec un nombre minimum de notes
            min_ratings = 50

            # Filtrer les données pour ne garder que les produits avec un nombre de notes supérieur ou égal à min_ratings
            filtered_data = [d for d in data if d['rating_count'] >= min_ratings]

            # Trier les données par nombre d'étoiles décroissant
            sorted_data = sorted(filtered_data, key=lambda d: d['stars'], reverse=True)

            # Sélectionner les 10 premiers produits
            top_10 = sorted_data[:10]

            return render_template('top_10.html', top_10=top_10)
        else:
            return render_template('index.html')



if __name__ == '__main__':
    app.run()
