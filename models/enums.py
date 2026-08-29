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


class ProductType(Enum):
    # Decided PER ORDER LINE, not in the catalog - the same SKU may one day sell
    # both ways. Derived in the adapter only, from the size attribute key.
    STANDARD = "standard"  # off-the-shelf size, "Rozmiar: M"
    MADE_TO_ORDER = "made_to_order"  # sewn to measure, "Rozmiar startowy" + measurements


class FulfillmentPath(Enum):
    # HOW the line gets fulfilled - mutable STATE, unlike ProductType.
    # MADE_TO_ORDER is always PRODUCTION. STANDARD starts in WAREHOUSE and drops
    # to PRODUCTION when stock runs out. Never the other way round.
    PRODUCTION = "production"
    WAREHOUSE = "warehouse"


class MaterialUsageKind(Enum):
    # Filled in by the cutter after the job - the norm is only a hint, since
    # faulty material changes how many metres actually go into the garment.
    USED = "used"  # went into the product
    WASTE = "waste"  # faulty pattern/material - left stock, never reached the product
    RETURN = "return"  # correction or cancellation - goes back on stock


class UserRole(Enum):
    # Not a secret, but an authorization decision: always read it from the DB or
    # a signed token, never from anything the client sends.
    USER = "user"  # reads orders, reports material usage
    ADMIN = "admin"  # runs orders and production, manages accounts and devices


class DeliveryMethod(Enum):
    PICKUP_POINT = "pickup_point"
    HOME_DELIVERY = "home_delivery"
