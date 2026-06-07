# Database do przetrzymywania stanu.
from dotenv import load_dotenv
import psycopg2
import os
from routers.schemas import OrderJSON
from psycopg2.extras import Json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        self.cursor = self.conn.cursor()

    def push_order(self, order: OrderJSON):
        query = """
                INSERT INTO orders (
                    order_id,
                    status,
                    data
                    ) VALUES (%s, %s, %s)
                """
        self.cursor.execute(
            query,
            (
                order.order_id,
                order.status.value,
                Json(order.model_dump(mode="json")),
            ),
        )
        self.conn.commit()

    def fetch_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()
