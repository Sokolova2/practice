import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app 
from src.database.database import engine_test, Base, async_session_test, get_session_test 
import os
from dotenv import load_dotenv
from datetime import datetime
import jwt
import asyncio
import sys

if sys.platform.startswith("win"):
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
    

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

def create_jwt_token(sub: str, login: str, role: str, token_type: str = "access"):
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "login": login,
        "role": role,
        "iat": int(now.timestamp()),
        "type": token_type
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@pytest.fixture(scope="session", autouse=True)
def set_pytest_asyncio_session_scope():
    pytest_asyncio.current_loop_scope = "session"

@pytest_asyncio.fixture(scope="session")
async def setup_database():
    print("\nSetting up database...")
    async with engine_test.begin() as conn: 
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 
    print("Database setup complete.")
    yield 
    print("Cleaning up database...")
    print("Database cleanup complete.")

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with async_session_test() as session:
            yield session 
            
@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_session():
        yield db_session
        
    app.dependency_overrides[get_session_test] = override_get_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test" 
    ) as ac:
        yield ac
        
    app.dependency_overrides.clear()

@pytest.fixture
def cashier_token():
    return create_jwt_token("1", "cashier", "Касир")

@pytest.fixture
def accountant_token():
    return create_jwt_token("2", "accountant", "Бухгалтер")

@pytest.fixture
def sales_consultant_token():
    return create_jwt_token("3", "sales_consultant", "Продавець-консультант")