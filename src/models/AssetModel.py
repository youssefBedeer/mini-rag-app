from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums import DatabaseEnums
from bson import ObjectId 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AssetModel(BaseDataModel):
    
    def __init__(self, db_client: async_sessionmaker[AsyncSession]):
        super().__init__(db_client=db_client)
        self.db_client = db_client


    @classmethod 
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance
    
    async def create_asset(self, asset: Asset) -> Asset:
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.refresh(asset)
        
        print(asset)
        return asset
    
    async def get_all_project_assets(self,asset_project_id: str,asset_type: str) -> list[Asset]:

        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_type == asset_type
            )
            result = await session.execute(query)
            records = result.scalars().all()
        return records
    
    
    async def get_asset_record(self, asset_project_id: str, asset_name: str) -> Asset:
        
        async with self.db_client() as session:
            query = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(query)
            record = result.scalar_one_or_none()
        return record

        
        