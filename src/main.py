from fastapi import FastAPI, Depends
import uvicorn
from src.database.database import engine_app, engine_test, Base
from src.database.fixtures.products_fixtures import create_product
from src.database.fixtures.staff_fixtures import create_user
from src.database.models.staff.staff import StaffModels
from src.api.auth.auth_controller import auth_routes
from src.api.cashier.cashier_controller import cashier_routes
from src.api.sales_consultant.sales_consultant_controller import sales_consultant_routes
from src.api.accountant.accountant_controller import accountant_routes
from src.api.dependencies.require_role import require_role

app = FastAPI()

app.include_router(auth_routes, tags=["Auth servise"])
app.include_router(cashier_routes, tags=["Cashier service"], dependencies=[Depends(require_role("Касир"))])
app.include_router(sales_consultant_routes, tags=["Sales consultant service"], dependencies=[Depends(require_role("Продавець-консультант"))])
app.include_router(accountant_routes, tags=["Accountant service"], dependencies=[Depends(require_role("Бухгалтер"))])

async def init_models():
    async with engine_app.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_models():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
@app.on_event("startup")
async def on_startup():
    await init_models()
    await create_product()
    await create_user()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)