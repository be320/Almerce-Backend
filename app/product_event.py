def product_event_details(data):
    details = {
    "event": data["event"],
    "product_id": data["properties"]["id"],
    "session_id": data["anonymousId"],
    "user_id": data["userId"],
    "timestamp": data["timestamp"]    
    }
    print(details)
