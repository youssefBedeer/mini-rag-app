from pydantic import BaseModel, Field, field_validator
from typing import Optional 
from bson.objectid import ObjectID

class Project(BaseModel):
    _id: Optional[ObjectID]
    project_id: str= Field(..., min_length=1)
    
    @field_validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        
        else:
            return value
        
    class config:
        arbitrary_types_allowed = True

