from .VectorDBEnums import VectorDBEnums
from .providers import QdrantDB, PGVectorProvider
from controllers.BaseController import BaseController
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from helpers.config import Settings


class VectorDBProviderFactory():
    def __init__(self, config: Settings, db_client: async_sessionmaker[AsyncSession]):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client
    
    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            
            qdrant_db_client = self.base_controller.get_database_path(self.config.VECTOR_DB_PATH)
            return QdrantDB(db_client = qdrant_db_client,
                            default_vector_size = self.config.EMBEDDING_MODEL_SIZE,
                            distance_method = self.config.VECTOR_DB_DISTANCE_METHOD,
                            index_threshold = self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD)
            
        elif provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(db_client = self.db_client,
                                    default_vector_size = self.config.EMBEDDING_MODEL_SIZE,
                                    distance_method = self.config.VECTOR_DB_DISTANCE_METHOD,
                                    index_threshold = self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD)
            
        return None