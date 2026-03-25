from models.db_schemas.data_chunk import RetrievedDocument

from ..VectorDBInterface import VectorDBInterface 
from ..VectorDBEnums import DistanceMethodEnums
import logging 
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams
from typing import List
import numpy as np

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path:str, distance_method: str = "cosine"):
        self.db_path = db_path
        self.distance_method = distance_method
        self.client = None
        
        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
            
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
            
        self.logger = logging.getLogger(__name__)
    
    
    def connect(self) -> None:
        self.client = QdrantClient(path = self.db_path)
    
    def disconnect(self) -> None:
        self.client = None
    
    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str)-> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str) -> None:
        if self.is_collection_existed(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)
    
    def create_collection(self, collection_name: str,
                                embedding_size: int, 
                                do_reset: bool = False) -> bool:
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)
            
        if not self.is_collection_existed(collection_name=collection_name):
            _ = self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=embedding_size, 
                                                distance=self.distance_method),
                )
            return True 
        
        return False
    
    
    def insert_one(self, collection_name: str,
                          text: str,
                          vector: list,
                          metadata: dict = None, 
                          record_id: str = None):
        
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"Can not insert record, collection: {collection_name} not existed.")
            return False
        
        try:
            _ = self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct( 
                        id = [record_id],
                        vector = vector, 
                        payload= {
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ],
            )
        except Exception as e:
            self.logger.error(f"Error while insert record: {e}")
            return False
            
        return True
            
    
    def insert_many(self, collection_name: str,
                          texts: list[str],
                          vectors: list[list],
                          metadata: list[dict] = None,
                          record_ids: list[str] = None,
                          batch_size: int = 50):
        
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"Can not insert record, collection: {collection_name} not existed.")
            return False
    
        if metadata is None:
            metadata = [None] * len(texts)
            
        if record_ids is None:
            record_ids = list(range(0, len(texts)))
                
        for i in range(0, len(texts), batch_size):
                
            batch_end = i + batch_size 
            
            batch_record_ids = record_ids[i:batch_end]
            batch_texts = texts[i:batch_end]
            batch_vecotrs = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            
            batch_records = [

                models.PointStruct( 
                    id = batch_record_ids[x],
                    vector = batch_vecotrs[x], 
                    payload= {
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x]
                    }
                )
                
                for x in range(len(batch_texts))
            ] 
            
            try:
                _ = self.client.upsert(
                    collection_name=collection_name,
                    points= batch_records
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False
            
        return True
        

    def search_by_vector(self, collection_name: str, vector, limit: int = 5) -> List[RetrievedDocument] :
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"Can not search, collection: {collection_name} not existed.")
            return False

        results =  self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        )

        return [
            RetrievedDocument(**{
                "text": result.payload["text"],
                "score": result.score
            })
            for result in results.points
        ]