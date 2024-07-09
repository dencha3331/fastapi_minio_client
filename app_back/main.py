from fastapi import FastAPI
from app_back.api import router as api_router
from app_back.db import engine
from app_back.storage import minio_client

app = FastAPI()

# Определите маршруты API
app.include_router(api_router)


# Инициализируйте подключение к базе данных
@app.on_event("startup")
async def startup():
    await engine.connect()


# Инициализируйте клиента хранилища
@app.on_event("startup")
async def startup():
    await minio_client.connect()


# Обработка событий закрытия
@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()
    await minio_client.close()
