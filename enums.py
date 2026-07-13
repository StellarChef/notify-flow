from enum import Enum


class OrderStatus(Enum):
    COMPLEX = "złożone"
    ACCEPTED = "przyjete_do_realizacji"
    AWAITING_DELIVERY = "oczekiwanie_na_dostawe"
    IN_PROGRESS = "w_trakcie_kompletowania"
    AWAITING_PAYMENT = "oczekiwanie_na_platnosc"
    READY_TO_SHIP = "gotowe_do_wyslania"

    SHIPPED = "przesylka_wyslana"

    CANCELLED = "anulowane"
    REJECTED = "odrzucone"
    RETURNED = "zwrocone"
    COMPLAINED = "reklamowane"


CLOSED = {
    OrderStatus.SHIPPED,
    OrderStatus.CANCELLED,
    OrderStatus.REJECTED,
    OrderStatus.RETURNED,
    OrderStatus.COMPLAINED,
}


class FulfillmentPath(Enum):
    PRODUCTION = "production"
    WAREHOUSE = "warehouse"


class DeliveryMethod(Enum):
    PICKUP_POINT = "pickup_point"
    HOME_DELIVERY = "home_delivery"
