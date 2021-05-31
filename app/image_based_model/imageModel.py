from app.db_connection import Database
from keras.models import load_model
import tensorflow as tf
import numpy as np

imageModel = load_model('./AlmerceRankNetV2.h5')
id_results = []
recommendations=[]


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result




def predictImages(imageList):
    global id_results
    image = tf.image.decode_jpeg(imageList, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, (224,224))
    image = np.expand_dims(image, axis=0)
    id_results = ['18','49','127','144','145']
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

