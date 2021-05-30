from .HotEncoder import *
def get_similar_products(user_parameters):
    data,fixed_user_parameters,products = hotEncode_categories(user_parameters)
    N_QUERY_RESULT = 5
    nbrs = NearestNeighbors(n_neighbors=N_QUERY_RESULT, algorithm = 'brute',metric=custom_metric).fit(data)

    user_input= list(fixed_user_parameters['category'])
    user_input.append(fixed_user_parameters['mean_price'])
    distances, indices = nbrs.kneighbors([user_input])
    print("Similarity distances")
    print(distances)

    print("error")
    global error
    sum2=0
    for distance in distances[0]:
        sum2+=distance
    error=sum2/len(distances) 
    print(error)

    similar_product_indices = indices.reshape(-1)

    global recommendations
    recommendations=[]
    for i in similar_product_indices:
        R = {}   
        id = products[i][0]
        query = "select name,image_name,description from toys_shop.products where product_id = "+str(id)+";"
        query_result = load_data_db(query)
        print(query_result)
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

    # print(similar_product_indices)
    # print(distances)
    # for i in similar_product_indices:
    #      print(data[i])

def custom_metric(X1,X2):
    cat1 = X1[:(len(X1)-1)]
    cat2 = X2[:(len(X2)-1)]
    price1 = X1[len(X1)-1]
    price2 = X2[len(X2)-1]
    category_distance = distance.jaccard(cat1, cat2) #measure dissamilarity between categories
    price_distance = abs( (price1-minPrice)/(maxPrice - minPrice) - (price2-minPrice)/(maxPrice - minPrice) ) #normalize mean prices: price 1 and price 2
    dist = math.sqrt(price_distance**2 + category_distance**2)
    return dist
