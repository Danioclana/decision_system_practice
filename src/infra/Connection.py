import psycopg
from dotenv import load_dotenv
import os

class Connection:
    def __init__(self):
        load_dotenv()
        self.conn = None

    def get_connection(self):
        try:
            self.conn = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            return self.conn
        except Exception as e:
            print("Postgres Database Connection Error: ", e)
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            return True
        return False
