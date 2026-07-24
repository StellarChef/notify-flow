from datetime import date

from sqlalchemy import ForeignKey
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


class DeliveryProviderTable(Base):
    __tablename__ = "delivery_providers"
    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str]


class StatusTable(Base):
    __tablename__ = "statuses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class OrderTable(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    fulfillment_path: Mapped[str]
    fulfillment_date: Mapped[date]
    delivery_method: Mapped[str]  # enum stored as a column
    delivery_address: Mapped[str | None]
    delivery_point: Mapped[str | None]

    # foreign keys - the actual columns in the table
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    delivery_provider_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_providers.id")
    )

    # relationships - Python-side navigation, not columns
    customer: Mapped["CustomerTable"] = relationship()
    status: Mapped["StatusTable"] = relationship()
    delivery_provider: Mapped["DeliveryProviderTable"] = relationship()
    products: Mapped[list["ProductTable"]] = relationship()
