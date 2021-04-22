from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_event_details
from .order_completed import order_completed_details
from .db_connection import db_connect


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

messages = [
    {
        "message": {"TextField": " اهلا بيك، انا لسة تحت الانشاء فسألك شوية اسئلة كدة عشان اعرف اساعدك..يلا نبدأ؟\n ممكن اعرف سن الطفل اللي هيلعب باللعبة ؟"},
        "elementType": "ChoiceTemplate",
        "choices":  ["اكثر من 6 سنوات","من 5-6 سنه","من 4-5 سنه","من 3-4 سنه","من1-2 سنه","من 0-1 سنه"]


    },
    {
        "message": {"TextField": "ممكن اعرف الطفل ولد و لا بنت ؟"},
        "elementType": "ChoiceTemplate",
        "choices": ["بنت", "ولد"]

    },
    {
        "message": {"TextField": "ايه هي المهارات اللي عايز اللعبة تنميها عند الطفل باللعبة ؟"},
        "elementType": "ChoiceTemplate",
        "choices": [
            "العاب تركيز و انتباه",
            "التركيب و البناء",
            "المطابقة و التصنيف",
            "العاب البازل",
            "العاب البيبي",
            "تعليمي",
             "العاب جماعيه",
              "العاب العلوم",
            "المجسمات",
            "العاب تمثيليه",
             "أشغال يدوية و فنون",
             "الاشكال الهندسيه و الكسور"
             ]

    },
    {
        "message": {"TextField": "حضرتك تحب اللعبة من اني قسم ؟"},
        "elementType": "ChoiceTemplate",
        "choices": [
            "كتب تعليميه وسلاسل قصصية",
            "كروت تخاطب",
            "العاب خارجية وتجهيزات",
            "العاب ترفيهيه",
            "كتب مونتسوري",
            "أدوات مونتسوري",
             "العاب تنمية المهارات"
             ]

    },
    {
        "message": {"TextField": "طيب ممكن صورة او صور  للمنتج الي بتدور عليه"},
        "elementType": "MessageTemplate",
        "choices": []

    },
    {
        "message": {"TextField": " تمام جدا، تحب ادورلك في الاسعار من كام لكام؟"},
        "elementType": "SliderTemplate",
        "choices": []

    },
    {
        "message": {"TextField": "انا خلاص لاقيت منتاجات مناسبة.. تحب اوريك الاقتراحات؟ "},
        "elementType": "ChoiceTemplate",
        "choices": ["نعم"]

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
                   ]
    },

    {
        "message": {},
        "elementType": "StarRatingTemplate",
        "choices": []

    },
    {
        "message": {"TextField": "متشكر علي تقيمك جدا عشان ده هيساعدني احسن من نفسي "},
        "elementType": "MessageTemplate",
        "choices": []

    },
]


# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    choice = temp["message"]["TextField"]
    print(index)
    print(choice)
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


@app.route('/sendImagesList', methods=["POST"])
@cross_origin()
def sendImagesList():
    request_data = request.get_json()
    temp = request_data["Template"]
    index = temp["index"]
    imageList = temp["imageList"]
    print(index)
    print(imageList)
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


# Load data from database to be used in model
@app.route('/load_data', methods=["GET"])
def load_data():
    db_connect()
    data = {}
    data["reply"] = "Working!!!!!------------aaaaaaa"
    data["status"] = 'success'
    return jsonify(data)



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
