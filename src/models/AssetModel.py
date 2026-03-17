from .BaseDataModel import BaseDataModel
from .db_schemas.asset import Asset
from .enums import DatabaseEnums
from bson import ObjectId 


class AssetModel(BaseDataModel):
    
    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DatabaseEnums.COLLECTION_ASSET_NAME.value]
        
    
    async def init_collection(self):
        indexes = await self.collection.index_information() 
        
        if (DatabaseEnums.ASSET_PROJECT_ID_INDEX.value not in indexes) \
        or (DatabaseEnums.ASSET_PROJECT_ID_NAME_INDEX.value not in indexes):
            
            for index in Asset.get_indexes():
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
                
    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client=db_client)
        await instance.init_collection() 
        return instance 
    

    async def create_asset(self, asset:Asset) -> Asset:
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_none=True))
        asset.id = result.inserted_id 
        return asset 
    
    
    async def get_all_project_assets(self, asset_project_id:str)-> list:
        result = self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
        }).tolist(length=None)
        
            