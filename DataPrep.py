import pandas as pd
import numpy as np

df = pd.read_csv('SSD.csv') # Read the data

# keep only the columns that are needed for the analysis
df = df[['asin']] # asin is the unique identifier for each product


print(df.head()) # print the first 5 rows of the data

# Save the data to a new csv file
df.to_csv('ASIN.csv', index=False)