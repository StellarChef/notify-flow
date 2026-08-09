from adapters import ShoperAdapter
from routers.shoper_client import fetch_full_order
from Database.repository import Repository
import os

"""raw = fetch_full_order("1062")
order = ShoperAdapter().parse(raw)
new_id = Repository.save_order(order)
print(f"Zapisano id={new_id}")"""

orders = Repository.fetch_orders()

for order in orders:
    print(order.order_id, order.status, order.customer.name)
