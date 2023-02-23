import pandas as pd
from pymongo import MongoClient

# Load CSV file into pandas dataframe
df = pd.read_csv('DataTraite.csv', sep=';')

# Connect to MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['4201C']

# Drop collection if it already exists
db['SSD-HDD'].drop()

# Insert data into MongoDB collection
db['SSD-HDD'].insert_many(df.to_dict('records'))

# Test if data was inserted correctly
print(db['SSD-HDD'].find_one())

