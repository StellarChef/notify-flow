from fastapi import APIRouter
from Database.repository import Repository
from routers.schemas import Order
from routers.orders import fetch_full_order

# from schemas import OrderJSON,enums
from dotenv import load_dotenv
import os
import json

load_dotenv()
app = APIRouter()

api_token = os.getenv("SHOPER_API_KEY")
client_id = os.getenv("SHOPER_CLIENT_ID")
shop_address_url = os.getenv("SHOP_ADDRESS")


@app.get("/sync", response_model=list[Order])
def get_orders_new():
    pass


@app.get("/orders", response_model=list[Order])
def get_orders():
    pass


@app.post("/")
def Toapp(orders):
    return
