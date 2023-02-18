import pandas as pd
import pymongo

client = pymongo.MongoClient()
database = client['exercices'] # A changer ? 
collection = database['ssd_amazon']

csv_file="amazon/data/SSD.csv"
df_ssd = pd.read_csv(csv_file)
#print(df_ssd.head())
#print(df_ssd.describe())


# Delete the collection
result = collection.drop()

# Insert the data from the DataFrame into the collection
records = df_ssd.to_dict(orient='records')
result = collection.insert_many(records)

# Print the number of documents inserted
print(f'Number of documents inserted: {len(result.inserted_ids)}')