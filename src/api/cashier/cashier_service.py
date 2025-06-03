from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.database.schemas.orders.orders import OrdersAddSchemas
from src.database.models.orders.orders import OrdersModel
from src.database.schemas.products.products import ProductGetSchemas
from src.database.models.products.products import ProductsModel

class CashierService:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_product(self) -> List[ProductGetSchemas]:
        result = await self.db.execute(select(ProductsModel))
        get_product = result.scalars().all()
        return get_product
    
    async def add_order(self, order = OrdersAddSchemas):
        stmt = select(ProductsModel).where(ProductsModel.id_product == order.id_product)
        result = await self.db.execute(stmt)
        get_product = result.scalars().first()

        if get_product == None:
            raise HTTPException(status_code=404, detail="User not found")
        
        add_order = OrdersModel(
            id_product = get_product.id_product,
            discount = order.discount
        )

        self.db.add(add_order)
        await self.db.commit()
        await self.db.refresh(add_order)
        return add_order
    