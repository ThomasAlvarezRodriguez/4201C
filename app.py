#Fichier app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        page = request.form['page']
        return redirect(url_for('index', page=page))
    else:
        page = request.args.get('page')
        return render_template('menu.html', page=page)


# Route pour afficher le tableau
@app.route('/table')
def table():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['4201C'] 
    collection = db['SSD-HDD']
    data = list(collection.find())
    return render_template('table.html', data=data)

# Route pour afficher le graphique
@app.route('/graph')
def graph():
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['4201C'] 
    collection = db['SSD-HDD']
    data = list(collection.find())

    # Préparation des données pour le graphique
    ssd_data = []
    hdd_data = []
    for d in data:
        if d['keyword'] == 'SSD':
            ssd_data.append(d)
        elif d['keyword'] == 'HDD':
            hdd_data.append(d)

    ssd_x = [d['harmonized_capacity'] for d in ssd_data]
    ssd_y = [d['price'] for d in ssd_data]
    hdd_x = [d['harmonized_capacity'] for d in hdd_data]
    hdd_y = [d['price'] for d in hdd_data]

    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ssd_x, y=ssd_y, mode='markers', name='SSD'))
    fig.add_trace(go.Scatter(x=hdd_x, y=hdd_y, mode='markers', name='HDD'))
    fig.update_layout(title='Prix en fonction de la capacité de stockage', xaxis_title='Capacité de stockage (Go)', yaxis_title='Prix (€)')
    
    # Affichage du graphique
    graph_html = fig.to_html(full_html=False)
    return render_template('graph.html', graph_html=graph_html)

# Route pour afficher le texte
@app.route('/text')
def text():
    return render_template('text.html')

if __name__ == '__main__':
    app.run()
