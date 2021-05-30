from app.db_connection import Database
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance
import math 
import numpy as np
import pandas as pd

maxPrice = 0
minPrice = 0
recommendations=[]
error = 0.0

def get_chatBased_recommendations():
    return recommendations

def get_error():
    return error

def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result
 

def hotEncode_categories(user_parameters):
    global maxPrice,minPrice 
    #c1,c2,c3= hotEncode_category()
    
    # c1,c2,c3 are the hotencode category1,category2,category3
    # Array of arrays, each array consits of many strings, each string is a bit (0 or 1)
    # ex: c1 = [['1','0','0'],['0','0','1']] 
    c1= np.load('c1_file.npy')
    c2=np.load('c2_file.npy')
    c3=np.load('c3_file.npy')
    # print("HEREEEEEEEEEEEEEEEEEEEEE")
    # print(c1,c2,c3)

    # c1_str,c2_str,c3_str are 1D arrays of strings, each string is the hot encode of a category consisting of multiple bits
    # ex: c1_str = ['100','001'] 
    c1_str = []
    c2_str = []
    c3_str = []

    # categories_names is ['المتجر > كتب تعليمية وسلاسل قصصية > بطاقات ', 'المتجر > تنمية المهارات > العاب العلوم ']
    # products_np = np.load('products_file.npy') 
    # print(type(products_np))
    # p1= products_np[:,0].astype(np.int)
    # p2 = products_np[:,1]
    # p1 = np.reshape(p1, (-1, 1))
    # p2 = np.reshape(p2, (-1, 1))
    # p=np.concatenate((p1,p2),axis=1)
    # print(p)
    # p3 = products_np[:,2].astype(np.float)
    # categories_name = np.unique(products_np[:, 1].copy())
    # print((categories_name[:5]))
  
    query = "select product_id,categories_name,price from toys_shop.products;"
    products = load_data_db(query)  
    
    query = "select * from toys_shop.categories;"
    categories = load_data_db(query)  
    categories = np.array(categories)
    # c_names is ['المتجر > كتب تعليمية وسلاسل قصصية > بطاقات ', 'المتجر > تنمية المهارات > العاب العلوم '] of all 38 (till now) distinct categories_name 
    c_names = []  
    for c in categories:
        s =   "المتجر " + ">" + str(c[0]) + ">" + str(c[1]) + ">" + str(c[2]) + " "
        s = s.replace(">None","")
        c_names.append(s.strip())
    #print((categories_name[:5]))

    

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

        c_codes.append(c1_str[i]+c2_str[i]+c3_str[i])
    d = dict(zip(c_names, c_codes))  


    data = []
    prices = []

    for product in products:
        # hot encode each category name and append it into "row" list
        s = ""
        s = str(product[1])
        product[1]=d[s.strip()] #0001000000000010000000000000000000000000
        row = list(map(int, product[1])) #[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #append price to "row" making it last item in it
        row.append(product[2])
        #prices (bara el for loop) collects all product's prices to be able to calculate max and min price
        prices.append(product[2])
        #data (bara el for loop) array of arrays
        data.append(row)
    maxPrice = max(prices)
    minPrice = min(prices)
    
    # df = pd.DataFrame(products)
    # df.to_csv('kmeans_products.csv',index=False)

    fixed_user_parameters = {}
    s =   "المتجر " + "> " + str(user_parameters['category1']) + " > " + str(user_parameters['category2']) + " > " + str(user_parameters['category3']) + " "
    s = s.replace("> NONE ","")
    fixed_user_parameters['category']=d[str(s).strip()]
    mean_price = (min(user_parameters['price'])+max(user_parameters['price']))/2
    fixed_user_parameters['mean_price'] = mean_price

    return data,fixed_user_parameters,products

def get_categories1():
    db=Database()
    query = "select distinct category_1 from toys_shop.categories WHERE category_1 IS NOT NULL;"
    category_1_records = Database.select_rows_dict_cursor(db,query)
    return (category_1_records)

def get_categories2(choice):
    db=Database()
    query = "select distinct category_2 from toys_shop.categories WHERE category_1 = ' "+choice+" ' AND category_2 IS NOT NULL;"
    category_2_records = Database.select_rows_dict_cursor(db,query)
    return (category_2_records)

def get_categories3(choice):
    db=Database()
    query = "select distinct category_3 from toys_shop.categories WHERE category_2 = ' "+choice+" ' AND category_3 IS NOT NULL;"
    category_3_records = Database.select_rows_dict_cursor(db,query)
    return (category_3_records)
