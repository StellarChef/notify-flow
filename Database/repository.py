from sqlalchemy import select, exists
from sqlalchemy.orm import sessionmaker, selectinload

from Database.config_db import db
from models.schemas import Order
from models.enums import CLOSED
from Database.db_schemas import (
    CustomerTable,
    ProductTable,
    DeliveryProviderTable,
    OrderTable,
    Base,
)
from sqlalchemy.dialects.postgresql import insert

Session = sessionmaker(bind=db)

CLOSED_STATUSES = [status.value for status in CLOSED]


class Repository:

    @staticmethod
    def save_order(pydantic_order: Order) -> int:
        with Session() as session:
            customer = session.scalar(
                select(CustomerTable).where(
                    CustomerTable.user_id == pydantic_order.customer.user_id
                )
            )
            if customer is None:
                customer = CustomerTable(
                    user_id=pydantic_order.customer.user_id,
                    name=pydantic_order.customer.name,
                    lastname=pydantic_order.customer.lastname,
                    email=pydantic_order.customer.email,
                    phone=pydantic_order.customer.phone,
                )

            provider = session.merge(
                DeliveryProviderTable(
                    id=pydantic_order.delivery_method.provider.id,
                    provider=pydantic_order.delivery_method.provider.name,
                )
            )

            order = session.scalar(
                select(OrderTable).where(OrderTable.order_id == pydantic_order.id)
            )
            if order is None:
                order = OrderTable(order_id=pydantic_order.id)
                session.add(order)

            order.status = pydantic_order.status.value
            order.fulfillment_path = pydantic_order.fulfillment_path.value
            order.ordered_at = pydantic_order.fulfillment_date.ordered_at
            order.ship_by = pydantic_order.fulfillment_date.ship_by
            order.delivery_method = pydantic_order.delivery_method.method.value
            order.delivery_address = pydantic_order.delivery_method.address
            order.delivery_point = pydantic_order.delivery_method.point
            order.customer = customer
            order.delivery_provider = provider
            order.products = [
                ProductTable(
                    name=p.name,
                    sku=p.sku,
                    quantity=p.quantity,
                    price=p.price,
                    attributes=p.attributes,
                    product_type=p.product_type.value,
                )
                for p in pydantic_order.products
            ]

            session.commit()
            return order.id

    @staticmethod
    def fetch_open_orders() -> list[OrderTable]:
        with Session() as session:
            statement = (
                select(OrderTable)
                .where(OrderTable.status.not_in(CLOSED_STATUSES))
                .options(
                    selectinload(OrderTable.customer),
                    selectinload(OrderTable.products),
                    selectinload(OrderTable.delivery_provider),
                )
            )
            return list(session.scalars(statement).all())

    @staticmethod
    def fetch_all_orders() -> list:
        with Session() as session:
            statement = select(OrderTable).options(
                selectinload(OrderTable.customer),
                selectinload(OrderTable.products),
                selectinload(OrderTable.delivery_provider),
            )
            return list(session.scalars(statement).all())

    @staticmethod
    def delete_order(id: int):
        with Session() as session:
            order = session.scalar(select(OrderTable).where(OrderTable.order_id == id))
            if bool is None:
                return False
            session.delete(order)
            session.commit()
            return True

    @staticmethod
    def _look_at_record(table: Base, search, col):
        with Session() as s:
            query = select(table).where(col.like(f"%{search}%")).limit(3)
            return s.scalars(query).all()

    # DEBUG: pretty-print a list of orders as a table
    @staticmethod
    def show(orders: list[OrderTable]):
        header = (
            f"{'order_id':<8} | {'status':>6} | {'customer':<22} | "
            f"{'prod':>4} | {'delivery':<13} | point / address"
        )
        print(header)
        print("-" * len(header))
        for o in orders:
            customer = f"{o.customer.name} {o.customer.lastname}"
            dest = o.delivery_point or o.delivery_address or "-"
            print(
                f"{o.order_id:<8} | {o.status:>6} | {customer:<22} | "
                f"{len(o.products):>4} | {o.delivery_method:<13} | {dest}"
            )
        print(f"\n({len(orders)} orders total)")
