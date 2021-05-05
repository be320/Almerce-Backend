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

def hotEncode_category(i):
    postgreSQL_select_Query = "select category_"+str(i)+" from toys_shop.categories;"
    categories = load_data_db(postgreSQL_select_Query)
    data = []
    for row in categories:
        data.append(row[0])
    s=pd.get_dummies(data)
    return s,categories


def hotEncode_categories(user_parameters):
    global maxPrice,minPrice
    c1,c1_names = hotEncode_category(1)
    c1=c1.to_numpy()
    c1_str = []
    for arr in c1:
        s = ""
        for i in arr:
            s+=str(i)
        c1_str.append(s)

    c2,c2_names = hotEncode_category(2)
    c2=c2.to_numpy()
    c2_str = []
    for arr in c2:
        s = ""
        for i in arr:
            s+=str(i)
        c2_str.append(s)

    c3,c3_names = hotEncode_category(3)
    c3=c3.to_numpy()
    c3_str = []
    for arr in c3:
        s = ""
        for i in arr:
            s+=str(i)
        c3_str.append(s)

    c_names = []
    for i in range(0,len(c3)):
        c_names_str = ""
        c_names_str =   "المتجر " + ">" + str(c1_names[i][0]) + ">" + str(c2_names[i][0]) + ">" + str(c3_names[i][0])
        c_names_str = c_names_str.replace(">None","")
        c_names.append(c_names_str)

    c_codes = []
    for i in range(0,len(c3)):
        c_code_str = ""
        c_code_str =  ''.join(map(str, c1[i]))  + ''.join(map(str, c2[i]))  + ''.join(map(str, c3[i]))
        c_codes.append(c_code_str)
    d = dict(zip(c_names, c_codes))  

    query = "select product_id,categories_name,price from toys_shop.products;"
    products = load_data_db(query)

    data = []
    prices = []
    for product in products:
        s = ""
        s = str(product[1])
        product[1]=d[s]
        row = list(map(int, product[1]))
        row.append(product[2])
        prices.append(product[2])
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
    for i in similar_product_indices:
        R = {}   
        id = products[i][0]
        imgSrc_query = "select image_name from toys_shop.products where product_id = "+str(id)+";"
        R['imgSrc'] = load_data_db(imgSrc_query)
        productHeader_query = "select name from toys_shop.products where product_id = "+str(id)+";"
        R['productHeader'] = load_data_db(productHeader_query)
        nn = str(R['productHeader'][0][0])
        n = nn.replace(" ","-")
        print(n)
        R['ProductUrl']= "https://www.magaya.world/product/"+n+"/"
        productParagraph_query = "select description from toys_shop.products where product_id = "+str(id)+";"
        R['productParagraph'] = load_data_db(productParagraph_query)
        R['id']= id
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


# from .db_connection import Database
# from sklearn.neighbors import NearestNeighbors
# from sklearn.neighbors import DistanceMetric
# from scipy.spatial import distance
# from sklearn import preprocessing
# import pandas as pd
# import numpy as np
# import math 

# user_parameters=[]
# fixed_user_parameters = []
# recommendations_index = []
# recommendations = []

# def load_data_db(query):
#     db=Database()
#     result = Database.select_rows_dict_cursor(db,query)
#     return result

# def hotEncode_category_1():
#     postgreSQL_select_Query = "select category_1 from toys_shop.categories;"
#     categories = load_data_db(postgreSQL_select_Query)
#     data = []
#     for row in categories:
#         data.append(row[0])
#     s=pd.get_dummies(data)
#     return s,categories


# def hotEncode_category_2():
#     postgreSQL_select_Query = "select category_2 from toys_shop.categories;"
#     categories = load_data_db(postgreSQL_select_Query)
#     data = []
#     for row in categories:
#         data.append(row[0])
#     s=pd.get_dummies(data)
#     return s,categories

# def hotEncode_category_3():
#     postgreSQL_select_Query = "select category_3 from toys_shop.categories;"
#     categories = load_data_db(postgreSQL_select_Query)
#     data = []
#     for row in categories:
#         data.append(row[0])
#     s=pd.get_dummies(data)
#     return s,categories

# def send_category1(user_category1):
#     user_parameters.append(user_category1)
# def send_category2(user_category2):
#     user_parameters.append(user_category2)
# def send_category3(user_category3):
#     user_parameters.append(user_category3)
# def send_price(price):
#     for p in price:
#         user_parameters.append(p)
#     hotEncode_categories()
# def get_recommendations():
#     return recommendations



   
# def hotEncode_categories():
#     c1,c1_names = hotEncode_category_1()
#     c1=c1.to_numpy()
#     c1_str = []
#     for arr in c1:
#         s = ""
#         for i in arr:
#             s+=str(i)
#         c1_str.append(s)

#     c2,c2_names = hotEncode_category_2()
#     c2=c2.to_numpy()
#     c2_str = []
#     for arr in c2:
#         s = ""
#         for i in arr:
#             s+=str(i)
#         c2_str.append(s)

#     c3,c3_names = hotEncode_category_3()
#     c3=c3.to_numpy()
#     c3_str = []
#     for arr in c3:
#         s = ""
#         for i in arr:
#             s+=str(i)
#         c3_str.append(s)

#     c_names = []
#     for i in range(0,len(c3)):
#         c_names_str = ""
#         c_names_str =   "المتجر " + ">" + str(c1_names[i][0]) + ">" + str(c2_names[i][0]) + ">" + str(c3_names[i][0])
#         c_names_str = c_names_str.replace(">None","")
#         c_names.append(c_names_str)

#     c_codes = []
#     for i in range(0,len(c3)):
#         c_code_str = ""
#         c_code_str =  ''.join(map(str, c1[i]))  + ''.join(map(str, c2[i]))  + ''.join(map(str, c3[i]))
#         c_codes.append(c_code_str)
#     d = dict(zip(c_names, c_codes))  

#     query = "select product_id,categories_name,price from toys_shop.products;"
#     products = load_data_db(query)
 
#     encoded_categories = []
#     prices = []
#     for product in products:
#         s = ""
#         s = str(product[1])
#         product[1]=d[s]
#         encoded_categories.append(product[1])
#         prices.append(product[2])

#     maxPrice = max(prices)
#     minPrice = min(prices)

#     s =   "المتجر " + "> " + str(user_parameters[0]) + " > " + str(user_parameters[1]) + " > " + str(user_parameters[2]) + " "
#     s = s.replace("> NONE ","")
#     fixed_user_parameters.append(d[str(s)])
#     mean_price = (user_parameters[-1]+user_parameters[-2])/2
#     fixed_user_parameters.append(mean_price)
    
#     similarities = custom_metric(fixed_user_parameters[1],fixed_user_parameters[0], minPrice, maxPrice, prices, encoded_categories)
#     while len(recommendations_index) < 5:
#         min_value = min(similarities)
#         values = np.array(similarities)
#         min_indices = np.where(values == min_value)[0]
#         for index in min_indices:
#             recommendations_index.append(index)
#             similarities[index]+=1000.0

#     for i in recommendations_index:
#         R = []   
#         id = products[i][0]
#         imgSrc_query = "select image_name from toys_shop.products where product_id = "+str(id)+";"
#         imgSrc_result = load_data_db(imgSrc_query)
#         R.append(imgSrc_result)
#         # ProductUrl_query=
#         # ProductUrl_result=load_data_db(ProductUrl_query)
#         # R.append(img_result)
#         productHeader_query = "select name from toys_shop.products where product_id = "+str(id)+";"
#         productHeader_result = load_data_db(productHeader_query)
#         R.append(productHeader_result)
#         productParagraph_query = "select description from toys_shop.products where product_id = "+str(id)+";"
#         productParagraph_result = load_data_db(productParagraph_query)
#         R.append(productParagraph_result)
#         R.append(id)
#         recommendations.append(R)
#     print(recommendations_index)
#     print(recommendations)



# def custom_metric(user_price, user_category, minPrice, maxPrice, prices, encoded_categories):
#     normalized_user_price = (user_price-minPrice)/(maxPrice-minPrice)
#     for i in range(0,len(encoded_categories)):
#         encoded_categories[i] = list(map(int, encoded_categories[i]))
#     user_category= list(map(int,user_category))
#     similarity_distance = []
#     for i in range(0,len(prices)):
#         price_distance = abs(normalized_user_price - (prices[i] - minPrice) / (maxPrice - minPrice))
#         category_distance = distance.jaccard(encoded_categories[i], user_category)
#         dist = math.sqrt(price_distance**2+category_distance**2)
#         similarity_distance.append(dist)
#     return similarity_distance
    
    
 