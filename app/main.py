from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_event_details
from .order_completed import order_completed_details
from .HotEncoder import *
from .category import  *
import timeit, functools
import os
import schedule
import time

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
user_parameters = {}

if os.stat('KNN_Test_Cases.csv').st_size == 0:
    df = pd.DataFrame(columns=['category 1','category 2','category 3','mean price', 'error %','execution time (s)'])
else:
    df = pd.read_csv('KNN_Test_Cases.csv')

#pre processing done once in the beginning
@app.before_first_request
def before_first_request():
    while True:
        try:
            # hot encoding the 3 categories
            postgreSQL_select_Query = "select * from toys_shop.categories;"
            categories = load_data_db(postgreSQL_select_Query)
            categories = np.array(categories)
            c1_names = categories[:,0].copy()
            c2_names = categories[:,1].copy()
            c3_names = categories[:,2].copy()
        
            c1=pd.get_dummies(c1_names).to_numpy() # c1 is the hot encoding of category1 names ex: c1 = [['1','0','0'],['0','0','1']] 
            c2=pd.get_dummies(c2_names).to_numpy() # c2 is the hot encoding of category2 names
            c3=pd.get_dummies(c3_names).to_numpy() # c3 is the hot encoding of category3 names

            np.save('c1_file', c1)
            np.save('c2_file', c2)
            np.save('c3_file', c3)
            
            # fetch products from database and saves it into file
            query = "select product_id,categories_name,price from toys_shop.products;"
            products = load_data_db(query)
            np.save('products_file',products)
            break 
        except Exception as e:
            print("Connection to database failed")


messages = [
{
    "message": {"TextField": " اهلا بيك، انا لسة تحت الانشاء فهسألك شوية اسئلة كدة عشان اعرف اساعدك..يلا نبدأ؟ ممكن اعرف سن الطفل اللي هيلعب باللعبة ؟"},
    "elementType": "ChoiceTemplate",
    "choices":  ["اكثر من 6 سنوات","من 5-6 سنه","من 4-5 سنه","من 3-4 سنه","من1-2 سنه","من 0-1 سنه"],
    "choiceType":"age"
},
{
    "message": {"TextField": "ممكن اعرف الطفل ولد و لا بنت ؟"},
    "elementType": "ChoiceTemplate",
    "choices": ["بنت", "ولد"],
    "choiceType":"gender"

},
{
    "message": {"TextField": "حضرتك تحب اللعبة من اني قسم تبع القائمة الاولي ؟"},
    "elementType": "ChoiceTemplate",
    "choices": [],
    "choiceType":"category1"
},
{
    "message": {"TextField":"حضرتك تحب اللعبة من اني قسم تبع القائمة الثانية ؟"},
    "elementType": "ChoiceTemplate",
    "choices": [],
    "choiceType":"category2"
},
    {
    "message": {"TextField":"حضرتك تحب اللعبة من اني قسم تبع القائمة الثالثة ؟"},
    "elementType": "ChoiceTemplate",
    "choices": [],
    "choiceType":"category3"

},
{
    "message": {"TextField": "طيب ممكن صورة او صور  للمنتج الي بتدور عليه"},
    "elementType": "MessageTemplate",
    "choices": [],
    "choiceType":"IMG"


},
{
    "message": {"TextField": " تمام جدا، تحب ادورلك في الاسعار من كام لكام؟"},
    "elementType": "PriceSliderTemplate",
    "choices": [],
    "choiceType":"None"


},
{
    "message": {"TextField": "انا خلاص لاقيت منتاجات مناسبة.. تحب اوريك الاقتراحات؟ "},
    "elementType": "ChoiceTemplate",
    "choices": ["نعم"],
    "choiceType":"None"


},
{
    "elementType": "ProductCardTemplate",
    "cards": [{"imgSrc": "https://safwatoys.com/image/cache/catalog/W50-2/x122c5919-e115-43fc-a6c8-d283ce0ffb72-230x230.jpg.pagespeed.ic.ZrBiS-lubg.webp",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&product_id=1049",
                "productHeader": "لوحة تلوين بالرمل W50-2",
                "productParagraph": "لوحة معها رمل ملون يقوم الطفل بلصقها ف مكانها المناسب حسب الصورة الملونة لتتحول الي صوره ملونه بشكل مميز ينمي العضلات الدقيقة واصابع اليد ومهارات التحكم تزيد ثقة الطفل بنفسه متاح عدة اشكال تساعد في تمييز الطفل للالوان وتنميه مهاره المطابقة مناسبه للاطفال فرط الحركه مناسب لسن 4 سنين", "id": "1049"},
                {"imgSrc": "https://safwatoys.com/image/cache/catalog/W5-11/W5--11-228x228.jpg",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&path=67_106&product_id=2017",
                "productHeader": "صيد سمك وسط W5-11",
                "productParagraph": "تقوم فكرتها علي صيد السمك بالصنارة أو صيدها بالشاكوش لأن به ثقب في المنتصف فيلتقط القطع", "id": "2017"},
                {"imgSrc": "https://safwatoys.com/image/cache/catalog/W37-67/w37-67-230x230.jpeg",
                "ProductUrl": "https://safwatoys.com/index.php?route=product/product&path=67_113&product_id=1846", "productHeader": "سلم وثعبان وليدو خشب w37-67", "productParagraph": "لعبة 2x1 لعبة السلم والثعبان وليدو في شكل جديد مقاس 30*30 سم خامة خشبية متينه جودة أعلى تعلم الطفل العد والارقام والعمليات الحسابية بطريقة ممتعه", "id": "1846"}
                ],
    "choiceType":"ShowRecommendations"

},
{
    "message": {"TextField": "متشكر علي تقيمك جدا عشان ده هيساعدني احسن من نفسي "},
    "elementType": "MessageTemplate",
    "choices": [],
    "choiceType":"None"


},
]

# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    global user_parameters
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    choice = temp["message"]["TextField"]
    choiceType = temp["choiceType"]
    data = {}
    if index >= 0 & index < len(messages):
        data = messages[index]
        data["serverSide"] = True
        data["index"] = index
        data["status"] = 'success'
        if data["choiceType"] == "category1":
            data["choices"]=get_categories1()

        elif data["choiceType"] == "category2":
            user_parameters['category1']=choice
            category_2_records =get_categories2(choice)
            if not category_2_records:
                data["choices"]=["NONE"]
            else:
                category_2_records.append("NONE")
                data["choices"]=category_2_records

        elif data["choiceType"] == "category3":
            user_parameters['category2']=choice
            category_3_records =get_categories3(choice)
            if not category_3_records:
                data["choices"]=["NONE"]
            else:
                category_3_records.append("NONE")
                data["choices"]=category_3_records

        elif data["choiceType"] == "IMG":
            user_parameters['category3']=choice

        elif data["choiceType"] == "ShowRecommendations":
            global Knn_exec_time #time to execute functon
            Knn_exec_time = timeit.timeit(functools.partial(get_similar_products,user_parameters), number=1) # calling get_similar_products(user_parameters) in HotEncoder.py
            
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
            recommendations = get_recommendations()
            if(recommendations):
                data['cards'] = recommendations
       
    else:
        data = messages[0]
        data["message"] = "هناك عطل"
        data["elementType"] = "MessageTemplate"
        data["serverSide"] = True
        data["status"] = 'BAD REQUEST'

    return jsonify(data)


@app.route('/sendImagesList', methods=["POST"])
@cross_origin()
def sendImagesList():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    imageList = temp["imageList"]
    print(index)
    #print(imageList)
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

@app.route('/sendpriceRange', methods=["POST"])
@cross_origin()
def sendpriceRange():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    price = temp["price"]
    print(index)
    print(price)
    user_parameters['price']=price
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


