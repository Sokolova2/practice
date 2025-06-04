from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session
from src.api.auth.auth_service import AuthService
from src.database.schemas.staff.staff import StaffAddSchemas, StaffLoginSchemas

"""Контроллер для виклику методів із сервіса AuthService"""

auth_routes = APIRouter(
    prefix="/auth"
)

@auth_routes.post("/new", summary="Add user")
async def add_user(user: StaffAddSchemas, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    return await service.add_user(users=user)

@auth_routes.post("/login", summary="Login user")
async def login(creds: StaffLoginSchemas, response: Response, db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    return await service.login(creds=creds, response=response)

@auth_routes.get("/staff", summary="Get staff")
async def get_user(db: AsyncSession = Depends(get_session)):
    service = AuthService(db)
    return await service.get_user()