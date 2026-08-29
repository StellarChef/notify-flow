from models.schemas import Order
from Database.repository import Repository
from fastapi import APIRouter, Depends
from Services.service import Service
from Services.serializers import Serializer
from Services.shoper_client import update_status_order
import secrets
import json

router = APIRouter()


@router.post("/shoper/sync", response_model=list[Order])
def sync_and_return():
    Service.reception_from_shoper()
    return Repository.fetch_open_orders()


@router.put("/orders/{order_id}")
def update_order(order: Order):
    uploaded_order = Serializer.deserialize(order)
    Repository.save_order(uploaded_order)

    update_status_order(uploaded_order.order_id, uploaded_order.status)
    return {"status": "updated", "order_id": uploaded_order.order_id}


@router.get("/orders", response_model=list[Order])
def get_open_orders():
    orders = [Serializer.to_schema(order) for order in Repository.fetch_open_orders()]
    return orders
