from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_event_details
from .order_completed import order_completed_details
import timeit, functools
import os

from app.chat_based_model.Sequence import chat_based_messages
from app.chat_based_model.Preprocessing import chat_based_model_preprocessing
from app.chat_based_model.UserParameters import *
from app.chat_based_model.Knn import *
from .category import *
from app.image_based_model.sequence import image_based_messages
from app.image_based_model.imageModel import predictImages
from app.image_based_model.imageModel import get_imageBased_recommendations


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
chatBased_user_parameters = {}
Knn_exec_time = 0.0
ImgSerch_exec_time = 0.0
model_messages = ""
ages = {'من 0-1 سنه' : 0.5, 'من 1-2 سنه' : 1.5, 'من 2-3 سنه' : 2.5, 'من 3-4 سنه' : 3.5, 'من 4-5 سنه' : 4.5, 'من 5-6 سنه' : 5.5, 'اكثر من 6 سنوات' : 7}

#pre processing run once after every flask run
@app.before_first_request
def before_first_request():
    chat_based_model_preprocessing() # hot encoding the 3 categories & fetch products from database and saves it into file
            
#this message show to the user when an error occur
messages=[
    {
    "message": {"TextField": "متشكر علي تقيمك جدا عشان ده هيساعدني احسن من نفسي "},
    "elementType": "MessageTemplate",
    "choices": [],
    "choiceType":"AfterRestart"
},
]
# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    global chatBased_user_parameters # save user chosen category1,2 and 3
    global model_messages # specify model chosen by user
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    choice = temp["message"]["TextField"]
    data = {}

    #initialising model_messages
    if (index ==0):
        model_messages = "chat_based_messages"
    else:
        if(choice=="البحث عن طريق الاختيارات"):
            model_messages = "chat_based_messages"
        elif (choice =="البحث عن طريق الصور"):
            model_messages = "image_based_messages"
        elif (choice =="التحدث مع ألميرس"):
            model_messages = "text_based_messages"
    #---------------------------------------------------------------
    if model_messages == "chat_based_messages":
        if index >= 0 & index < len(chat_based_messages):
            data = chat_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'

            if data["choiceType"] == "category1":
                data["choices"]=get_categories1()

            elif data["choiceType"] == "category2":
                chatBased_user_parameters['category1']=choice
                category_2_records =get_categories2(choice)
                if not category_2_records:
                    data["choices"]=["NONE"]
                else:
                    category_2_records.append("NONE")
                    data["choices"]=category_2_records

            elif data["choiceType"] == "category3":
                chatBased_user_parameters['category2']=choice
                category_3_records =get_categories3(choice)
                if not category_3_records:
                    data["choices"]=["NONE"]
                else:
                    category_3_records.append("NONE")
                    data["choices"]=category_3_records

            elif data["choiceType"] == "price":
                chatBased_user_parameters['category3']=choice  

            elif data["choiceType"] == "gender":
                chatBased_user_parameters['age']=ages[choice]  
        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

        return jsonify(data)

    elif model_messages == "image_based_messages":
        if index >= 0 & index < len(image_based_messages):
            data = image_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'

        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

        return jsonify(data)


#assuming this will only be used with image_based_model
@app.route('/sendImagesList', methods=["POST"])
@cross_origin()
def sendImagesList():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    imageList = temp["imageList"]
    print(index)
    # print(imageList)
    data = {}
    if index >= 0 & index < len(image_based_messages):
        data = image_based_messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'
        global ImgSerch_exec_time
        ImgSerch_exec_time = timeit.timeit(functools.partial(predictImages,imageList[0]), number=1) 
        print(ImgSerch_exec_time)
        # get recommendations produced in image_based_messages folder
        imageBased_recommendations = get_imageBased_recommendations()
        print(imageBased_recommendations)
        if(imageBased_recommendations):
            print("imageBased_recommendations")
            print(imageBased_recommendations)
            data['cards'] = imageBased_recommendations
    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'
    return jsonify(data)

@app.route('/sendAudioMessage', methods=["POST"])
@cross_origin()
def sendAudioMessage():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    audio = temp["audio"]
    print(index)
    print(audio)
    data = {}
    if index >= 0 & index < len(messages):
        data = messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'
    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'
    print(data)
    return jsonify(data)


@app.route('/sendchangeRating', methods=["POST"])
@cross_origin()
def sendchangeRating():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    rating = temp["rating"]
    print(index)
    print(rating)
    data = {}
    if(model_messages == "chat_based_messages"):
        if index >= 0 & index < len(chat_based_messages):
            data = chat_based_messages[index]   
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'
        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'
        print(data)
        return jsonify(data)
    elif(model_messages == "image_based_messages"):
        if index >= 0 & index < len(image_based_messages):
            data = image_based_messages[index] 
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'
        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'
        print(data)
        return jsonify(data)
    
#assuming this will only be used with chat_based_model
@app.route('/sendpriceRange', methods=["POST"])
@cross_origin()
def sendpriceRange():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    price = temp["price"]
    print(index)
    print(price)
    chatBased_user_parameters['price']=price
    data = {}
    if index >= 0 & index < len(chat_based_messages):
        data = chat_based_messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'

        # calling get_similar_products(user_parameters)
        global Knn_exec_time
        Knn_exec_time = timeit.timeit(functools.partial(get_similar_products,chatBased_user_parameters), number=1) 
        print(Knn_exec_time)

        # get recommendations produced 
        chatBased_recommendations = get_chatBased_recommendations()
        if(chatBased_recommendations):
            print("chatBased_recommendations")
            print(chatBased_recommendations)
            data['cards'] = chatBased_recommendations
        
                    #time to execute functon
                # global Knn_exec_time
                # Knn_exec_time = timeit.timeit(functools.partial(get_similar_products,user_parameters), number=1) # calling get_similar_products(user_parameters) in HotEncoder.py
                # print(Knn_exec_time)
                # #for generating test cases for knn method
                # error = get_error()
                # new_test_case ={'category 1':user_parameters['category1'],'category 2':user_parameters['category2'],
                # 'category 3':user_parameters['category3'],'mean price':(min(user_parameters['price'])+max(user_parameters['price']))/2, 
                # 'error %':error*100, 'execution time (s)':Knn_exec_time}
                # global df
                # df = df.append(new_test_case, ignore_index=True)
                # df.to_csv('KNN_Test_Cases.csv',index=False)
                # print(df)
                # print(user_parameters)
                # print(error)
                # print("Time Taken To Execute get_similar_products (seconds): ",Knn_exec_time)

                #showing product cards
                # recommendations = get_recommendations()
                # if(recommendations):
                #     print("recommendations")
                #     print(recommendations)
                #     data['cards'] = recommendations

    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'

    print(data)
    return jsonify(data)

# Track Click Events
@app.route('/track', methods=["POST"])
def track():
    request_data = request.get_json()
    if "event" in request_data:
        event_type = request_data["event"]
        if event_type == "Order Completed":
            order_completed_details(request_data)
        else:
            product_event_details(request_data)
        data = {}
        data["reply"] = "Data Received"
        data["status"] = 'success'
        return jsonify(data)
    else:
        return ""

# # Load data from database to be used in model
# @app.route('/load_data', methods=["GET"])
# def load_data():
#     db_connect()
#     data = {}
#     data["reply"] = "Working!!!!!------------aaaaaaa"
#     data["status"] = 'success'
#     return jsonify(data)

# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"


# A welcome message to test our server
@app.route('/productcards', methods=["POST"])
@cross_origin()
def recommend():
    reply = {
        "elementType":"ProductCardTemplate",
        "cards":[{ "imgSrc" :"https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp","ProductUrl":"https://safwatoys.com/index.php?route=product/product&product_id=1049","productHeader":"لوحة تلوين بالرمل W50-2","productParagraph":"لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين"
        ,"id":"78"},{ "imgSrc" :"https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp","ProductUrl":"https://safwatoys.com/index.php?route=product/product&product_id=1049","productHeader":"لوحة تلوين بالرمل W50-2","productParagraph":"لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين"
        ,"id":"78"},{ "imgSrc" :"https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp","ProductUrl":"https://safwatoys.com/index.php?route=product/product&product_id=1049","productHeader":"لوحة تلوين بالرمل W50-2","productParagraph":"لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين"
        ,"id":"78"},{ "imgSrc" :"https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp","ProductUrl":"https://safwatoys.com/index.php?route=product/product&product_id=1049","productHeader":"لوحة تلوين بالرمل W50-2","productParagraph":"لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين"
        ,"id":"78"},{ "imgSrc" :"https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp","ProductUrl":"https://safwatoys.com/index.php?route=product/product&product_id=1049","productHeader":"لوحة تلوين بالرمل W50-2","productParagraph":"لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين"
        ,"id":"78"}]		
    }
    return jsonify(reply)


