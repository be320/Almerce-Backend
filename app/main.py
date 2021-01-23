from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_event_details

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Text Messages
@app.route('/sendText', methods=["POST"])
@cross_origin()
def sendText():
    request_data = request.get_json()
    print(request_data)
    request_data["Template"]["serverSide"] = True
    data = {}
    data["reply"] = "Data Received"
    data["status"] = 'success'
    return jsonify(request_data)


# Track Click Events
@app.route('/track', methods=["POST"])
def track():
    request_data = request.get_json()
    if "event" in request_data:
        event_type = request_data["event"]
        if event_type == "Order Completed":
#            order_completed_details(request_data)
            print("Order Completed")
        else:
            product_event_details(request_data)
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






