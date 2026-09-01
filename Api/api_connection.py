from models.enums import OrderStatus
from models.schemas import Order
from Database.repository import Repository
from fastapi import APIRouter, Depends, HTTPException
from Services.serializers import Serializer
from Api.auth import get_current_active_user

# NOTE: nothing here calls Shoper. Outbound sync (Services/service.py and
# Services/shoper_client.py) is left in the repo but no longer exposed as an
# endpoint - the inbound webhook is the only live Shoper integration for now.

# One guard for the whole router: every route below requires a valid token from
# an approved, active account. Cheaper to read - and impossible to forget on a
# new endpoint - than repeating Depends() on each function.
router = APIRouter(dependencies=[Depends(get_current_active_user)])


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
