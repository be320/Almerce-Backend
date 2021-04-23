import psycopg2
from psycopg2 import Error
from .product_event import *

#"""
#{
#    event,
#    product_id,
#    session_id,
#    user_id,
#    timestamp,
#    sale_price,
#    regular_price,
#    categories
#}
#"""

def db_connect():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="segment",
                                      password="Almerce2020",
                                      host="54.173.4.231",
                                      port="5432",
                                      database="clickstream")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        cursor.execute("select category_1 from toys_shop.categories")
        category_1_records = cursor.fetchall()      
        category_1 =[]
        for row in category_1_records:
        category_1.append(row[0])

        get_clicked_data(cursor)




    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")