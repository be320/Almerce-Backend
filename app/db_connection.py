import psycopg2
from psycopg2 import Error

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

        postgreSQL_select_Query = "select * from toys_shop.product_clicked"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from product_clicked table using cursor.fetchall")
        product_clicked_records = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in product_clicked_records:
            print("Product ID  = ", row[12])
            print("Event = ", row[3])
            print("Session ID = ", row[13])
            print("Timestamp = ", row[18], "\n")



    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")