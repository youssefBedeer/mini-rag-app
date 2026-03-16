from .BaseDataModel import BaseDataModel 
from .enums.DatabaseEnums import DatabaseEnums
from .db_schemas import DataChunk
from pymongo import InsertOne
from bson import ObjectId



class ChunkModel(BaseDataModel):

    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DatabaseEnums.COLLECTION_CHUNK_NAME.value]
        
    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client) 
        await instance.init_collection()
        return instance    
    
    
    async def init_collection(self):
        indexes = await self.collection.index_information()

        if DatabaseEnums.CHUNK_PROJECT_ID_INDEX not in indexes:
            for index in DataChunk.get_indexes():
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
    
    
    async def create_chunk(self, chunk:DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True ,exclude=None))
        chunk.id = result.inserted_id 
        
        return chunk 
    
    
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "chunk_id": chunk_id
        })
        
        return None if result is None else  DataChunk(**result)
    
    
    async def insert_many_chunks(self, chunks:list, batch_size: int=100):
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            
            operations = [InsertOne(chunk.model_dump(exclude_none=True, by_alias=True)) for chunk in batch]
            
            result = await self.collection.bulk_write(operations)
            
        return result.inserted_count
    
    
    async def delete_chunks_by_project_id(self, project_id:ObjectId):
        
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        
        return f" deleted count: {result.deleted_count}"