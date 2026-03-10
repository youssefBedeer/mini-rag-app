from pydantic import BaseModel, Field, field_validator
from typing import Optional 
from bson.objectid import ObjectID

class DataChunk(BaseModel):
    _id: Optional[ObjectID]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict 
    chunk_order: int= Field(..., gt=0)
    chunk_project_id: ObjectID
        
    class config:
        arbitrary_types_allowed = True

