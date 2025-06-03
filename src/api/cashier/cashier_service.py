from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.database.schemas.orders.orders import OrdersAddSchemas, OrdersGetSchemas
from src.database.models.orders.orders import OrdersModel
from src.database.models.products.products import ProductsModel
from src.api.cashier.discount import DiscountService

class CashierService:
    def __init__(self, db:AsyncSession):
        self.db = db
        self.discount_service = DiscountService(db)

    async def get_product(self):
        result = await self.db.execute(select(ProductsModel))
        get_product = result.scalars().all()

        if get_product == None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return get_product
    
    async def add_order(self, order: OrdersAddSchemas):
        stmt = select(ProductsModel).where(ProductsModel.id_product == order.id_product)
        result = await self.db.execute(stmt)
        get_product = result.scalars().first()

        if get_product == None:
            raise HTTPException(status_code=404, detail="User not found")
        
        discounted_price = await self.discount_service.discount(get_product.id_product)
        
        price = get_product.price

        add_order = OrdersModel(
            id_product = get_product.id_product,
            discount = discounted_price,
            price = price
        )

        self.db.add(add_order)
        await self.db.commit()
        await self.db.refresh(add_order)

        return add_order
    
