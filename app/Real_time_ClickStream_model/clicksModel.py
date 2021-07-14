from app.db_connection import Database

    
id_results = []
recommendations=[]


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def predictClicks():
    global  id_results
    query = "SELECT session_id FROM toys_shop.realtime_clicks;"
    users = load_data_db(query)  
    last_user = users[len(users)-1][0]
    query = "SELECT product_id FROM toys_shop.realtime_clicks WHERE session_id = '" +str(last_user)+"';"
    products = load_data_db(query)
    products = products[::-1]
    if len(products) > 5:
        products = products[:5] 
    id_results = products
    products_details = []
    for prod in products:
        prod = prod[0]
        query = "SELECT categories_name,price,age FROM toys_shop.products WHERE product_id = '"+str(prod)+"';"
        prod = load_data_db(query)
        products_details.append(prod)
    print(products_details)
    get_similar_products()



def get_similar_products():
    global recommendations
    for id in id_results:
        print(id)
        R = {}   
        query = "select name,image_name,description from toys_shop.products where product_id = "+str(id)+";"
        query_result = load_data_db(query)
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


def get_clicksBased_recommendations():
    return recommendations
