from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session
from src.api.sales_consultant.sales_consultant_service import SalesConsultantService

sales_consultant_routes = APIRouter(
    prefix="/consultant"
)

@sales_consultant_routes.get("/order", summary="Get last order")
async def get_order(db: AsyncSession = Depends(get_session)):
    service = SalesConsultantService(db)
    return await service.get_order()