from enum import IntEnum, Enum


class OrderStatus(IntEnum):
    COMPLEX = 1
    ACCEPTED = 2
    AWAITING_DELIVERY = 3
    IN_PROGRESS = 4
    AWAITING_PAYMENT = 5
    READY_TO_SHIP = 6
    SHIPPED = 7
    CANCELLED = 8
    REJECTED = 9
    RETURNED = 11


CLOSED = {
    OrderStatus.SHIPPED,
    OrderStatus.CANCELLED,
    OrderStatus.REJECTED,
    OrderStatus.RETURNED,
}


class FulfillmentPath(Enum):
    PRODUCTION = "production"
    WAREHOUSE = "warehouse"


class DeliveryMethod(Enum):
    PICKUP_POINT = "pickup_point"
    HOME_DELIVERY = "home_delivery"
