from config_db import db
from routers.schemas import Order
from sqlalchemy.orm import sessionmaker
from Database.db_schemas import *

Session = sessionmaker(bind=db)


class Repository:

    def save_order(pydantic_order: Order):
        with Session as session:
            customer = CustomerTable(
                name=pydantic_order.customer.name,
                lastname=pydantic_order.customer.surname,
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

            order = OrderTable(
                status=pydantic_order.status.value,
                fulfillment_path=...,
                customer=customer,
                products=products,
            )

        session.add(order)
        session.commit()

    def fetch_order():
        
