from pydantic import BaseModel

from enums import OrderStatus, FulfillmentPath


class Customer(BaseModel):
    name: str
    surname: str
    address: str


class Product(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float
    attributes: dict


class Order(BaseModel):
    id: str
    customer: Customer
    products: list[Product]
    status: OrderStatus
    fulfillment_path: FulfillmentPath
