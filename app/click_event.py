from .db_connection import Database
from .db_connection import insert_data_db

def saveClick(data):
    details = {
    "event": data["event"],
    "product_id": data["properties"]["id"],
    "session_id": data["anonymousId"],
    "timestamp": data["timestamp"]    
    }
    postgres_insert_query = """ INSERT INTO toys_shop.realtime_clicks (event, product_id, session_id,timestamp) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (details["event"], details["product_id"], details["session_id"], details["timestamp"])
    insert_data_db(postgres_insert_query,record_to_insert)
    print(details)

