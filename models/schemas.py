from pydantic import BaseModel, AwareDatetime
from datetime import date
from decimal import Decimal
from models.enums import (
    OrderStatus,
    FulfillmentPath,
    DeliveryMethod,
    ProductType,
    UserRole,
)


class Customer(BaseModel):
    model_config = {"from_attributes": True}
    user_id: int
    name: str
    lastname: str
    email: str
    phone: str


class Product(BaseModel):
    model_config = {"from_attributes": True}
    name: str
    sku: str
    quantity: int
    price: Decimal
    # decided per order line by the adapter, from the size attribute key
    product_type: ProductType
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
    ordered_at: AwareDatetime
    ship_by: AwareDatetime


class Order(BaseModel):
    id: str
    customer: Customer
    products: list[Product]
    status: OrderStatus
    fulfillment_path: FulfillmentPath
    fulfillment_date: FulfillmentDate
    delivery_method: Delivery


class User(BaseModel):
    id: int
    role: UserRole
    login: str
    password: str
