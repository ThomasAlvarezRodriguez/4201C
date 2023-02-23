from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['4201C']

@app.route('/')
def index():
    # Query data from MongoDB collection
    data = db['SSD-HDD'].find()

    # Render template with data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
