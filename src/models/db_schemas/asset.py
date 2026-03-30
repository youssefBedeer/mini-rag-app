from pydantic import BaseModel, Field 
from typing import Optional
from bson import ObjectId
from datetime import datetime, UTC


class Asset(BaseModel):
    
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId 
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1) 
    asset_size: float = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_created_at: datetime = Field(default=datetime.now(UTC))
    
    model_config = {
                    "arbitrary_types_allowed": True,
                    "populate_by_name": True,
                    "json_encoders": {ObjectId: str}
                    }
    
    @classmethod 
    def get_indexes(cls):
        return [
            {
                "key": [
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False 
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            }
        ]
