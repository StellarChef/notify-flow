from fastapi import APIRouter

# from schemas import OrderJSON,enums
from dotenv import load_dotenv
import requests
import os
import json
from routers.enums import OrderStatus

load_dotenv()

api_token = os.getenv("SHOPER_API_KEY")
client_id = os.getenv("SHOPER_CLIENT_ID")
shop_address = os.getenv("SHOP_ADDRESS")
headers = {"Authorization": f"Bearer {api_token}"}


def fetch_full_order(order_id: str) -> dict:

    # attempt 1: the API may return products on its own with the extended flag
    order = requests.get(
        f"{shop_address}/orders/{order_id}",
        params={"extended": "true"},
        headers=headers,
    ).json()

    # if products are missing, fetch them separately and attach
    if "products" not in order:
        products = requests.get(
            f"{shop_address}/order-products",
            params={"filters": json.dumps({"order_id": str(order_id)})},
            headers=headers,
        ).json()
        order["products"] = products.get("list", [])

    with open(f"order_{order_id}.json", "w", encoding="utf-8") as f:
        json.dump(order, f, ensure_ascii=False, indent=2)

    return order


# paginacja w api shopera ?


def fetch_orders() -> dict:
    orders = requests.get(
        f"{shop_address}/orders/",
        params={"extended": "true"},
        headers=headers,
        timeout=20,
    )
    orders.encoding = "utf-8"
    data = orders.json()
    filtered = []
    for order in data.get("list", []):
        try:
            status_id = int(order.get("status_id"))
        except (TypeError, ValueError):
            continue
        if OrderStatus(status_id) is not OrderStatus.CLOSED:
            filtered.append(order)
    return filtered


def update_status_order(order_id: str, status_id: int) -> None:
    response = requests.put(
        f"{shop_address}/orders/{order_id}",
        json={"status_id": status_id},
        headers=headers,
    )
    response.raise_for_status()


with open("orders.json", "w", encoding="utf-8") as f:
    json.dump(fetch_orders(), f, ensure_ascii=False, indent=2)
