import io
from app.db_connection import Database
from keras.models import load_model
import tensorflow as tf
import numpy as np
from sklearn.neighbors import NearestNeighbors
import base64
import imageio

with open('./app/image_based_model/models/Ranknet_features_v2.npy', 'rb') as f:
      img_vector_features = np.load(f)

with open('./app/image_based_model/models/products_map.npy', 'rb') as f:
    data_map = np.load(f)

imageModel = load_model('./app/image_based_model/models/AlmerceRankNet.h5')
id_results = []
recommendations=[]


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def predictImages(imageList):
    global id_results
    if 'base64,' in imageList["imageURL"]:
        image = imageList["imageURL"].split('base64,')[1]
    image = base64.b64decode(image)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, (224,224))
    image = np.expand_dims(image, axis=0)
    print(image.shape)
    embedding = imageModel([image,image,image])
    N_QUERY_RESULT = 5
    print(embedding.shape)
    features = img_vector_features.reshape(850,4096)
    print(features.shape)
    nbrs = NearestNeighbors(n_neighbors=N_QUERY_RESULT,metric="cosine").fit(features)
    
    distances, indices = nbrs.kneighbors(embedding)
    similar_image_indices = indices.reshape(-1)
    topFive_results = []

    for j in range(N_QUERY_RESULT):
        ind = similar_image_indices[j]
        fileName = data_map[ind]
        topFive_results.append(fileName[0])

    id_results = topFive_results
    print("these are the images suggested\n"+str(id_results))
    get_similar_products()



def get_similar_products():
    global recommendations
    for id in id_results:
        R = {}   
        query = "select name,image_name,description from toys_shop.products where product_id = "+str(id)+";"
        query_result = load_data_db(query)
        print(query_result)
        R['productHeader'] = query_result[0][0]
        R['imgSrc'] = query_result[0][1]
        if query_result[0][2] == None:
            R['productParagraph'] = ""
        else:
            R['productParagraph'] = query_result[0][2]

        R['id']= id
        nn = str(query_result[0][0])
        n = nn.replace(" ","-")
        R['ProductUrl']= "https://www.magaya.world/product/"+n+"/"
        recommendations.append(R)


def get_imageBased_recommendations():
    return recommendations

def safe_b64decode(data):
    # Incoming base64-encoded data is not always padded to a multiple of 4. Python's parser is more strict and requires
    # padding. Add padding if it's needed.
    overflow = len(data) % 4
    if overflow:
        if isinstance(data, str):
            padding = '=' * (4 - overflow)
        else:
            padding = b'=' * (4 - overflow)
        data += padding
    return base64.b64decode(data)

