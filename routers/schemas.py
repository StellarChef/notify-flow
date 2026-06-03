"""
Modele Pydantic = dane "W RUCHU".
OrderJSON odwzorowuje surowy JSON, który przysyła sklep (patrz mok_order.json).
Pydantic na podstawie tych klas WALIDUJE wejście: sprawdza typy, parsuje daty,
zamienia stringi statusu na Twój Enum. Jak coś się nie zgadza -> czytelny błąd 422.
"""

from datetime import datetime, date
from pydantic import BaseModel

from enums import OrderStatus


class Customer(BaseModel):
    name: str
    email: str
    phone: str
    ip: str
    accepted_terms: bool


class Address(BaseModel):
    name: str
    street: str
    postal_code: str
    city: str
    country: str


class Payment(BaseModel):
    status: str
    method: str


class Delivery(BaseModel):
    method: str
    inpost_point_id: str
    inpost_point_address: str


class Personalization(BaseModel):
    kolor: str
    rozmiar_bazowy: str
    wzrost_cm: int
    dlugosc_rekawa_cm: int
    dlugosc_produktu_cm: int
    obwod_biust_cm: int
    obwod_biodra_cm: int
    obwod_talia_cm: int
    szerokosc_plecow_cm: int


class Product(BaseModel):
    id: int
    name: str
    product_code: str
    price_gross: float
    discount_percent: float
    discount_code: str
    price_after_discount: float
    size: str
    quantity: int
    personalization: Personalization


class Summary(BaseModel):
    shipping_cost: float
    discount_total: float
    coupon_code: str
    coupon_value_percent: float
    total_gross: float


class Notes(BaseModel):
    customer: str
    admin_private: str
    admin_public: str


class OrderJSON(BaseModel):
    order_id: str
    order_number: str
    status: OrderStatus
    status_label: str
    created_at: datetime
    delivery_date_estimated: date
    delivery_days: int
    customer: Customer
    billing_address: Address
    shipping_address: Address
    payment: Payment
    delivery: Delivery
    products: list[Product]
    summary: Summary
    notes: Notes
    delivery_date_label: str
