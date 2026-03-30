import uuid
from .minirag_base import SQLAlchemyBase 
from sqlalchemy import UUID, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

class Project(SQLAlchemyBase):
    __tablename__ = "projects" 
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")