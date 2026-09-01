from pydantic import BaseModel, AwareDatetime, EmailStr
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
    # Internal model - carries the password hash, so it must never be used as a
    # response_model. Use UserOut for anything that leaves the API.
    id: int
    role: UserRole
    login: str
    email: EmailStr
    password: str
    is_active: bool


class UserCreate(BaseModel):
    # Registration input: the plaintext password stops here, at the API edge.
    login: str
    email: EmailStr  # EmailStr rejects malformed addresses before they hit the DB
    password: str


class UserLogin(BaseModel):
    # Sign-in input. Separate from UserCreate on purpose: registration may grow
    # fields (email confirmation, terms) that must never be required to log in.
    login: str
    password: str


class UserOut(BaseModel):
    # Registration output - no password, no hash.
    model_config = {"from_attributes": True}
    id: int
    login: str
    email: EmailStr
    role: UserRole
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str
