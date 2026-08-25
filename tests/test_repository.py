import json
from pathlib import Path

from Database.repository import Repository
from Services.adapter import ShoperAdapter

FAKE_ORDERS = Path(__file__).parent.parent / "config" / "fake_orders"


# DEBUG: pretty-print every order in the DB as a table
def show():
    orders = Repository.fetch_all_orders()
    header = (
        f"{'order_id':<8} | {'status':>6} | {'customer':<20} | "
        f"{'prod':>4} | {'delivery':<14} | point / address"
    )
    print(header)
    print("-" * len(header))
    for o in orders:
        customer = f"{o.customer.name} {o.customer.lastname}"
        dest = o.delivery_point or o.delivery_address or "-"
        print(
            f"{o.order_id:<8} | {o.status:>6} | {customer:<20} | "
            f"{len(o.products):>4} | {o.delivery_method:<14} | {dest}"
        )
    print(f"\n({len(orders)} orders total)")


def add_to_database():
    files = sorted(FAKE_ORDERS.glob("*.json"))
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        order = ShoperAdapter.parse(raw)
        Repository.save_order(order)
        print(f"  pushed order {order.id}")
    print(f"({len(files)} orders pushed to DB)")


def demo():
    add_to_database()
    print()
    show()


if __name__ == "__main__":
    demo()
