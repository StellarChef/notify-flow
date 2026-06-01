from routers import orders
from fastapi import FastAPI

app = FastAPI()

app.include_router(orders.router)
