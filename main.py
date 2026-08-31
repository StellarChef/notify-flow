from fastapi import FastAPI
from Database.repository import Base
from Database.config_db import db
from Api.api_connection import router as api_router
from Api.webhook import router as webhook_router
from Api.auth import router as auth_router
from Database.repository import Repository

app = FastAPI()

app.include_router(api_router)
app.include_router(webhook_router)
app.include_router(auth_router)

engine = db
Base.metadata.create_all(engine)