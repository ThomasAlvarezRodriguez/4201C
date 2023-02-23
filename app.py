#Fichier app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        page = request.form['page']
        return redirect(url_for('index', page=page))
    else:
        page = request.args.get('page')
        return render_template('menu.html', page=page)


@app.route('/table')
def table():
    # Connect to MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['4201C'] 
    collection = db['SSD-HDD']
    data = list(collection.find())
    print(data)
    return render_template('table.html', data=data)


@app.route('/graph')
def graph():
    # Code pour générer le graphique
    return render_template('graph.html')

@app.route('/text')
def text():
    return render_template('text.html')

if __name__ == '__main__':
    app.run()
