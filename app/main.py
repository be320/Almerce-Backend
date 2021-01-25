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
        "message": {"Textfield":"ممكن اعرف سن الطفل اللي هيلعب باللعبة ؟"},
        "elementType": "MessageTemplate",
        "choices": []

    },
    {
        "message": {"Textfield":"ممكن اعرف الطفل ولد و لا بنت ؟"},
        "elementType": "ChoiceTemplate",
        "choices": ["بنت", "ولد"]

    },
    {
        "message": {"Textfield":"ايه هي المهارات اللي عايز اللعبة تنميها عند الطفل باللعبة ؟"},
        "elementType": "ChoiceTemplate",
        "choices": ["الحساب", "الذاكرة", "الذكاء", "ال"]

    },
    {
        "message": {"Textfield":"حضرتك تحب اللعبة من اني قسم ؟"},
        "elementType": "ChoiceTemplate",
        "choices": ["الحساب", "الذاكرة", "الذكاء"]

    },
    {
        "message": {"Textfield":"حضرتك تحب تكون اللعبه بنظام التعليم مونتيسوري ؟"},
        "elementType": "ChoiceTemplate",
        "choices": ["نعم", "لا"]

    },
    {
        "message": {"Textfield":"تحب ادورلك في الاسعار من كام لكام ؟"},
        "elementType": "MessageTemplate",
        "choices": []

    }

]


# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    request_data = request.get_json()
    index = request_data["index"]
    index = 0
    data = {}
    if index>=0 & index<len(messages):
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
