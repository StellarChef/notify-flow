from adapters import ShoperAdapter
from routers.shoper_client import fetch_full_order
from routers.schemas import Order
from Database.repository import Repository
import os
from fastapi import APIRouter
from service import Service

router = APIRouter()

orders = Repository.fetch_orders()


@router.post("/sync", response_model=list[Order])
def sync_and_return():
    Service.reception_from_shoper()
    return Repository.fetch_orders()


@router.post("/orders/order")
def update_order_db(order: Order):
    Repository.save_order(order)
    return {"status": "updated", "order_id": order.order_id}
