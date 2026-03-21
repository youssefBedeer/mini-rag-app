from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from routes import base, data, test
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect mongodb on start
    settings = get_settings()
    
    app.mongo_conn = AsyncMongoClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    # llm provider 
    llm_provider_factory = LLMProviderFactory()
    
    ## generation model 
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND.value)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID.value)
    
    ## embedding model 
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND.value)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID.value, 
                                            embedding_size=settings.EMBEDDING_MODEL_SIZE.value)
    # Close on finish
    yield
    await app.mongo_conn.close()


app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(test.test_router)


