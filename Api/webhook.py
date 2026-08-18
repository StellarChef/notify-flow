from fastapi import APIRouter, Header, HTTPException

from Database.repository import Repository
from Services.adapter import ShoperAdapter
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


@app.post("/webhooks/shoper/orders")
def receive_order_webhook(order: dict, x_webhook_secret: str = Header(...)):
    if x_webhook_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")
    Repository.save_order(ShoperAdapter.parse(order))

    print("Webhook received")
    return {"status": "delivered"}
