from ..chat_based_model.Knn import get_similar_products,get_chatBased_recommendations

dummy =[]
temp = []
product_ids =[]

def get_temp():
    return temp
def reset_temp():
    global temp
    temp = []

def recommend_clicks(products_details):
    global dummy
    global temp
    global product_ids
    dummy =[]
    user_parameter = {}
    i = 0
    for product in products_details:
        if len(product[0][0].split(' > ')) > 1:
            user_parameter['category1'] = product[0][0].split(' > ')[1].rstrip().lstrip()
        else:
            user_parameter['category1'] = 'NONE'
            user_parameter['category2'] = 'NONE'
            user_parameter['category3'] = 'NONE'
        if len(product[0][0].split(' > ')) > 2:
            user_parameter['category2'] = product[0][0].split(' > ')[2].rstrip().lstrip()
        else:
            user_parameter['category2'] = 'NONE'
            user_parameter['category3'] = 'NONE'
        if len(product[0][0].split(' > ')) > 3:
            user_parameter['category3'] = product[0][0].split(' > ')[3].rstrip().lstrip()
        else:
            user_parameter['category3'] = 'NONE'

        print(product[0][1])
        user_parameter['price'] = [product[0][1], product[0][1]]
        user_parameter['age'] = product[0][2]
        product_id = product[0][3]

        if len(products_details) == 5:
            get_similar_products(user_parameter, 2)
            dummy.append(get_chatBased_recommendations())
            user_parameter = {}

        elif len(products_details) == 4:
            if (i == 0):
                get_similar_products(user_parameter, 3)
                dummy.append(get_chatBased_recommendations())
            else:
                get_similar_products(user_parameter, 2)
                dummy.append(get_chatBased_recommendations())
            i += 1
            user_parameter = {}

        elif len(products_details) == 3:
            if (i < 2):
                get_similar_products(user_parameter, 3)
                dummy.append(get_chatBased_recommendations())
            else:
                get_similar_products(user_parameter, 2)
                dummy.append(get_chatBased_recommendations())

            i += 1
            user_parameter = {}
        
        elif len(products_details) == 2:
            if (i == 0):
                get_similar_products(user_parameter, 4)
                dummy.append(get_chatBased_recommendations())               
            else:
                get_similar_products(user_parameter, 3)
                dummy.append(get_chatBased_recommendations())

            i += 1
            user_parameter = {}
        
        elif len(products_details) == 1:
            get_similar_products(user_parameter, 6)
            dummy.append(get_chatBased_recommendations())
            user_parameter = {}
            
        product_ids.append(product_id)
    print(product_ids)
    for d in dummy:
        for i in d:
            if(i['id'] not in product_ids):
                print(i['id'])
                temp.append(i)