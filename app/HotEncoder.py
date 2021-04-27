from .db_connection import Database
import pandas as pd

def load_categories(query):
    db=Database()
    categories = Database.select_rows_dict_cursor(db,query)
    return categories

def hotEncode_category_1():
    postgreSQL_select_Query = "select distinct category_1 from toys_shop.categories WHERE category_1 IS NOT NULL;"
    categories = load_categories(postgreSQL_select_Query)
    data = []
    for row in categories:
        data.append(row[0])
    s=pd.get_dummies(data)
    print(s)
    return s


def hotEncode_category_2():
    postgreSQL_select_Query = "select distinct category_2 from toys_shop.categories WHERE category_2 IS NOT NULL;"
    categories = load_categories(postgreSQL_select_Query)
    data = []
    for row in categories:
        data.append(row[0])
    s=pd.get_dummies(data)
    #print(s)
    return s

def hotEncode_category_3():
    postgreSQL_select_Query = "select distinct category_3 from toys_shop.categories WHERE category_3 IS NOT NULL;"
    categories = load_categories(postgreSQL_select_Query)
    data = []
    for row in categories:
        data.append(row[0])
    s=pd.get_dummies(data)
    #print(s)
    return s
    
def hotEncode_categories():
    c1 = hotEncode_category_1()
    c1_names=c1.columns.values.tolist()
    c1=c1.to_numpy()
    print (c1_names)
    print (c1)
    c2 = hotEncode_category_2()
    c3 = hotEncode_category_3()


    
     

