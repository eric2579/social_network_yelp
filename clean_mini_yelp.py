import pickle
import pandas as pd
df = pd.read_pickle("yelp2.pkl")
df1 = df.ix[:30]
df1.to_pickle("yelp_30_restaurants.pkl")