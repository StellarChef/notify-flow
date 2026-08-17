from models.schemas import Order
from Database.repository import Repository
from fastapi import APIRouter
from Services.service import Service
from Services.serializers import Serializer
from routers.shoper_client import update_status_order

router = APIRouter()

orders = Repository.fetch_orders()


@router.post("/sync", response_model=list[Order])
def sync_and_return():
    Service.reception_from_shoper()
    return Repository.fetch_orders()


@router.post("/orders/order", response_model=Order)
def update_order(order: Order):
    uploaded_order = Serializer.deserialize(order)
    Repository.save_order(uploaded_order)

    update_status_order(uploaded_order.order_id, uploaded_order.status)
    return {"status": "updated", "order_id": uploaded_order.order_id}


@router.post("")
def post_order():
    orders_dict = {}
    orders = Repository.fetch_open_orders()
    for order in orders:
        orders_dict.add(Serializer.serialize(order))

    return {"success": "true", "orders": orders_dict}
