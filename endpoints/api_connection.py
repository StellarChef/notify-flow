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
    uploaded_order = Serializer.deserialize(order)
    Repository.save_order(uploaded_order)
    return {"status": "updated", "order_id": uploaded_order.order_id}

@router.put("")
def put_order(order: Order):
    #Repository.fetch_order() fetch order updated_order from db
    #Services.deserialised_order pack order to shipp to the shoper
    #shoper_client.update_status_order(updated_order)
    return {"status": "succesfully updated", "order_id": order.order_id}

@router.post("")
def post_order(orders: list[Order]):
    s_orders = []
    for order in orders:
        s_orders.append(Service.serialize(order))
        #Services.deserialised_order pack order to shipp to the shoper
    #shoper_client.update_status_order(updated_order)
    return {"status": "succesfully updated", "order_id": order.order_id}
