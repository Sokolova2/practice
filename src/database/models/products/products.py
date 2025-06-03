from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.models.orders.orders import OrdersModel

class ProductsModel(Base):
    __tablename__ = "products"

    id_product: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    create_data: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    orders: Mapped[list["OrdersModel"]] =relationship("OrdersModel", back_populates="product")