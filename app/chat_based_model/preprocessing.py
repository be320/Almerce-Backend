from .UserParameters import *
import time
import pickle
from ..db_connection import load_data_db

def chat_based_model_preprocessing():
    while True:
        try:
            hot_encode_three_categories()
            save_database_products_to_file()
            data_preprocessing()
            break 
        except Exception as e:
            print("Connection to database failed")
            time.sleep(2)

def hot_encode_three_categories():
    postgreSQL_select_Query = "select * from toys_shop.categories;"
    categories = load_data_db(postgreSQL_select_Query)
    categories = np.array(categories)    
    # c_names is ['المتجر > كتب تعليمية وسلاسل قصصية > بطاقات ', 'المتجر > تنمية المهارات > العاب العلوم '] of all 38 (till now) distinct categories_name 
    c1_names = categories[:,0].copy()
    c2_names = categories[:,1].copy()
    c3_names = categories[:,2].copy()
    
    # c1_str,c2_str,c3_str are 1D arrays of strings, each string is the hot encode of a category consisting of multiple bits
    # ex: c1_str = ['100','001'] 
    c1_str = []
    c2_str = []
    c3_str = []

    # c1,c2,c3 are the hotencode category1,category2,category3
    # Array of arrays, each array consits of many strings, each string is a bit (0 or 1)
    # ex: c1 = [['1','0','0'],['0','0','1']] 
    c1=pd.get_dummies(c1_names).to_numpy() # c1 is the hot encoding of category1 names ex: c1 = [['1','0','0'],['0','0','1']] 
    c2=pd.get_dummies(c2_names).to_numpy() # c2 is the hot encoding of category2 names
    c3=pd.get_dummies(c3_names).to_numpy() # c3 is the hot encoding of category3 names

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

    # c_codes is ['000010','0000100000001000000000001','01000000'] where c_codes saves all the hot encodings of all categories
    c_codes=np.concatenate((c1_str, c2_str, c3_str), axis=None)
    # c_names is [' مجموعات ضمنية وكروت تخاطب ' ' منتسوري ' ' منتسوري ' ' منتسوري '] where c_codes saves all names of all categories
    c_names = np.concatenate((c1_names, c2_names, c3_names), axis=None)
    dictionary = dict(zip(c_names, c_codes))
    with open('dictionary.pkl', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
    c_len = [len(c1[0]), len(c2[0]), len(c3[0])]
    with open('c_len.pkl', 'wb') as handle:
        pickle.dump(c_len, handle)


def data_preprocessing():

    query = "select product_id,categories_name,price from toys_shop.products where price <= 3000;"
    products = load_data_db(query)  
    
    with open('dictionary.pkl', 'rb') as handle:
        dictionary = pickle.load(handle)

    data = []
    prices = []
    for product in products:
        #prices (bara el for loop) collects all product's prices to be able to calculate max and min price
        prices.append(product[2])
    maxPrice = max(prices)
    minPrice = min(prices)
    #save max price and min price in a file to be used in normalizing fixed_user_parameters
    with open('max_min_prices.pkl', 'wb') as handle:
            pickle.dump([maxPrice, minPrice], handle)
    #load the lengths of category 1,2,3
    with open('c_len.pkl', 'rb') as handle:
        c_len = pickle.load(handle)
    cat1_zeroes = '0' * c_len[0]
    cat2_zeroes = '0' * c_len[1]
    cat3_zeroes = '0' * c_len[2]

    for product in products:
        # hot encode each category name and append it into "row" list
        s = ""
        s = str(product[1])
        categories = s.split('>')
        if len(categories) == 1:
            product[1] = cat1_zeroes + cat2_zeroes + cat3_zeroes
        elif len(categories) == 2:
            product[1]=dictionary[categories[1]] + cat2_zeroes + cat3_zeroes
        elif len(categories) == 3:
            product[1]=dictionary[categories[1]] + dictionary[categories[2]] + cat3_zeroes
        else:
            product[1]=dictionary[categories[1]] + dictionary[categories[2]] + dictionary[categories[3]]
        row = list(map(int, product[1])) #[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #append price to "row" making it last item in it
        row.append((product[2] - minPrice) / (maxPrice - minPrice))
        #data (bara el for loop) array of arrays
        data.append(row)
    #save the data list [0,1,0,0,0,0,1,.....,0,0.15] to a file
    with open('data.pkl', 'wb') as handle:
        pickle.dump(data, handle)
    #save the products list [148,'00100001000000001',0.15] to a file
    with open('products.pkl', 'wb') as handle:
        pickle.dump(products, handle)





def save_database_products_to_file():
    query = "select product_id,categories_name,price from toys_shop.products where price <= 3000;"
    products = load_data_db(query)
    np.save('products_file',products)

