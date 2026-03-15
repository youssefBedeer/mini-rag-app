from pydantic import BaseModel, Field, field_validator
from typing import Optional 
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId]= Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict 
    chunk_order: int= Field(..., gt=0)
    chunk_project_id: ObjectId
        
    model_config = {
                    "arbitrary_types_allowed": True,
                    "populate_by_name": True,
                    "json_encoders": {ObjectId: str}
                    }

