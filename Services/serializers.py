from models.schemas import *
import json


class Serializer:
    @staticmethod
    def serialize(order: Order):
        return json.model_dump(order)

    @staticmethod
    def deserialize(response: dict):
        order = Order(**response)
        return order
        


