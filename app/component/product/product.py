from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric, Index
from app.component.database.database import Base
from app.component.category.category import Category


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("index_products_title_fulltext", "title", mysql_prefix="FULLTEXT"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(3000), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=14, scale=6), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    category: Mapped[Category] = relationship("Category")