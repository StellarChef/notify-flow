from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import session
from dotenv import load_dotenv
import os

from fastapi import APIRouter, HTTPException, status

from models.schemas import UserCreate, UserOut
from Services.auth_service import Auth

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate):
    # Thin on purpose: HTTP in, HTTP out. Hashing and the default role are
    # decided in Auth.register, so this stays the only layer that knows codes.
    try:
        return Auth.register(data)
    except ValueError as e:
        # 409 - the request was well formed, it just clashes with existing state
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
