from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload

from Database.config_db import db
from routers.schemas import Order
from routers.enums import CLOSED
from Database.db_schemas import (
    CustomerTable,
    ProductTable,
    DeliveryProviderTable,
    OrderTable,
    Base,
)
from Database.config_db import db as engine

Session = sessionmaker(bind=db)

CLOSED_STATUSES = [status.value for status in CLOSED]


class Repository:

    @staticmethod
    def save_order(pydantic_order: Order) -> int:
        with Session() as session:
            customer = CustomerTable(
                name=pydantic_order.customer.name,
                lastname=pydantic_order.customer.lastname,
                email=pydantic_order.customer.email,
                phone=pydantic_order.customer.phone,
            )

            products = [
                ProductTable(
                    name=p.name,
                    sku=p.sku,
                    quantity=p.quantity,
                    price=p.price,
                    attributes=p.attributes,
                )
                for p in pydantic_order.products
            ]

            provider = session.merge(
                DeliveryProviderTable(
                    id=pydantic_order.delivery_method.provider.id,
                    provider=pydantic_order.delivery_method.provider.name,
                )
            )

            order = OrderTable(
                order_id=pydantic_order.id,
                status=pydantic_order.status.value,
                fulfillment_path=pydantic_order.fulfillment_path.value,
                ordered_at=pydantic_order.fulfillment_date.ordered_at,
                ship_by=pydantic_order.fulfillment_date.ship_by,
                delivery_method=pydantic_order.delivery_method.method.value,
                delivery_address=pydantic_order.delivery_method.address,
                delivery_point=pydantic_order.delivery_method.point,
                customer=customer,
                products=products,
                delivery_provider=provider,
            )

            session.merge(order)
            session.commit()
            return order.id

    @staticmethod
    def fetch_orders() -> list[OrderTable]:
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
    def delete_order(table: Base, id: int):
        with Session() as session:
            record = session.get(table, id)
            if record is None:
                print("Record doesn't exists")
                return
            session.delete(record)
            session.commit()

    @staticmethod
    def _look_at_record(table: Base, search, col):
        with Session() as s:
            query = select(table).where(col.like(f"%{search}%")).limit(3)
            return s.scalars(query).all()

    def show():
        return
