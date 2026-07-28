from datetime import date, datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    sessionmaker,
    relationship,
)
from sqlalchemy.dialects.postgresql import JSONB

from config_db import db

Session = sessionmaker(bind=db)
Base = declarative_base()


class CustomerTable(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]


class ProductTable(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    sku: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    attributes: Mapped[dict] = mapped_column(JSONB)
    # every product line belongs to one order
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))


class DeliveryProviderTable(Base):
    __tablename__ = "delivery_providers"
    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str]


class OrderTable(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(unique=True, index=True)
    status: Mapped[str]
    fulfillment_path: Mapped[str]
    ordered_at: Mapped[date]
    ship_by: Mapped[date]
    delivery_method: Mapped[str]
    delivery_address: Mapped[str | None]
    delivery_point: Mapped[str | None]
    # when the order landed in our DB (set by the database on insert)
    received_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # foreign keys - the actual columns in the table
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    delivery_provider_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_providers.id")
    )

    # relationships - Python-side navigation, not columns
    customer: Mapped["CustomerTable"] = relationship()
    delivery_provider: Mapped["DeliveryProviderTable"] = relationship()
    products: Mapped[list["ProductTable"]] = relationship()
