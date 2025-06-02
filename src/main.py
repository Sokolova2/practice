import os
from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import uvicorn
from src.database.database import engine, Base

load_dotenv()

app = FastAPI()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.creat_all)

@app.on_event("startup")
async def on_startup():
    await init_models()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)