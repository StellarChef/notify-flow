import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
url = os.getenv("DB_URL")

# One engine for the whole process. It owns the connection pool, so creating a
# second one would open a second pool against the same database.
db = sa.create_engine(url, client_encoding="utf8")

# One session factory, built here rather than in every repository. Each call to
# Session() still hands out a fresh, independent session - what is shared is the
# configuration and the pool underneath, not the session itself.
Session = sessionmaker(bind=db)
