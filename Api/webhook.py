import logging

from fastapi import APIRouter, Header, HTTPException

from Database.repository import Repository
from Services.adapter import ShoperAdapter
import os
from dotenv import load_dotenv
from secrets import compare_digest

load_dotenv()

# Named after the module, so records read "Api.webhook | ..." and point straight
# at their source. Same pattern in every module.
logger = logging.getLogger(__name__)

router = APIRouter()


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


@router.post("/webhooks/shoper/orders")
def receive_order_webhook(order: dict, x_webhook_secret: str = Header(...)):
    if not compare_digest(x_webhook_secret, WEBHOOK_SECRET):
        # WARNING, not ERROR: a rejected call is the guard doing its job, not a
        # fault. Still worth recording - a burst of these means someone probing.
        # Never log the secret that was sent, not even the wrong one.
        logger.warning("Webhook rejected: invalid secret")
        raise HTTPException(status_code=401, detail="Invalid webhook secret")
    saved = Repository.upsert_order(ShoperAdapter.parse(order))

    # Log the order id, not the payload: it carries the customer's name, address
    # and phone, and log files are not the place for personal data.
    logger.info("Webhook accepted, order %s stored (row id %s)", order.get("order_id"), saved)
    return {"status": "delivered"}
