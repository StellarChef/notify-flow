from routers.shoper_client import fetch_orders
from Database.repository import Repository
import routers.schemas as s


class Service:
    def reception_from_shoper():
        uploaded_orders = (
            fetch_orders()
        )  # But its returning all of the orders with or without closed ones
        my_orders = Repository.fetch_orders()

        my_orders_ids = {order.order_id for order in my_orders}

        for uploaded_order in uploaded_orders:
            if uploaded_order["order_id"] not in my_orders_ids:
                Repository.save_order(s.Order(**uploaded_order))
