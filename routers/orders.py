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


@router.get("/orders/{order_id}")
def fetch_order(order_id: str):
    resp = requests.get(
        f"{shop_address}/orders/{order_id}",
        headers={"Authorization": f"Bearer {api_token}"},
    )
    resp_product = requests.get(
        f"{shop_address}/{order_id}-products",
        headers={"Authorization": f"Bearer {api_token}"},
    )

    return resp_product.json()
