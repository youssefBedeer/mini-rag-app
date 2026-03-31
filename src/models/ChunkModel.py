from typing import List

from .BaseDataModel import BaseDataModel 
from .enums.DatabaseEnums import DatabaseEnums
from .db_schemas import DataChunk
from pymongo import InsertOne
from sqlalchemy.future import select
from sqlalchemy import func, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker




class ChunkModel(BaseDataModel):

    def __init__(self, db_client: async_sessionmaker[AsyncSession]):
        super().__init__(db_client=db_client)
        self.db_client = db_client


    @classmethod 
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance
    
    
    async def create_chunk(self, chunk:DataChunk) -> DataChunk:
        
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.refresh(chunk)
        return chunk
    
    
    async def get_chunk(self, chunk_id: str) -> DataChunk:
        
        async with self.db_client() as session:
            query = select(DataChunk).where(DataChunk.chunk_id == chunk_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        


    async def insert_many_chunks(self, chunks:list, batch_size: int=100):
        total_inserted = 0
        
        async with self.db_client() as session:
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                
                async with session.begin():
                    session.add_all(batch)
                
                total_inserted += len(batch)
        return total_inserted
        
    
    
    async def delete_chunks_by_project_id(self, project_id:int):
        
        async with self.db_client() as session:
            async with session.begin():
                result = await session.execute(
                    delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                )
                
            return result.rowcount or 0
    
    
    async def get_project_chunk(self, 
                                project_id: int,
                                page_no: int = 1, 
                                page_size: int = 50) -> List[DataChunk]:
        
        async with self.db_client() as session:
            result = await session.execute(
                select(DataChunk).where(DataChunk.chunk_project_id == project_id)\
                    .offset( (page_no - 1) * page_size ).limit(page_size)
            )
        return result.scalars().all()
        
