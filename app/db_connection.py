import psycopg2
from psycopg2.extras import DictCursor

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
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                print(error(e))
                raise e
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

