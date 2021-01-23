from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from .product_event import product_added_details

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
    event_type = request_data["event"]
    if event_type == "Product Added":
        product_event_details(request_data)
    #elif event_type == "Product Clicked":

    #elif event_type == "Product Removed":

    #elif event_type == "Order Completed":
    
    #else:
    #    print("Other events not handled")

#    print(request_data)
    data = {}
    data["reply"] = "Data Received"
    data["status"] = 'success'
    return jsonify(data)


# A welcome message to test our server
@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our server !!</h1>"






