"""
Modele Pydantic = dane "W RUCHU".
OrderJSON odwzorowuje surowy JSON, który przysyła sklep (patrz mok_order.json).
Pydantic na podstawie tych klas WALIDUJE wejście: sprawdza typy, parsuje daty,
zamienia stringi statusu na Twój Enum. Jak coś się nie zgadza -> czytelny błąd 422.
"""

from datetime import datetime, date
from pydantic import BaseModel

from enums import OrderStatus


# --- KLOCKI (modele zagnieżdżone) ---
# Pydantic wymaga, by zagnieżdżony model był zdefiniowany ZANIM go użyjesz,
# dlatego najpierw "liście", a OrderJSON (korzeń) na samym końcu.

class Customer(BaseModel):
    name: str
    email: str          # można podmienić na EmailStr -> walidacja maila gratis (wymaga: pip install "pydantic[email]")
    phone: str
    ip: str
    accepted_terms: bool


class Address(BaseModel):
    # billing_address i shipping_address mają IDENTYCZNY kształt,
    # więc jeden model obsłuży oba. Nie powielaj kodu.
    name: str
    street: str
    postal_code: str
    city: str
    country: str


class Payment(BaseModel):
    status: str         # "oplacone" -> tu w przyszłości może wejść PaymentStatus(Enum)
    method: str


class Delivery(BaseModel):
    method: str
    inpost_point_id: str
    inpost_point_address: str


class Personalization(BaseModel):
    # Dane "na miarę" - to one realnie idą do szwalni.
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


# --- KORZEŃ: całe zamówienie ze sklepu ---

class OrderJSON(BaseModel):
    order_id: str                       # w JSON-ie "1053" jest stringiem, nie liczbą
    order_number: str
    status: OrderStatus                 # string -> Pydantic SAM zamieni na Twój Enum
    status_label: str
    created_at: datetime                # "2026-05-26T22:34:00" -> Pydantic SAM sparsuje na datetime
    delivery_date_estimated: date       # "2026-06-15" -> parsowane na date
    delivery_days: int
    customer: Customer
    billing_address: Address
    shipping_address: Address
    payment: Payment
    delivery: Delivery
    products: list[Product]             # lista! produktów może być wiele
    summary: Summary
    notes: Notes
    delivery_date_label: str
