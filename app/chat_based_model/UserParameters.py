from app.db_connection import Database
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance
from .Kmeans import normalize_cat, bin_to_dec
import math 
import numpy as np
import pandas as pd
import pickle

error = 0.0

def get_error():
    return error

def hot_encoding_user_parameters(user_parameters):
    fixed_user_parameters = {}
    #load dictionary of categories names and their hot encodings
    with open('dictionary.pkl', 'rb') as handle:
        dictionary = pickle.load(handle)
    #load max price and min price
    with open('max_min_prices.pkl', 'rb') as handle:
        max_min_prices = pickle.load(handle)
    #load max age and min age
    with open('max_min_ages.pkl', 'rb') as handle:
        max_min_ages = pickle.load(handle)
    #load the lengths of category 1,2,3
    with open('c_len.pkl', 'rb') as handle:
        c_len = pickle.load(handle)
    cat1_zeroes = '0' * c_len[0]
    cat2_zeroes = '0' * c_len[1]
    cat3_zeroes = '0' * c_len[2]
    maxPrice = max_min_prices[0]
    minPrice = max_min_prices[1]
    maxAge = max_min_ages[0]
    minAge = max_min_ages[1]
    s =   "المتجر " + "> " + str(user_parameters['category1']) + " > " + str(user_parameters['category2']) + " > " + str(user_parameters['category3']) + " "
    s = s.replace("> NONE ","")
    categories = s.split('>')
    if len(categories) == 1:
        fixed_user_parameters['category'] = cat1_zeroes + cat2_zeroes + cat3_zeroes
    elif len(categories) == 2:
        fixed_user_parameters['category']=dictionary[categories[1]] + cat2_zeroes + cat3_zeroes
    elif len(categories) == 3:
        fixed_user_parameters['category']=dictionary[categories[1]] + dictionary[categories[2]] + cat3_zeroes
    else:
        fixed_user_parameters['category']=dictionary[categories[1]] + dictionary[categories[2]] + dictionary[categories[3]]
    mean_price = (min(user_parameters['price'])+max(user_parameters['price']))/2
    age = user_parameters['age']
    fixed_user_parameters['mean_price'] = (mean_price - minPrice) / (maxPrice - minPrice)
    fixed_user_parameters['age'] = (float(age) - float(minAge)) / (float(maxAge) - float(minAge))
    return fixed_user_parameters
    