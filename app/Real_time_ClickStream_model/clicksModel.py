from app.db_connection import Database
from app.Real_time_ClickStream_model.clicks import get_dummy, recommend_clicks

    
id_results = []
recommendations=[]
def get_clicksBased_recommendations():
    return recommendations


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def predictClicks():
    global  id_results
    global recommendations
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
    recommend_clicks(products_details)
    recommendations = get_dummy()

def get_clicksBased_recommendations():
    return recommendations

