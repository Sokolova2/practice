from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session_app
from src.api.accountant.accountant_service import AccountantService
from datetime import datetime

"""Контроллер для виклику методів із сервіса AccoutantService"""

accountant_routes = APIRouter(
    prefix="/accountant"
)

@accountant_routes.get("/orders", summary="Get order")
async def get_order(
    start_data: datetime,
    end_data: datetime,
    db: AsyncSession = Depends(get_session_app)
):
    service = AccountantService(db)
    return await service.get_orders(start_data, end_data)