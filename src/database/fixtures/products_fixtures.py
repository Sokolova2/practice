from src.database.models.products.products import ProductsModel
from src.database.database import new_async_session
from sqlalchemy import select

async def create_product():
    async with new_async_session() as session:
        result = await session.execute(select(ProductsModel))
        product = result.scalars().first()

        if not product:
            products = [
                ProductsModel(name="Ноутбук Lenovo", price=21000.0),
                ProductsModel(name="Телефон Samsung", price=11000.0),
                ProductsModel(name="Миша Logitech", price=500.0),
                ProductsModel(name="Комп`ютер Intell", price=33000.0),
                ProductsModel(name="Клавіатура Hator", price=500.0),
                ProductsModel(name="Телефон Iphone 13", price=25000.0),
                ProductsModel(name="Подовжувач Gelius", price=1000.0),
            ]
            session.add_all(products)
            await session.commit()