import uuid

from pydantic import BaseModel
from sqlalchemy import Column, Index, Integer, UUID, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql.json import JSONB
from .minirag_base import SQLAlchemyBase
from sqlalchemy.orm import relationship

class Asset(SQLAlchemyBase):
    __tablename__ = "assets"
    
    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    asset_name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)
    asset_config = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    
    project = relationship("Project", back_populates="assets")
    chunks = relationship("DataChunk", back_populates="asset")
    
    __table_args__ = (
        Index("ix_asset_project_id", asset_project_id),
        Index("ix_asset_type", asset_type)
    )