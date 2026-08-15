from pydantic import BaseModel
from datetime import date
from routers.enums import OrderStatus, FulfillmentPath, DeliveryMethod


class Customer(BaseModel):
    name: str
    lastname: str
    email: str
    phone: str


class Product(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float
    attributes: dict


class DeliveryProvider(BaseModel):
    id: int
    name: str


class Delivery(BaseModel):
    method: DeliveryMethod
    address: str | None = None
    point: str | None = None
    provider: DeliveryProvider


class FulfillmentDate(BaseModel):
    ordered_at: date
    ship_by: date


class Order(BaseModel):
    id: str
    customer: Customer
    products: list[Product]
    status: OrderStatus
    fulfillment_path: FulfillmentPath
    fulfillment_date: FulfillmentDate
    delivery_method: Delivery
