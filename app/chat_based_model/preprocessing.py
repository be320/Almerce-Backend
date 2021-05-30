from .HotEncoder import *
import time
def chat_based_model_preprocessing():
    while True:
        try:
            hot_encode_three_categories()
            save_database_products_to_file()
            break 
        except Exception as e:
            print("Connection to database failed")
            time.sleep(2)

def hot_encode_three_categories():
    postgreSQL_select_Query = "select * from toys_shop.categories;"
    categories = load_data_db(postgreSQL_select_Query)
    categories = np.array(categories)
    c1_names = categories[:,0].copy()
    c2_names = categories[:,1].copy()
    c3_names = categories[:,2].copy()

    c1=pd.get_dummies(c1_names).to_numpy() # c1 is the hot encoding of category1 names ex: c1 = [['1','0','0'],['0','0','1']] 
    c2=pd.get_dummies(c2_names).to_numpy() # c2 is the hot encoding of category2 names
    c3=pd.get_dummies(c3_names).to_numpy() # c3 is the hot encoding of category3 names

    np.save('c1_file', c1)
    np.save('c2_file', c2)
    np.save('c3_file', c3)

def save_database_products_to_file():
    query = "select product_id,categories_name,price from toys_shop.products;"
    products = load_data_db(query)
    np.save('products_file',products)

