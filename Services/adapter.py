import json
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from models.schemas import (
    Order,
    Customer,
    Product,
    Delivery,
    DeliveryProvider,
    FulfillmentDate,
)
from models.enums import DeliveryMethod, FulfillmentPath, OrderStatus

# Shop-specific lookup tables live outside the repo (see .gitignore).
CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_config(filename: str) -> dict:
    with open(CONFIG_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


class Adapter(ABC):

    @abstractmethod
    def parse(self, raw: dict) -> Order:
        pass


class ShoperAdapter(Adapter):
    # --- SHOPER-SPECIFIC KNOWLEDGE (must never leak into the domain) ---

    # shipping_id -> human name. Loaded from config, source: shipping.json
    SHIPPING_NAMES = _load_config("shipping_names.json")

    # shipping_id -> domain OrderStatus. JSON holds enum NAMES, unpacked here.
    ORDER_STATUSES = {
        status_id: OrderStatus[name]
        for status_id, name in _load_config("order_statuses.json").items()
    }

    # shipping_id values that mean "collect at a point" (rest = delivery to address)
    PICKUP_POINT_SHIPPING = {"1", "7", "8"}

    # lead time threshold: up to 2 business days = ready stock, above = sewn to order
    WAREHOUSE_MAX_DAYS = 2

    # Timezone
    SHOP_TZ = ZoneInfo("Europe/Warsaw")

    @staticmethod
    def _parse_options(option: str) -> dict:
        # Shoper packs personalization into ONE string: "Key: Value; Key: Value"
        attributes = {}
        for part in option.split(";"):
            if ":" not in part:
                continue
            key, value = part.split(
                ":", 1
            )  # split on FIRST colon - keys may end with "?"
            attributes[key.strip()] = value.strip()
        return attributes

    @staticmethod
    def _parse_product(raw: dict) -> list[Product]:
        return [
            Product(
                name=product["name"],
                sku=product["code"],
                quantity=int(product["quantity"]),
                price=Decimal(product["price"]),
                attributes=ShoperAdapter._parse_options(product.get("option", "")),
            )
            for product in raw["products"]
        ]

    @staticmethod
    def _parse_customer(raw: dict) -> Customer:
        # phone lives in the address block, not at order level
        billing = raw["billing_address"]
        return Customer(
            user_id=int(raw["user_id"]),
            name=billing["firstname"],
            lastname=billing["lastname"],
            email=raw["email"],
            phone=billing["phone"],
        )

    @staticmethod
    def _parse_delivery(raw: dict) -> Delivery:
        # the enum comes OUT of this if - single place deciding the delivery method
        if raw["shipping_id"] in ShoperAdapter.PICKUP_POINT_SHIPPING:
            method = DeliveryMethod.PICKUP_POINT
            point = raw.get("pickup_point")  # .get - courier orders have no such key
            address = None
        else:
            method = DeliveryMethod.HOME_DELIVERY
            point = None
            addr = raw["delivery_address"]
            address = f"{addr['street1']}, {addr['postcode']} {addr['city']}, {addr['country']}"

        # provider is built AFTER the if - needed by both branches.
        # The order carries only shipping_id; names come from the config lookup.
        provider = DeliveryProvider(
            id=int(raw["shipping_id"]),
            name=ShoperAdapter.SHIPPING_NAMES.get(raw["shipping_id"], "Undefined"),
        )

        return Delivery(method=method, address=address, point=point, provider=provider)

    @staticmethod
    def _business_days_between(start: date, end: date) -> int:
        # weekends excluded - Shoper counts its lead time in business days
        days = 0
        current = start
        while current < end:
            current += timedelta(days=1)
            if current.weekday() < 5:
                days += 1
        return days

    @staticmethod
    def _parse_fulfillment_date(raw: dict) -> FulfillmentDate:
        # both dates come straight from raw - Shoper already computed ship_by
        return FulfillmentDate(
            ordered_at=datetime.strptime(raw["date"], "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=ShoperAdapter.SHOP_TZ
            ),
            ship_by=datetime.strptime(raw["delivery_date"], "%Y-%m-%d").replace(
                tzinfo=ShoperAdapter.SHOP_TZ
            ),
        )

    @staticmethod
    def _parse_fulfillment_path(raw: dict) -> FulfillmentPath:
        # lead time = business days between order date and ship-by date
        # short (2d) = ready stock; long (14d) = sewn to order
        dates = ShoperAdapter._parse_fulfillment_date(raw)
        lead_days = ShoperAdapter._business_days_between(
            dates.ordered_at, dates.ship_by
        )

        if lead_days <= ShoperAdapter.WAREHOUSE_MAX_DAYS:
            return FulfillmentPath.WAREHOUSE
        return FulfillmentPath.PRODUCTION

    @staticmethod
    def _parse_status(raw: dict) -> OrderStatus:
        # Shoper status_id -> domain enum
        return ShoperAdapter.ORDER_STATUSES[raw["status_id"]]

    @staticmethod
    def parse(raw: dict) -> Order:
        # public entry point - every piece comes from a private parser
        customer = ShoperAdapter._parse_customer(raw)
        products = ShoperAdapter._parse_product(raw)
        status = ShoperAdapter._parse_status(raw)
        fulfillment_path = ShoperAdapter._parse_fulfillment_path(raw)
        fulfillment_date = ShoperAdapter._parse_fulfillment_date(raw)
        delivery = ShoperAdapter._parse_delivery(raw)

        return Order(
            id=raw["order_id"],
            customer=customer,
            products=products,
            status=status,
            fulfillment_path=fulfillment_path,
            fulfillment_date=fulfillment_date,
            delivery_method=delivery,
        )
