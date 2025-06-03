from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.products.products import ProductsModel

class OrdersModel(Base):
    __tablename__ = "orders"

    id_order: Mapped[int] = mapped_column(primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Прийнято")
    price: Mapped[float] = mapped_column(Float, nullable=False)
    discount: Mapped[float] = mapped_column(Float, default=0.0)
    create_data: Mapped[datetime] =  mapped_column(DateTime, default=datetime.now())
    update_data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    product: Mapped["ProductsModel"] = relationship("ProductsModel", back_populates="orders")