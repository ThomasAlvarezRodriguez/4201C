#Fichier app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import plotly

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the request is a POST request, extract the selected page value from the form data
        page = request.form.get('page', 'home')

        # Redirect the user to the same root URL with the 'page' parameter included in the URL query string
        return redirect(url_for('index', page=page))
    else:
        # If the request is a GET request, extract the value of the 'page' parameter from the URL query string
        page = request.args.get('page', 'home')

        # Render the appropriate page based on the value of the 'page' parameter
        if page == 'table':
            # Connect to MongoDB database
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())
            return render_template('table.html', data=data)
        elif page == 'graph':
            # Connect to MongoDB database
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())
            # Extract the storage and price data for SSDs and HDDs
            ssd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'SSD']
            ssd_price = [d['price'] for d in data if d['keyword'] == 'SSD']
            hdd_storage = [d['harmonized_capacity'] for d in data if d['keyword'] == 'HDD']
            hdd_price = [d['price'] for d in data if d['keyword'] == 'HDD']
            ssd_mean_price_per_gb = sum(ssd_price) / sum(ssd_storage)
            hdd_mean_price_per_gb = sum(hdd_price) / sum(hdd_storage)
            for doc in collection.find():
                if doc['keyword'] == 'SSD':
                    ssd_storage.append(doc['capacity'])
                    ssd_price.append(doc['price'])
                elif doc['keyword'] == 'HDD':
                    hdd_storage.append(doc['capacity'])
                    hdd_price.append(doc['price'])
            return render_template('graph.html',data=data, ssd_storage=ssd_storage, ssd_price=ssd_price, hdd_storage=hdd_storage, hdd_price=hdd_price, ssd_mean_price_per_gb=ssd_mean_price_per_gb, hdd_mean_price_per_gb=hdd_mean_price_per_gb)
        elif page == 'text':
            return render_template('text.html')# If the 'page' parameter is not present or invalid, render the default index page
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
