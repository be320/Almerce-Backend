from sklearn.cluster import KMeans
from ..db_connection import Database,load_data_db
import pickle
import pandas as pd
import numpy as np

def bin_to_dec(cat):
    cat = int(cat,2)
    return cat

def normalize_cat(cat, max_cat, min_cat):
    cat = (cat - min_cat) / max_cat - min_cat
    return cat

def kmeans():
    with open('products.pkl', 'rb') as handle:
        products= pickle.load(handle)
    df = pd.DataFrame(products, columns = ['id','category','price'])
    dfx = df.copy()
    df['category'] = df['category'].apply(bin_to_dec)
    max_cat = df['category'].max()
    min_cat = df['category'].min()
    with open('max_min_cat.pkl', 'wb') as handle:
        pickle.dump([max_cat, min_cat], handle)
    df['category'] = df['category'].apply(normalize_cat, args=(max_cat, min_cat))
    #select category and price and place them in a numpy array
    data = np.array(df.iloc[:,1:3])
    kmeans = KMeans(n_clusters=6, random_state=0)
    clusters = kmeans.fit_predict(data)
    pickle.dump(kmeans, open("kmeans.pkl", "wb"))
    dfx['cluster'] = clusters
    clust = []
    clust.append(dfx[dfx['cluster'] == 0].values.tolist())
    clust.append(dfx[dfx['cluster'] == 1].values.tolist())
    clust.append(dfx[dfx['cluster'] == 2].values.tolist())
    clust.append(dfx[dfx['cluster'] == 3].values.tolist())
    clust.append(dfx[dfx['cluster'] == 4].values.tolist())
    clust.append(dfx[dfx['cluster'] == 5].values.tolist())
    return clust
