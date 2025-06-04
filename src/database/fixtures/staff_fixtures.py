from src.database.models.staff.staff import StaffModels
from src.database.database import new_async_session
from sqlalchemy import select

async def create_user():
    """Фікстури для заповння даними користувачів бд"""
    
    async with new_async_session() as session:
        result = await session.execute(select(StaffModels))
        product = result.scalars().first()

        if not product:
            users = [
                StaffModels(last_name="Петров", first_name="Петро", login="petrov_petro", password="$2b$12$VEtNgWWL4KeT1g6vxe1ruucOgvt5uryGXAc8jXV8wWCcHx.aRXuE2", role="Бухгалтер"),
                StaffModels(last_name="Іваненко", first_name="Іван", login="ivanenko_ivan", password="$2b$12$VEtNgWWL4KeT1g6vxe1ruucOgvt5uryGXAc8jXV8wWCcHx.aRXuE2", role="Продавець-консультант"),
                StaffModels(last_name="Коваленко", first_name="Марина", login="kovalenko_marina", password="$2b$12$VEtNgWWL4KeT1g6vxe1ruucOgvt5uryGXAc8jXV8wWCcHx.aRXuE2", role="Касир"),
            ]
            session.add_all(users)
            await session.commit()