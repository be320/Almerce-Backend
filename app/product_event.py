from .db_connection import Database

def product_event_details(data):
    details = {
    "event": data["event"],
    "product_id": data["properties"]["id"],
    "session_id": data["anonymousId"],
    "user_id": data["userId"],
    "timestamp": data["timestamp"]    
    }
    print(details)

def get_clicked_data():
    data = []

    db=Database()
    postgreSQL_select_Query = "select * from toys_shop.product_clicked;"
    product_clicked_records = Database.select_rows_dict_cursor(db,postgreSQL_select_Query)
    print("Print each row and its columns values")
    print(product_clicked_records)
    for row in product_clicked_records:
        product_id = row['_id']
#        print("Product ID  = ", row[12])
#        print("Event = ", row[3])
#        print("Session ID = ", row[13])
#        print("Timestamp = ", row[18], "\n")
        postgreSQL_select_Query = "select * from toys_shop.products where product_id = "+product_id+"::varchar;"
        detailed_product = Database.select_rows_dict_cursor(db,postgreSQL_select_Query)
        print(detailed_product)
#        print(len(detailed_product))
#        print("Sale Price = ", detailed_product[0][3])
#        print("Regular Price = ", detailed_product[0][4])
#        print("Category = ", detailed_product[0][5])
    return data
