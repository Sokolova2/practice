from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING
from src.database.models.products.products import ProductsModel

if TYPE_CHECKING:
    from src.database.models.products.products import ProductsModel

class DiscountService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def discount(self, id_product: int) -> float:
        stmt = select(ProductsModel).where(ProductsModel.id_product == id_product)
        result = await self.db.execute(stmt)
        product = result.scalars().first()

        if product.create_data < datetime.now() -timedelta(days=30):
            discount = product.price * 0.2
            res = product.price - discount
            return res
        else:
            return product.price