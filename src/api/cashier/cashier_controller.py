from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session
from src.api.cashier.cashier_service import CashierService
from src.database.schemas.orders.orders import OrdersAddSchemas

cashier_routes = APIRouter(
    prefix="/cashier"
)

@cashier_routes.get("/product", summary="Get product")
async def get_product(db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.get_product()

@cashier_routes.post("/create/order", response_model=OrdersAddSchemas, summary="Create order")
async def add_product(order: OrdersAddSchemas, db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.add_order(order) 