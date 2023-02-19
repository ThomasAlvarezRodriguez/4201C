import pandas as pd
import numpy as np

df = pd.read_csv('SHD.csv') # Read the data
df2 = pd.read_csv('SSD-HDD-2.csv') # Read the data

# keep only the columns that are needed for the analysis
df = df[['name', 'asin','keyword','price', 'stars','rating_count','url']]
df2 = df2[['name', 'asin','keyword','price', 'stars','rating_count','url']]


print(df2.head()) # print the first 5 rows of the data

# merge the two dataframes so that the data is in one dataframe and the columns are the same
df3 = pd.concat([df, df2], ignore_index=True)
print(df3.head()) # print the first 5 rows of the data

# save the data to a csv file
df3.to_csv('Data.csv', index=False)