from fastapi import APIRouter
from routers.schemas import OrderJSON

router = APIRouter()


@router.post("/orders")
def order_request(order: OrderJSON):
    return order.order_id


@router.get("/orders")
def export(orders):
    return orders
