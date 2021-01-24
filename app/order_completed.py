def order_completed_details(data):
    details = {
    "event": "Order Completed",
    "products_names": data["properties"]["Order Details"].split(" ,").replace("\xa0", ""),
    "session_id": data["anonymousId"],
    "user_id": data["userId"],
    "timestamp": data["timestamp"]    
    }
    print(details)