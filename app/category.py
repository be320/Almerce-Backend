from .db_connection import Database

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




     


# def get_categories(cursor):
#     cursor.execute("select distinct category_1 from toys_shop.categories;")
#     category_1_records = cursor.fetchall()   
#     print(category_1_records)   
#     category_1 =["Skip"]
#     print(category_1_records)
   
#     for row in category_1_records:
#         category_1.append(row[0])
#     @app.route('/load_category1', methods=["POST"])
#     @cross_origin()
#     def r():
#         reply = {
#      	category_1
#         }
#     return jsonify(reply)


     