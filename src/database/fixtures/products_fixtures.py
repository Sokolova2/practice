from src.database.models.products.products import ProductsModel
from src.database.database import async_session_app
from sqlalchemy import select
from datetime import datetime

async def create_product():
    """Фікстури для заповння даними товарів бд"""

    async with async_session_app() as session:
        result = await session.execute(select(ProductsModel))
        product = result.scalars().first()

        if not product:
            products = [
                ProductsModel(name="Ноутбук Lenovo", price=21000.0, create_data=datetime(2025, 4, 25)),
                ProductsModel(name="Телефон Samsung", price=11000.0, create_data=datetime(2025, 5, 5)),
                ProductsModel(name="Миша Logitech", price=500.0, create_data=datetime(2025, 4, 1)),
                ProductsModel(name="Комп`ютер Intell", price=33000.0, create_data=datetime(2025, 5, 25)),
                ProductsModel(name="Клавіатура Hator", price=500.0, create_data=datetime(2025, 4, 29)),
                ProductsModel(name="Телефон Iphone 13", price=25000.0, create_data=datetime(2025, 5, 27)),
                ProductsModel(name="Подовжувач Gelius", price=1000.0, create_data=datetime(2025, 4, 19)),
                ProductsModel(name="Подовжувач Gelius", price=1000.0, create_data=datetime(2025, 4, 19)),
            ]
            session.add_all(products)
            await session.commit()