from app.chat_based_model.Kmeans import kmeans
from .UserParameters import *
from ..db_connection import load_data_db


recommendations=[]

def get_chatBased_recommendations():
    return recommendations


def get_similar_products(user_parameters):
    fixed_user_parameters = hot_encoding_user_parameters(user_parameters)
    # with open('data.pkl', 'rb') as handle:
    #     data = pickle.load(handle)
    # with open('products.pkl', 'rb') as handle:
    #     products = pickle.load(handle)
    with open('kmeans.pkl', 'rb') as handle:
        kmeans = pickle.load(handle)
    with open('max_min_cat.pkl', 'rb') as handle:
        max_min_cat = pickle.load(handle)
    with open('clust.pkl', 'rb') as handle:
        clust = pickle.load(handle)
    with open('encoded_clust.pkl', 'rb') as handle:
        encoded_clust = pickle.load(handle)
    maxCat = max_min_cat[0]
    minCat = max_min_cat[1]
    selected_cluster = kmeans.predict(X = [[normalize_cat(bin_to_dec(fixed_user_parameters['category']), maxCat, minCat),fixed_user_parameters['mean_price']]])
    data = encoded_clust[selected_cluster[0]]
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
    error=sum2/len(distances[0]) 
    print(error)

    similar_product_indices = indices.reshape(-1)

    global recommendations
    recommendations=[]
    products = clust[selected_cluster[0]]
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

def custom_metric(X1,X2):
    cat1 = X1[:(len(X1)-1)]
    cat2 = X2[:(len(X2)-1)]
    price1 = X1[len(X1)-1]
    price2 = X2[len(X2)-1]
    category_distance = distance.jaccard(cat1, cat2) #measure dissamilarity between categories
    price_distance = abs(price1 - price2) #normalize mean prices: price 1 and price 2
    dist = math.sqrt(price_distance**2 + category_distance**2)
    return dist