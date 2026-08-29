from models.enums import OrderStatus
from models.schemas import Order
from Database.repository import Repository
from fastapi import APIRouter, Depends, HTTPException
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


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    status: OrderStatus,
):
    order = Repository.fetch_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order = Serializer.to_schema(order)  # validate and convert to Pydantic model
    order.status = status
    Repository.upsert_order(order)

    # update_status_order(order.order_id, order.status)
    return {"status": "updated", "order_id": order.id, "new_status": order.status.value}


@router.get("/orders", response_model=list[Order])
def get_open_orders():
    orders = [Serializer.to_schema(order) for order in Repository.fetch_open_orders()]
    return orders
