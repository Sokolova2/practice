from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.schemas.orders.orders import OrdersAddSchemas, OrdersUpdateSchemas
from src.database.models.orders.orders import OrdersModel
from src.database.models.products.products import ProductsModel
from src.api.cashier.discount import DiscountService
from sqlalchemy.orm import selectinload
from datetime import datetime 

class CashierService:
    """Клас для функцій, які виконує касир"""

    def __init__(self, db:AsyncSession):
        self.db = db
        self.discount_service = DiscountService(db)

    async def get_product(self):
        """Метод для отримання усіх товарів"""

        result = await self.db.execute(select(ProductsModel))
        get_product = result.scalars().all()

        if get_product == None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return get_product
    
    async def add_order(self, order: OrdersAddSchemas):
        """
            Метод для додавання замовлення
            Для цього треба ввести id товара, який замовили

        """
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

        return {
        "message": "Order successfully created",
        "order": add_order
    } 
    
    async def check(self, id_order: int):
        """Метод для формування чека для замовлення. Треба ввести id замовлення"""
        
        stmt = select(OrdersModel).options(selectinload(OrdersModel.product)).where(OrdersModel.id_order == id_order)
        result = await self.db.execute(stmt)
        check = result.scalars().first()

        if check == None:
            raise HTTPException(status_code=404, detail="Data not found")
        
        if check.status == "Виконано":
            check_response = {
            "id_order": check.id_order,
            "name_product": check.product.name,
            "price": check.price,
            "discount": check.discount,
            "create_data": datetime.now(),
            "create_data_order": check.create_data 
            }
            return check_response
        
        return {"message": "Order not processed or already paid"}

    async def change_status(self, id_order: int, new_order: OrdersUpdateSchemas):
        """
            Метод для зміни статуса замовлення.
            Для цього потрібно ввести id_order та змінити статус на "Сплачено"
        """
        stmt = select(OrdersModel).where(OrdersModel.id_order == id_order)
        result = await self.db.execute(stmt)
        order = result.scalars().first()

        if order == None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.status == "Виконано":
            order.status = new_order.status
            await self.db.commit()
            await self.db.refresh(order)

            return{
                "message": "Changing status of order successfully",
                "New order": order
            } 
        
        return {"message": "Order not processed or already paid"}
    
    async def get_order(self):
        """Метод для отримання останнього замовлення"""

        result = await self.db.execute(
            select(OrdersModel).order_by(desc(OrdersModel.id_order)).limit(1))
        orders = result.scalars().first()

        if orders == None:
            raise HTTPException(status_code=404, detail="Not fountd order")
        
        if orders.status == "Виконано":
            return orders
        
        return {"message": "Order not processed or already paid"}
