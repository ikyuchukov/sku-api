import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'sku-user')}"
    f":{os.getenv('DB_PASSWORD')}"
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
