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
            ssd_stars = [d['stars'] for d in data if d['keyword'] == 'SSD']
            hdd_stars = [d['stars'] for d in data if d['keyword'] == 'HDD']
        
            return render_template('graph.html', data=data, ssd_storage=ssd_storage, ssd_price=ssd_price, hdd_storage=hdd_storage, hdd_price=hdd_price, ssd_stars=ssd_stars, hdd_stars=hdd_stars)


        elif page == 'text':

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
            # Calculate the mean price per GB for SSDs and HDDs
            ssd_mean_price_per_gb = round(sum(ssd_price) / sum(ssd_storage),4)
            hdd_mean_price_per_gb = round(sum(hdd_price) / sum(hdd_storage),4)
            # Calculate the mean stars for SSDs and HDDs
            ssd_mean_rating = round(sum(ssd_stars) / len(ssd_stars),2)
            hdd_mean_rating = round(sum(hdd_stars) / len(hdd_stars),2)
            return render_template('text.html', data=data, ssd_mean_storage=ssd_mean_storage,hdd_mean_storage=hdd_mean_storage,ssd_mean_price_per_gb=ssd_mean_price_per_gb, hdd_mean_price_per_gb=hdd_mean_price_per_gb, hdd_mean_rating=hdd_mean_rating, ssd_mean_rating=ssd_mean_rating)
        else:
            return render_template('index.html')



if __name__ == '__main__':
    app.run()
