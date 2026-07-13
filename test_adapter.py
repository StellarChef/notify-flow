import json

from adapters import ShoperAdapter


def load(path: str) -> dict:
    # errors="replace" - some dumps were saved without encoding="utf-8"
    with open(path, encoding="utf-8", errors="replace") as f:
        return json.load(f)


def show(path: str) -> None:
    raw = load(path)
    order = ShoperAdapter(raw).parse(raw)

    print("=" * 70)
    print(f"{path}  ->  Order {order.id}")
    print("=" * 70)
    print(f"  status           : {order.status.name}")
    print(f"  fulfillment_path : {order.fulfillment_path.name}")
    print(f"  ordered_at       : {order.fulfillment_date.ordered_at}")
    print(f"  ship_by          : {order.fulfillment_date.ship_by}")

    c = order.customer
    print(f"  customer         : {c.name} {c.lastname} | {c.email} | {c.phone}")

    d = order.delivery_method
    print(f"  delivery.method  : {d.method.name}")
    print(f"  delivery.point   : {d.point}")
    print(f"  delivery.address : {d.address}")
    print(f"  delivery.provider: [{d.provider.id}] {d.provider.name}")

    for p in order.products:
        print(f"  product          : {p.name}")
        print(f"    sku/qty/price  : {p.sku} / {p.quantity} / {p.price}")
        print(f"    attributes ({len(p.attributes)}):")
        for key, value in p.attributes.items():
            print(f"      - {key} => {value}")
    print()


if __name__ == "__main__":
    show("order_1057.json")   # shipping_id 1 -> PICKUP_POINT
    show("order_1052.json")   # shipping_id 2 -> HOME_DELIVERY
