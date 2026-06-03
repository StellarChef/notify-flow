from pydantic import BaseModel
from datetime import datetime
from routers.schemas import Personalization


class WorkModel(BaseModel):
    order_id: int
    production_id: int
    inpost_point_address: str
    product: str
    status: str
    shipping_date: datetime
    size: str
    personalization: Personalization | None = None
