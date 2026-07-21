from config_db import db
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB

Session = sessionmaker(bind=db)
Base = declarative_base


class Customer(Base):
    id = Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name = Mapped[str]
    lastname = Mapped[str]
    email = Mapped[str]
    phone = Mapped[str]


class Product(Base):
    name = Mapped[str]
    sku = Mapped[str]
    quantity = Mapped[int]
    price = Mapped[float]
    attributes = Mapped[dict] = mapped_column(JSONB)
