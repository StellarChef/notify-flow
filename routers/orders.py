from fastapi import APIRouter

# from schemas import OrderJSON,enums
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

api_token = os.getenv("SHOPER_API_KEY")
client_id = os.getenv("SHOPER_CLIENT_ID")
shop_address = os.getenv("SHOP_ADDRESS")

router = APIRouter()


# @router.post("/orders")
# def order_request(order: OrderJSON):
# return order.order_id


# @router.get("/orders")
# def export(orders):
#    return orders


def fetch_full_order(order_id: str) -> dict:
    headers = {"Authorization": f"Bearer {api_token}"}

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


resp = fetch_full_order("1057")

with open("mok_order_1.json", "w") as w:
    json.dump(resp, w, ensure_ascii=False, indent=2)
