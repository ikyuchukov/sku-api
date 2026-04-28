import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'sku-user')}"
    f":{quote_plus(os.getenv('DB_PASSWORD', ''))}"
    f"@{os.getenv('DB_HOST', 'sku-db')}"
    f":{os.getenv('DB_PORT', '3306')}"
    f"/{os.getenv('DB_NAME', 'sku')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
