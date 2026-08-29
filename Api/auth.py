from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import session
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = ["HS256"]
