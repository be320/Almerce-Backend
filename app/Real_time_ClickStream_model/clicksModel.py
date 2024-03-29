from app.db_connection import Database, load_data_db_clicks_model
from app.Real_time_ClickStream_model.clicks import recommend_clicks,get_temp

    
id_results = []
Clicks_recommendation =[]

def get_clicksBased_recommendations():
    return Clicks_recommendation
def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def predictClicks():
    global  id_results
    global Clicks_recommendation
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
    products_details = load_data_db_clicks_model(products)

    recommend_clicks(products_details)
    Clicks_recommendation = get_temp()


