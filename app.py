#Fichier app.py
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import plotly
import pandas as pd

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

            ssd_data = [d for d in data if d['keyword'] == 'SSD']
            top3_ssd = sorted(ssd_data, key=lambda d: d['price']/d['harmonized_capacity'])[:3]
            hdd_data = [d for d in data if d['keyword'] == 'HDD']
            top3_hdd = sorted(hdd_data, key=lambda d: d['price']/d['harmonized_capacity'])[:3]

            return render_template('text.html', data=data, top3_hdd=top3_hdd, top3_ssd=top3_ssd, ssd_mean_storage=ssd_mean_storage,hdd_mean_storage=hdd_mean_storage,ssd_mean_price_per_gb=ssd_mean_price_per_gb, hdd_mean_price_per_gb=hdd_mean_price_per_gb, hdd_mean_rating=hdd_mean_rating, ssd_mean_rating=ssd_mean_rating)
      
        elif page == 'top_10':
            # Connect to MongoDB database
            client = MongoClient('mongodb://localhost:27017/')
            db = client['4201C']
            collection = db['SSD-HDD']
            data = list(collection.find())

            # Define the minimum number of ratings required
            min_ratings = 50

            # Filter the data to include only products with enough ratings
            filtered_data = [d for d in data if d['rating_count'] >= min_ratings]

            # Sort the filtered data by stars in descending order
            sorted_data = sorted(filtered_data, key=lambda d: d['stars'], reverse=True)

            # Select the top 10 products from the sorted data
            top_10 = sorted_data[:10]

            return render_template('top_10.html', top_10=top_10)
        else:
            return render_template('index.html')



if __name__ == '__main__':
    app.run()
