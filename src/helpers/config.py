from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPEN_API_KEY: str

    FILE_ALLOWED_TYPES: List[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    WINDOWS_RESERVED: List[str]

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    # Providers
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_URL: Optional[str] = None

    COHERE_API_KEY: Optional[str] = None

    HF_API_KEY: Optional[str] = None

    # Models
    GENERATION_MODEL_ID: str 
    EMBEDDING_MODEL_ID: str 
    EMBEDDING_MODEL_SIZE: int

    # Defaults
    INPUT_DEFAULT_MAX_CHARACTERS: Optional[int] 
    GENERATION_DEFAULT_MAX_TOKENS: Optional[int] 
    GENERATION_DEFAULT_TEMPERATURE: Optional[float] 

    # VectorDB CONFIG
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str
    
    # Template Configs
    PRIMARY_LANG:str
    DEFAULT_LANG:str    
        
    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()