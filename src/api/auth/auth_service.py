import os
from fastapi import HTTPException, Response
from dotenv import load_dotenv
from authx import AuthX, AuthXConfig
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.staff.staff import StaffModels
from src.database.schemas.staff.staff import StaffAddSchemas, StaffLoginSchemas, StaffGetSchemas
from datetime import datetime
import jwt
from typing import List

load_dotenv()

config = AuthXConfig(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET"),
    JWT_ACCESS_COOKIE_NAME=os.getenv("JWT_ACCESS_COOKIE_NAME"),
    JWT_TOKEN_LOCATION=["cookies"]
)

"""Хешування паролю для безпеки"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

authx = AuthX(config=config)

class AuthService:
    """
    Клас для додавання користувача до системи та авторизації, 
    щоб обмежити доступ для певних функцій, для певної ролі

    """

    def __init__(self, db:AsyncSession):
        self.db = db

    async def add_user(self, users: StaffAddSchemas):
        """
            Метод для додавання користувача, для цього потрібно:
            ввести прізвище, ім`я, логін, пароль та роль.
            Може бути три ролі:
                -Бухгалтер
                -Продавець-консультант
                -Касир
        """
        stmt = select(StaffModels).where(StaffModels.login == users.login)
        result = await self.db.execute(stmt)
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User with this login already exists ")
        
        add_user = StaffModels(
            last_name = users.last_name,
            first_name = users.first_name,
            login = users.login,
            password = hash_password(users.password),
            role = users.role
        )
        self.db.add(add_user)
        await self.db.commit()
        await self.db.refresh(add_user)

        return{
            "message": f"Successfully add user",
            "NewUser": add_user
        }
    
    def create_jwt_token(self, id_user: str, login: str, role: str, secret_key:str):
        """Метод для створення токену"""

        now = datetime.now()
        payload = {
            "sub": id_user,
            "login": login,
            "role": role,
            "iat": int(now.timestamp()),
            "type": "access"
        }
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    async def login(self, creds: StaffLoginSchemas, response: Response):
        """
            Метод для авторизації:
            - треба ввести логін та пароль
        """
        stmt = select(StaffModels).where(StaffModels.login == creds.login)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        if not pwd_context.verify(creds.password, user.password):
            raise HTTPException(status_code=403, detail="Invalid password")
        
        token = self.create_jwt_token(
            id_user = str(user.id),
            login = user.login,
            role = user.role,
            secret_key=os.getenv("JWT_SECRET")
        )

        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

        return{
            "message": f"Successfully login: {user.last_name + ' ' + user.first_name}",
            "access_token": token,
            "token-type": "bearer",
            "id_user": user.id,
            "login": user.login,
            "role": user.role
        }
    
    async def get_user(self) -> List[StaffGetSchemas]:
            """Метод для отримання усіх користувачів"""
            
            result = await self.db.execute(select(StaffModels))
            get_user = result.scalars().all()

            if not get_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return get_user