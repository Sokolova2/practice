from src.database.models.products.products import ProductsModel
from src.database.database import new_async_session
from sqlalchemy import select

async def create_product():
    async with new_async_session() as session:
        result = await session.execute(select(ProductsModel))
        product = result.scalars().first()

        if not product:
            products = [
                ProductsModel(name="Laptop", price=21000.0),
                ProductsModel(name="Phone Samsung", price=11000.0),
                ProductsModel(name="Mouse", price=500.0),
            ]
            session.add_all(products)
            await session.commit()