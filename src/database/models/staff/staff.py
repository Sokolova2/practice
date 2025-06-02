from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from database import database
from sqlalchemy import String

class StaffModels(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(70), nullable=False)
    first_name: Mapped[str] = mapped_column(String(70), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
