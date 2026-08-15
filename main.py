from models.schemas import Order
from Database.repository import Repository
from fastapi import APIRouter
from Services.service import Service
from Services.serializers import Serializer

router = APIRouter()

orders = Repository.fetch_orders()


@router.post("/sync", response_model=list[Order])
def sync_and_return():
    Service.reception_from_shoper()
    return Repository.fetch_orders()


@router.post("/orders/order")
def response_captcha(order: dict):
    Serializer.deserialize(order)
    return {"status": "updated", "order_id": order.order_id}


