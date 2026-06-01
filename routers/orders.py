from fastapi import APIRouter
from routers.schemas import OrderJSON

router = APIRouter()


@router.post("/orders")
def order_request(order: OrderJSON):
    return order.order_id
