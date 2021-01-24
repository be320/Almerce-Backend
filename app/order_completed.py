def order_completed_details(data):
    details = {
    "event": "Order Completed",
    "product_id": data["properties"]["id"],
    "session_id": data["anonymousId"],
    "user_id": data["userId"],
    "timestamp": data["timestamp"]    
    }
    print(details)

    {
    event,
    product_id[],
    session_id,
    user_id,
    timestamp,
    sale_price[],
    regular_price[],
    categories
}