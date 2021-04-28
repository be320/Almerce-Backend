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
