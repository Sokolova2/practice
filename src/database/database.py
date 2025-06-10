import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME_APP = os.getenv("DB_NAME_APP")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")

engine_app = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_APP}', echo=True)
engine_test = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}', echo=True)

async_session_app = async_sessionmaker(bind=engine_app, expire_on_commit=False)
async_session_test = async_sessionmaker(bind=engine_test, expire_on_commit=False)


async def get_session_app():
    async with async_session_app() as session:
        yield session
        
async def get_session_test():
    async with async_session_test() as session:
        yield session

class Base(DeclarativeBase):
    pass