import psycopg2
from psycopg2.extras import DictCursor
import time

class Database:
    """PostgreSQL Database class."""

    def __init__(
            self
        ):
        self.host = "54.173.4.231"
        self.username = "segment"
        self.password = "Almerce2020"
        self.port = "5432"
        self.dbname = "clickstream"
        #used to ensure that only a single connection exists for our database at any given time
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            while True:
                try:
                    self.conn = psycopg2.connect(
                        host=self.host,
                        user=self.username,
                        password=self.password,
                        port=self.port,
                        dbname=self.dbname
                    )
                    break
                except psycopg2.DatabaseError as e:
                    print(e)
                    time.sleep(1)
                    
                finally:
                    print("Connection opened successfully.")
    
    def select_rows_dict_cursor(self,query):
        """Run SELECT query and return list of dicts."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
            #print (records)
            # for row in records
            #     print(row['WRITE A COLUMN'S TITLE HERE'])
        cur.close()
        return records

    def insert_rows(self,query,record):
        """Run INSERT query FOR REALTIME CLICKS"""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query,record)
        self.conn.commit()
        print("Inserted Record Successfully")
        cursor.close()
        self.conn.close()
    
    def select_rows_dict_cursor_ids(self,id_results):
        """Run SELECT query and return list of dicts."""
        self.connect()
        recommendations=[]
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            for id in id_results:
                print(id)
                R = {}
                query = "select name,image_name,description from toys_shop.products where product_id = '" + str(
                    id) + "';"
                cur.execute(query)
                query_result = cur.fetchall()
                R['productHeader'] = query_result[0][0]
                R['imgSrc'] = query_result[0][1]
                if query_result[0][2] == None:
                    R['productParagraph'] = ""
                else:
                    R['productParagraph'] = query_result[0][2]

                R['id'] = str(id)
                nn = str(query_result[0][0])
                n = nn.replace(" ", "-")
                R['ProductUrl'] = "https://www.magaya.world/product/" + n + "/"
                recommendations.append(R)

            cur.close()
            return recommendations


    def select_rows_dict_cursor_clicks_model(self,products):
            """Run SELECT query and return list of dicts."""
            self.connect()
            recommendations=[]
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                for prod in products:
                    prod = prod[0]
                    query = "SELECT categories_name,price,age,product_id FROM toys_shop.products WHERE product_id = '"+str(prod)+"';"
                    cur.execute(query)
                    query_result = cur.fetchall()
                    recommendations.append(query_result)
                cur.close()
                return recommendations


def load_data_db(query):
    db=Database()
    result = Database.select_rows_dict_cursor(db,query)
    return result

def load_data_db_ids(ids):
    db=Database()
    result = Database.select_rows_dict_cursor_ids(db,ids)
    return result

def load_data_db_clicks_model(products):
    db=Database()
    result = Database.select_rows_dict_cursor_clicks_model(db,products)
    return result


def insert_data_db(query,record):
    print("insert_data_db called")
    db=Database()
    result = Database.insert_rows(db,query,record)
    return result
