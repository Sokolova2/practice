from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.orders.orders import OrdersModel
from src.database.schemas.orders.orders import OrdersUpdateSchemas

class SalesConsultantService:
    """Клас для функцій, які виконує продавець-консультант"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order(self):
        """Метод для отримання останнього замовлення"""

        result = await self.db.execute(
            select(OrdersModel).order_by(desc(OrdersModel.id_order)).limit(1))
        orders = result.scalars().first()
        
        if orders == None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if orders.status != "Сплачено" and orders.status != "Виконано":
            return orders
        
        return {"message": "Last order already processed or paid"}
    
    async def change_status(self, id_order: int, new_order: OrdersUpdateSchemas):
        """
            Метод для зміни статусу замовлення на 'Виконано'
            Треба ввести id замовлення та змінити статус
        """
        
        stmt = select(OrdersModel).where(OrdersModel.id_order == id_order)
        result = await self.db.execute(stmt)
        order = result.scalars().first()

        if order == None: 
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order.status != "Сплачено" and order.status != "Виконано": 
            order.status = new_order.status

            await self.db.commit()
            await self.db.refresh(order)

            return{
                "message": "Changing status of order successfully",
                "New order": order
            } 
        
        return {"message": "Last order already processed or paid"}