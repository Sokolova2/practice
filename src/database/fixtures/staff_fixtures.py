from src.database.models.staff.staff import StaffModels
from src.database.database import new_async_session
from sqlalchemy import select

async def create_user():
    async with new_async_session() as session:
        result = await session.execute(select(StaffModels))
        product = result.scalars().first()

        if not product:
            users = [
                StaffModels(last_name="Петров", fist_name="Петро", login="petrov_petro", password="12345678", role="Бухглатер"),
                StaffModels(last_name="Іваненко", fist_name="Іван", login="ivanenko_ivan", password="12345678", role="Продавец-консультант"),
                StaffModels(last_name="Коваленко", fist_name="Марина", login="kovalenko_marina", password="12345678", role="Касир"),
            ]
            session.add_all(users)
            await session.commit()