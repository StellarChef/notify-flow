from models.schemas import (
    Order,
    Customer,
    Product,
    FulfillmentDate,
    Delivery,
    DeliveryProvider,
)
from Database.db_schemas import OrderTable
import json


class Serializer:
    @staticmethod
    def to_schema(row: OrderTable) -> Order:
        return Order(
            id=row.order_id,  # numer z Shopera, nie int PK
            status=row.status,
            fulfillment_path=row.fulfillment_path,
            customer=Customer.model_validate(row.customer),
            products=[Product.model_validate(p) for p in row.products],
            fulfillment_date=FulfillmentDate(  # dwie kolumny -> jeden obiekt
                ordered_at=row.ordered_at,
                ship_by=row.ship_by,
            ),
            delivery_method=Delivery(  # string + kolumny -> jeden obiekt
                method=row.delivery_method,
                address=row.delivery_address,
                point=row.delivery_point,
                provider=DeliveryProvider(
                    id=row.delivery_provider.id,
                    name=row.delivery_provider.provider,  # kolumna nazywa się `provider`
                ),
            ),
        )
