import io
from app.db_connection import Database
from keras.models import load_model
import tensorflow as tf
import numpy as np
from sklearn.neighbors import NearestNeighbors
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
import base64

with open('./app/image_based_model/resources/vgg16_features_updated.npy', 'rb') as f:
      img_vector_features = np.load(f)

with open('./app/image_based_model/resources/products_map_updated.npy', 'rb') as f:
    data_map = np.load(f)

print(data_map)
imageModel = VGG16(weights='imagenet', include_top=False, pooling='max')

id_results = []
recommendations=[]


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def predictImages(imageList):
    
    global id_results
    id_results = []
    global recommendations
    recommendations = []
    if 'base64,' in imageList["imageURL"]:
        image = imageList["imageURL"].split('base64,')[1]
    image = base64.b64decode(image)
    image = tf.image.decode_jpeg(image, channels=3)
    # image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, (224,224))
    image = np.expand_dims(image, axis=0)
    img = np.array(image)
    print("------------Image---------\n")
    print(img)
    image = preprocess_input(img)
    embedding = imageModel.predict(image)
    embedding = embedding.flatten()
    N_QUERY_RESULT = 5
    print("------------EMBEDDING---------\n")
    print(embedding)
    features = img_vector_features.reshape(2236,512)
    nbrs = NearestNeighbors(n_neighbors=N_QUERY_RESULT,metric="cosine").fit(features)
    
    distances, indices = nbrs.kneighbors([embedding])
    similar_image_indices = indices.reshape(-1)
    print("SIMILAR INDICES",similar_image_indices)
    topFive_results = []
    print(similar_image_indices)
    for j in range(N_QUERY_RESULT):
        ind = similar_image_indices[j]
        fileName = data_map[ind]
        print("fileName",fileName)
        topFive_results.append(fileName[0])
        
    print(topFive_results)
    id_results = topFive_results
    get_similar_products()



def get_similar_products():
    global recommendations
    for id in id_results:
        print(id)
        R = {}   
        query = "select name,image_name,description from toys_shop.products where product_id = '"+str(id)+"';"
        query_result = load_data_db(query)
        R['productHeader'] = query_result[0][0]
        R['imgSrc'] = query_result[0][1]
        if query_result[0][2] == None:
            R['productParagraph'] = ""
        else:
            R['productParagraph'] = query_result[0][2]

        R['id']= "'"+str(id)+"'"
        nn = str(query_result[0][0])
        n = nn.replace(" ","-")
        R['ProductUrl']= "https://www.almerce.xyz/product/"+n+"/"
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

