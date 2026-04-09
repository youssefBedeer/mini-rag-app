from enum import Enum

class DatabaseEnums(Enum):
    
    COLLECTION_PROJECT_NAME = "projects"
    COLLECTION_CHUNK_NAME = "chunks"
    COLLECTION_ASSET_NAME = "assets"
    
    PROJECT_ID_INDEX = "project_id_index"
    CHUNK_PROJECT_ID_INDEX= "chunk_project_id_index"
    ASSET_PROJECT_ID_INDEX= "asset_project_id_index_1"
    ASSET_PROJECT_ID_NAME_INDEX= "asset_project_id_name_index_1"