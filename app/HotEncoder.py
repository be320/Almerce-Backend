from .db_connection import Database
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance
import math 
import numpy as np
import pandas as pd

maxPrice = 0
minPrice = 0
recommendations=[]

def get_recommendations():
    return recommendations
def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def hotEncode_category():
    postgreSQL_select_Query = "select * from toys_shop.categories;"
    categories = load_data_db(postgreSQL_select_Query)
    c1_names = []
    c2_names = []
    c3_names = []
    for row in categories:
        c1_names.append(row[0])
        c2_names.append(row[1])
        c3_names.append(row[2])
  
    c1=pd.get_dummies(c1_names) # c1 is the hot encoding of category1 names
    c2=pd.get_dummies(c2_names) # c2 is the hot encoding of category2 names
    c3=pd.get_dummies(c3_names) # c3 is the hot encoding of category3 names

    return c1,c2,c3 # return the 3 categories hot encoded 


def hotEncode_categories(user_parameters):
    global maxPrice,minPrice 
    c1,c2,c3= hotEncode_category()
    
    # c1,c2,c3 are the hotencode category1,category2,category3
    # Array of arrays, each array consits of many strings, each string is a bit (0 or 1)
    # ex: c1 = [['1','0','0'],['0','0','1']] 
    c1=c1.to_numpy()
    c2=c2.to_numpy()
    c3=c3.to_numpy()

    # c1_str,c2_str,c3_str are 1D arrays of strings, each string is the hot encode of a category consisting of multiple bits
    # ex: c1_str = ['100','001'] 
    c1_str = []
    c2_str = []
    c3_str = []

    # categories_names is [['المتجر > كتب تعليمية وسلاسل قصصية > بطاقات '], ['المتجر > تنمية المهارات > العاب العلوم ']]
    postgreSQL_select_Query = "select distinct categories_name from toys_shop.products;"
    categories_names = load_data_db(postgreSQL_select_Query)

    # c_names is ['المتجر > كتب تعليمية وسلاسل قصصية > بطاقات ', 'المتجر > تنمية المهارات > العاب العلوم '] of all 38 (till now) distinct categories_name 
    c_names = []

    # c_codes is ['100100000001','01000001000010','0001000010000100'] where each element = category1 code + category2 + category3 code
    c_codes = []

    for i in range (len(c1)):
        s=""
        for bit in c1[i]:
            s+=str(bit)
        c1_str.append(s)
        s=""
        for bit in c2[i]:
            s+=str(bit)
        c2_str.append(s)
        s=""
        for bit in c3[i]:
            s+=str(bit)
        c3_str.append(s)

        c_names.append(categories_names[i][0])
        c_codes.append(c1_str[i]+c2_str[i]+c3_str[i])

    d = dict(zip(c_names, c_codes))  
            
    query = "select product_id,categories_name,price from toys_shop.products;"
    products = load_data_db(query)

    data = []
    prices = []
    for product in products:
        # hot encode each category name and append it into "row" list
        s = ""
        s = str(product[1])
        product[1]=d[s] #0001000000000010000000000000000000000000
        row = list(map(int, product[1])) #[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #append price to "row" making it last item in it
        row.append(product[2])
        #prices (bara el for loop) collects all product's prices to be able to calculate max and min price
        prices.append(product[2])
        #data (bara el for loop) array of arrays
        data.append(row)
    maxPrice = max(prices)
    minPrice = min(prices)

    fixed_user_parameters = {}
    s =   "المتجر " + "> " + str(user_parameters['category1']) + " > " + str(user_parameters['category2']) + " > " + str(user_parameters['category3']) + " "
    s = s.replace("> NONE ","")
    fixed_user_parameters['category']=d[str(s)]
    mean_price = (min(user_parameters['price'])+max(user_parameters['price']))/2
    fixed_user_parameters['mean_price'] = mean_price

    return data,fixed_user_parameters,products

def get_similar_products(user_parameters):
    data,fixed_user_parameters,products = hotEncode_categories(user_parameters)
    N_QUERY_RESULT = 5
    nbrs = NearestNeighbors(n_neighbors=N_QUERY_RESULT, algorithm = 'brute',metric=custom_metric).fit(data)

    user_input= list(fixed_user_parameters['category'])
    user_input.append(fixed_user_parameters['mean_price'])
    distances, indices = nbrs.kneighbors([user_input])
    similar_product_indices = indices.reshape(-1)

    global recommendations
    recommendations=[]
    for i in similar_product_indices:
        R = {}   
        id = products[i][0]
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
        nn = str(R['productHeader'][0][0])
        n = nn.replace(" ","-")
        R['ProductUrl']= "https://www.magaya.world/product/"+n+"/"
        recommendations.append(R)

    # print(similar_product_indices)
    # print(distances)
    # for i in similar_product_indices:
    #      print(data[i])

def custom_metric(X1,X2):
    cat1 = X1[:(len(X1)-1)]
    cat2 = X2[:(len(X2)-1)]
    price1 = X1[len(X1)-1]
    price2 = X2[len(X2)-1]
    category_distance = distance.jaccard(cat1, cat2)
    price_distance = abs( (price1-minPrice)/(maxPrice - minPrice) - (price2-minPrice)/(maxPrice - minPrice) )
    dist = math.sqrt(price_distance**2 + category_distance**2)
    return dist
