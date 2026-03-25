from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from routes import base, data, nlp
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect mongodb on start
    settings = get_settings()
    
    app.mongo_conn = AsyncMongoClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    ## initialize providers
    llm_provider_factory = LLMProviderFactory(config=settings)
    vectordb_provider_factory = VectorDBProviderFactory(config=settings)
    
    ## generation model 
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    
    ## embedding model 
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID, 
                                            embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    ## vectordb client 
    app.vectordb_client = vectordb_provider_factory.create(provider = settings.VECTOR_DB_BACKEND) 
    app.vectordb_client.connect()
    
    ## template parser 
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )
    
    # Close on finish
    yield
    await app.mongo_conn.close()
    app.vectordb_client.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)


