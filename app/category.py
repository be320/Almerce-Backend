def get_categories:
    cursor.execute("select category_1 from toys_shop.categories")
    category_1_records = cursor.fetchall()      
    category_1 =[]
    for row in category_1_records:
    category_1.append(row[0])
    return category_1