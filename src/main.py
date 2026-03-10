from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient 
from helpers.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect mongodb on start
    settings = get_settings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    # Close on finish
    yield
    app.congo_conn.close()


app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)


