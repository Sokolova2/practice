from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session
from src.api.cashier.cashier_service import CashierService
from src.database.schemas.orders.orders import OrdersAddSchemas, OrdersUpdateSchemas, OrderCreateResponse

"""Контроллер для виклику методів із сервіса CashierService"""

cashier_routes = APIRouter(
    prefix="/cashier"
)

@cashier_routes.get("/product", summary="Get product")
async def get_product(db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.get_product()

@cashier_routes.post("/create/order", summary="Create order")
async def add_product(order: OrdersAddSchemas, db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.add_order(order) 

@cashier_routes.get("/order", summary="Get last order")
async def get_order(db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.get_order()

@cashier_routes.get("/check/{id_order}", summary="Get check")
async def check(id_order: int, db: AsyncSession = Depends(get_session)):
    service = CashierService(db)
    return await service.check(id_order)

@cashier_routes.patch("/order/{status}", summary="Change status to payed")
async def change_status(
    id_order: int,
    new_order: OrdersUpdateSchemas,
    db: AsyncSession = Depends(get_session)
):
    service = CashierService(db)
    return await service.change_status(id_order, new_order)

