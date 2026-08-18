from Services.shoper_client import fetch_open_orders
from Services.adapter import ShoperAdapter
from Database.repository import Repository


class Service:
    @staticmethod
    def reception_from_shoper():
        uploaded_orders = fetch_open_orders()
        my_orders = Repository.fetch_open_orders()

        my_orders_ids = {order.order_id for order in my_orders}

        for uploaded_order in uploaded_orders:
            if uploaded_order["order_id"] not in my_orders_ids:
                Repository.save_order(ShoperAdapter.parse(uploaded_order))

    def reception_from_warehouse():
        return  # build this
