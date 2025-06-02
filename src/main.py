from fastapi import FastAPI, Depends
import uvicorn
from src.database.database import engine, Base
from src.database.fixtures.products_fixtures import create_product

app = FastAPI()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await init_models()
    await create_product()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)