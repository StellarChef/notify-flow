import sqlalchemy as sa
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DB_URL")

db = sa.create_engine(url)
db.connect()
