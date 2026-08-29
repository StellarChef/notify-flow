from sqlalchemy import delete, select
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
    def _upsert(session, table, values: dict, conflict_columns: list[str]) -> int:
        stmt = (
            insert(table)
            .values(**values)
            .on_conflict_do_update(index_elements=conflict_columns, set_=values)
            .returning(table.id)
        )
        return session.scalar(stmt)

    @staticmethod
    def upsert_order(pydantic_order: Order) -> int:
        with Session() as session:
            customer_id = Repository._upsert(
                session,
                CustomerTable,
                pydantic_order.customer.model_dump(),
                ["user_id"],
            )

            provider_id = Repository._upsert(
                session,
                DeliveryProviderTable,
                {
                    "id": pydantic_order.delivery_method.provider.id,
                    "provider": pydantic_order.delivery_method.provider.name,
                },
                ["id"],
            )

            order_pk = Repository._upsert(
                session,
                OrderTable,
                {
                    "order_id": pydantic_order.id,
                    "status": pydantic_order.status.value,
                    "fulfillment_path": pydantic_order.fulfillment_path.value,
                    "ordered_at": pydantic_order.fulfillment_date.ordered_at,
                    "ship_by": pydantic_order.fulfillment_date.ship_by,
                    "delivery_method": pydantic_order.delivery_method.method.value,
                    "delivery_address": pydantic_order.delivery_method.address,
                    "delivery_point": pydantic_order.delivery_method.point,
                    "customer_id": customer_id,
                    "delivery_provider_id": provider_id,
                },
                ["order_id"],
            )

            # Order lines have no natural key, so they are replaced wholesale.
            # This resets their ids on every sync - harmless while a line only
            # mirrors Shoper, but revisit once the warehouse writes to them.
            session.execute(
                delete(ProductTable).where(ProductTable.order_id == order_pk)
            )
            if pydantic_order.products:
                session.execute(
                    insert(ProductTable),
                    [
                        {
                            "order_id": order_pk,
                            "name": p.name,
                            "sku": p.sku,
                            "quantity": p.quantity,
                            "price": p.price,
                            "attributes": p.attributes,
                            "product_type": p.product_type.value,
                        }
                        for p in pydantic_order.products
                    ],
                )

            session.commit()
            return order_pk

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
    def fetch_order_by_id(order_id: str) -> OrderTable | None:
        with Session() as session:
            stmt = session.scalar(
                select(OrderTable)
                .where(OrderTable.order_id == order_id)
                .options(
                    selectinload(OrderTable.customer),
                    selectinload(OrderTable.products),
                    selectinload(OrderTable.delivery_provider),
                )
            )
            return stmt

    @staticmethod
    def delete_order(id: int):
        with Session() as session:
            order = session.scalar(select(OrderTable).where(OrderTable.order_id == id))
            if order is None:
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
