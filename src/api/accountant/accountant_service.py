from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database.models.orders.orders import OrdersModel
from datetime import datetime, timedelta

class AccoutantService:
    """Клас для функцій, які виконує бухгалтер"""

    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_orders(self, start_data: datetime, end_data: datetime):
        """
            Метод для отримання всіх замовлень за певний період
            Користувач вводить початкову дату та кінцеву дату періоду за який він хочу отримати замовлення.
            Формат дати yyyy-mm-dd
            
        """

        stmt = (
            select(OrdersModel)
            .options(selectinload(OrdersModel.product))
            .where(
                and_(
                    (OrdersModel.create_data >= start_data),
                    (OrdersModel.create_data <= (end_data + timedelta(days=1)))
                )
            )
        )

        result = await self.db.execute(stmt)
        orders = result.scalars().all()

        if orders == None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        response = []

        for order in orders:
            response.append({
                "id_order": order.id_order,
                "name_product": order.product.name,
                "status": order.status,
                "price": order.price,
                "discount": order.discount,
                "create_data": order.create_data,
                "update_data": order.update_data
            })

        return response