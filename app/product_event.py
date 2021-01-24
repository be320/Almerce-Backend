def product_event_details(data):
    details = {
    "event": data["event"],
    "product_id": data["properties"]["id"],
    "session_id": data["anonymousId"],
    "user_id": data["userId"],
    "timestamp": data["timestamp"]    
    }
    print(details)


def get_clicked_data(cursor):
    data = []
    postgreSQL_select_Query = "select * from toys_shop.product_clicked"

    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from product_clicked table using cursor.fetchall")
    product_clicked_records = cursor.fetchall()

    print("Print each row and it's columns values")
    for row in product_clicked_records:
        product_id = row[12]
        print("Product ID  = ", row[12])
        print("Event = ", row[3])
        print("Session ID = ", row[13])
        print("Timestamp = ", row[18], "\n")
        postgreSQL_select_Query = "select * from toys_shop.products where id = "+str(product_id)+"::varchar"
        cursor.execute(postgreSQL_select_Query)
        detailed_product = cursor.fetchone()[0]
        print("Sale Price = ", detailed_product[3])
        print("Regular Price = ", detailed_product[4])
        print("Category = ", detailed_product[5])

    return data
