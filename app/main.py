from typing import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .click_event import saveClick
from .order_completed import order_completed_details
import timeit
import functools
import os
import random
from .db_connection import load_data_db

from app.chat_based_model.Sequence import chat_based_messages
from app.chat_based_model.Preprocessing import chat_based_model_preprocessing
from app.chat_based_model.UserParameters import *
from app.chat_based_model.Knn import *
from .category import *
from app.image_based_model.sequence import image_based_messages
from app.image_based_model.imageModel import predictImages, get_imageBased_recommendations
from app.Real_time_ClickStream_model.sequence import clicks_based_messages
from app.Real_time_ClickStream_model.clicksModel import predictClicks, get_clicksBased_recommendations
from app.Real_time_ClickStream_model.clicks import reset_temp
from app.nlp_based_model.sequence import text_based_messages
from app.history_based_model.sequence import history_based_messages

# from flask_ngrok import run_with_ngrok


from sklearn.model_selection import train_test_split

app = Flask(__name__)
# run_with_ngrok(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True
chatBased_user_parameters = {}
Knn_exec_time = 0.0
ImgSerch_exec_time = 0.0
model_messages = ""
counter = 0
ages = {'من 0-1 سنه': 0.5, 'من 1-2 سنه': 1.5, 'من 2-3 سنه': 2.5,
        'من 3-4 سنه': 3.5, 'من 4-5 سنه': 4.5, 'من 5-6 سنه': 5.5, 'اكثر من 6 سنوات': 7}

if os.stat('Kmeans_Test_Cases.csv').st_size == 0:
    df = pd.DataFrame(columns=['category_1', 'category_2', 'category_3',
                               'mean_price', 'mean_age', 'error%', 'execution_time_(s)'])
else:
    df = pd.read_csv('Kmeans_Test_Cases.csv')

# pre processing run once after every flask run


@app.before_first_request
def before_first_request():
    print("main.py >> before_first_request called")
    # hot encoding the 3 categories & fetch products from database and saves it into file
    chat_based_model_preprocessing()


# this message show to the user when an error occur
messages = [
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
    global chatBased_user_parameters  # save user chosen category1,2 and 3
    global model_messages  # specify model chosen by user
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    choice = temp["message"]["TextField"]
    data = {}

    # initialising model_messages
    if (index == 0):
        model_messages = "chat_based_messages"
    else:
        if(choice == "البحث عن طريق الاختيارات"):
            model_messages = "chat_based_messages"
        elif (choice == "البحث عن طريق الصور"):
            model_messages = "image_based_messages"
        elif (choice == "التحدث مع ألميرس"):
            model_messages = "text_based_messages"
        elif (choice == "البحث من خلال تصفح الويب سايت"):
            model_messages = "clicks_based_messages"
        elif (choice == "مش عارف"):
            model_messages = "history_based_messages"
    # ---------------------------------------------------------------
    if model_messages == "chat_based_messages":
        if index >= 0 & index < len(chat_based_messages):
            data = chat_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'

            if data["choiceType"] == "category1":
                data["choices"] = get_categories1()
                data["choices"].append("اختيار طريقة ترشيح اخرى")
                data["choices"].append("عودة")
            elif data["choiceType"] == "category2":
                chatBased_user_parameters['category1'] = choice
                category_2_records = get_categories2(choice)
                data["choices"].append("اختيار طريقة ترشيح اخرى")
                data["choices"].append("عودة")
                if not category_2_records:
                    data["choices"] = ["NONE"]
                else:
                    category_2_records.append("NONE")
                    data["choices"] = category_2_records

            elif data["choiceType"] == "category3":
                chatBased_user_parameters['category2'] = choice
                category_3_records = get_categories3(choice)
                data["choices"].append("اختيار طريقة ترشيح اخرى")
                data["choices"].append("عودة")
                if not category_3_records:
                    data["choices"] = ["NONE"]
                else:
                    category_3_records.append("NONE")
                    data["choices"] = category_3_records

            elif data["choiceType"] == "price":
                chatBased_user_parameters['category3'] = choice

            elif data["choiceType"] == "gender":
                chatBased_user_parameters['age'] = ages[choice]
        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

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

    elif model_messages == "clicks_based_messages":
        if index >= 0 & index < len(clicks_based_messages):
            data = clicks_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'

        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

    elif model_messages == "text_based_messages":
        if index >= 0 & index < len(text_based_messages):
            data = text_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'

        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

    elif model_messages == "history_based_messages":
        if index >= 0 & index < len(history_based_messages):
            data = history_based_messages[index]
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


# assuming this will only be used with image_based_model
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
        ImgSerch_exec_time = timeit.timeit(
            functools.partial(predictImages, imageList[0]), number=1)
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

    elif(model_messages == "clicks_based_messages"):
        if index >= 0 & index < len(clicks_based_messages):
            data = clicks_based_messages[index]
            data["serverSide"] = True
            data["index"] = index
            data["status"] = 'success'
        else:
            data = messages[0]
            data["message"] = "هناك عطل"
            data["elementType"] = "MessageTemplate"
            data["serverSide"] = True
            data["status"] = 'BAD REQUEST'

    elif(model_messages == "text_based_messages"):
        data = {
            "message": {"TextField": "تحب نساعدك بحاجة تاني؟"},
            "elementType": "ChoiceTemplate",
            "choices":  ["نعم"],
            "choiceType": "restart"
        }
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'

    elif(model_messages == "history_based_messages"):
        global counter
        if(rating < 4.0):
            ids = load_data_db("SELECT product_id FROM toys_shop.products")
            ids = np.array(ids)
            ids = np.reshape(ids, -1)
            random.seed(10)
            random.shuffle(ids)
            ids_chunks = [ids[x:x+5] for x in range(0, len(ids), 5)]
            cards = load_data_db_ids(ids_chunks[counter])
            counter = counter+1
            data = {
                'elementType': 'ProductCardTemplate',
                'cards': cards,
                'choiceType': 'ShowRecommendations'}

        else:
            data = {
                "message": {"TextField": "تحب نساعدك بحاجة تاني؟"},
                "elementType": "ChoiceTemplate",
                "choices":  ["نعم"],
                "choiceType": "restart"
            }
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'
    print(data)
    return jsonify(data)

# assuming this will only be used with chat_based_model


@app.route('/sendpriceRange', methods=["POST"])
@cross_origin()
def sendpriceRange():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    price = temp["price"]
    print(index)
    print(price)
    chatBased_user_parameters['price'] = price
    data = {}
    if index >= 0 & index < len(chat_based_messages):
        data = chat_based_messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'

        # calling get_similar_products(user_parameters)
        global Knn_exec_time
        Knn_exec_time = timeit.timeit(functools.partial(
            get_similar_products, chatBased_user_parameters), number=1)
        print(Knn_exec_time)

        # get recommendations produced
        chatBased_recommendations = get_chatBased_recommendations()
        if(chatBased_recommendations):
            print("chatBased_recommendations")
            print(chatBased_recommendations)
            data['cards'] = chatBased_recommendations

            # knn Test cases
            error = get_error()
            new_test_case = {'category_1': chatBased_user_parameters['category1'], 'category_2': chatBased_user_parameters['category2'],
                             'category_3': chatBased_user_parameters['category3'], 'mean_price': (min(chatBased_user_parameters['price'])+max(chatBased_user_parameters['price']))/2, 'mean_age': chatBased_user_parameters['age'],
                             'error%': error*100, 'execution_time_(s)': Knn_exec_time}
            global df
            df = df.append(new_test_case, ignore_index=True)
            df.to_csv('Kmeans_Test_Cases.csv', index=False)
            print(df)
            print(chatBased_user_parameters)
            print(error)
            print("Time Taken To Execute get_similar_products (seconds): ", Knn_exec_time)

    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'

    print(data)
    return jsonify(data)


# assuming this will only be used with clicks_based_model
@app.route('/recommendFromClicks', methods=["POST"])
def recommendFromClicks():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    choice = temp["message"]["TextField"]

    data = {}
    print("recommendFromClicks called")
    if index >= 0 & index < len(clicks_based_messages):
        data = clicks_based_messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'

        predictClicks()
        clicksBased_recommendations = get_clicksBased_recommendations()

        if(clicksBased_recommendations):
            print("clicksBased_recommendations")
            print(clicksBased_recommendations)
            data['cards'] = clicksBased_recommendations

        data["reply"] = "Data Received"
        data["status"] = 'success'
    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'
    reset_temp()
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
            saveClick(request_data)
        data = {}
        data["reply"] = "Data Received"
        data["status"] = 'success'
        return jsonify(data)
    else:
        return ""

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
        "elementType": "ProductCardTemplate",
        "cards": [{"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp", "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049", "productHeader": "لوحة تلوين بالرمل W50-2", "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "78"}, {"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp", "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049", "productHeader": "لوحة تلوين بالرمل W50-2", "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "78"}, {"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp", "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049", "productHeader": "لوحة تلوين بالرمل W50-2", "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "78"}, {"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp", "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049", "productHeader": "لوحة تلوين بالرمل W50-2", "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "78"}, {"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp", "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049", "productHeader": "لوحة تلوين بالرمل W50-2", "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "78"}]
    }
    return jsonify(reply)
