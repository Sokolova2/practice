from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session_app
from src.api.sales_consultant.sales_consultant_service import SalesConsultantService
from src.database.schemas.orders.orders import OrdersUpdateSchemas

"""Контроллер для виклику методів із сервіса SalesConsultantService"""

sales_consultant_routes = APIRouter(
    prefix="/consultant"
)

@sales_consultant_routes.get("/order", summary="Get last order")
async def get_order(db: AsyncSession = Depends(get_session_app)):
    service = SalesConsultantService(db)
    return await service.get_order()

@sales_consultant_routes.patch("/order/{id_order}", summary="Change status")
async def change_status(
    id_order: int, 
    new_order: OrdersUpdateSchemas, 
    db:AsyncSession = Depends(get_session_app)
):
    service = SalesConsultantService(db)
    return await service.change_status(id_order, new_order)