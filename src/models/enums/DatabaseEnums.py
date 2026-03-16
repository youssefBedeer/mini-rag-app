from enum import Enum

class DatabaseEnums(Enum):
    
    COLLECTION_PROJECT_NAME = "projects"
    COLLECTION_CHUNK_NAME = "chunks"
    
    PROJECT_ID_INDEX = "project_id_index"
    CHUNK_PROJECT_ID_INDEX= "chunk_project_id_index"