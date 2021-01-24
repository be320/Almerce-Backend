from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_event_details
from .order_completed import order_completed_details
from .db_connection import db_connect


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

questions = [
    {
        "question": "ممكن اعرف سن الطفل اللي هيلعب باللعبة ؟",
        "responseType": "single-numeric",
        "choices": []

    },
    {
        "question": "ممكن اعرف الطفل ولد و لا بنت ؟",
        "responseType": "choice",
        "choices": ["بنت", "ولد"]

    },
    {
        "question": "ايه هي المهارات اللي عايز اللعبة تنميها عند الطفل باللعبة ؟",
        "responseType": "choice",
        "choices": ["الحساب", "الذاكرة", "الذكاء", "ال"]

    },
    {
        "question": "حضرتك تحب اللعبة من اني قسم ؟",
        "responseType": "choice",
        "choices": ["الحساب", "الذاكرة", "الذكاء"]

    },
    {
        "question": "حضرتك تحب تكون اللعبه بنظام التعليم مونتيسوري ؟",
        "responseType": "choice",
        "choices": ["نعم", "لا"]

    },
    {
        "question": "تحب ادورلك في الاسعار من كام لكام ؟",
        "responseType": "range",
        "choices": []

    }

]


# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    request_data = request.get_json()
    index = request_data["index"]
    data = {}
    if index>0 & index<len(questions):
        data = questions[index]
        data["Template"]["serverSide"] = True
        data["status"] = 'success'
    else:
        data = questions[0]
        data["question"] = "هناك عطل"
        data["responseType"] = "string"
        data["Template"]["serverSide"] = True
        data["status"] = 'error'
    print(data)
    return jsonify(request_data)


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


@app.route('/almercesays', methods=["POST"])
@cross_origin()
def almercesays():
    return
