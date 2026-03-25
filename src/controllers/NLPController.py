from typing import List
from models.db_schemas.data_chunk import DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from .BaseController import BaseController 
from models.db_schemas import Project
import json
from stores.llm.templates.template_parser import TemplateParser
import logging

class NLPController(BaseController):
    def __init__(self, vectordb_client, generation_client, embedding_client, template_parser):
        super().__init__() 
        
        self.vectordb_client = vectordb_client 
        self.generation_clinet = generation_client 
        self.embedding_client = embedding_client 
        self.template_parser = template_parser
        
        self.logger = logging.getLogger(__name__)
        
    def create_collection_name(self, project_id):
        return f"collection_{project_id}".strip()
    
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id = project.project_id)
        return self.vectordb_client.delete_collection(collection_name = collection_name)
    
    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id= project.project_id) 
        collection_info = self.vectordb_client.get_collection_info(collection_name = collection_name)
        
        return json.loads(
            json.dumps(collection_info, default= lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project,
                                   chunks: List[DataChunk],
                                   chunks_ids: List[int],
                                   do_reset: bool = False):
        # step 1: get collection name 
        collection_name = self.create_collection_name(project_id = project.project_id)
        
        # step 2: manage items 
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in chunks ] 
        vectors = [
            self.embedding_client.embed_text(text = t, 
                                             document_type = DocumentTypeEnum.DOCUMENT.value)
            for t in texts
        ]
        
        # step 3: create collection 
        self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size, 
            do_reset = do_reset)
        
        # step 4: insert into vectordb
        self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            vectors = vectors,
            metadata = metadata,
            record_ids=chunks_ids)
        
        return True
    
    
    
    def search_vectordb_collection(self, project: Project, text: str, limit: int = 5):
        # step 1: get collection name 
        collection_name = self.create_collection_name(project_id= project.project_id)
        
        # step 2: get text embedding vector 
        vector = self.embedding_client.embed_text(text= text, document_type=DocumentTypeEnum.QUERY.value)
        
        if vector is None:
            return False
        
        # step 3: semantic search
        results = self.vectordb_client.search_by_vector(collection_name=collection_name ,vector= vector, limit= limit)
        if not results: 
            return False 
        
        return results
        
    def answer_rag_question(self, project: Project, query: str, limit: int=10):
        
        answer, full_prompt, chat_history = None, None, None
        # retrive realted documents 
        retrived_documents = self.search_vectordb_collection(
            project = project, 
            text = query,
            limit= limit
        )
        
        if not retrived_documents or len(retrived_documents) == 0:
            self.logger.error(f"No retrived_documents")
            return None, None, None
        # construct LLM prompt 
        system_prompt = self.template_parser.get("rag", "system_prompt")
        
        document_prompt = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                "doc_num": idx + 1,
                "chunk_text": doc.text
            })
            for idx, doc in enumerate(retrived_documents)
        ])
        
        footer_prompt = self.template_parser.get("rag", "footer_prompt")
        
        chat_history = [
            self.generation_clinet.construct_prompt(
                prompt = system_prompt,
                role = self.generation_clinet.enums.SYSTEM.value
            )
        ] 

        full_prompt = "\n\n".join([document_prompt, footer_prompt])
        
        answer = self.generation_clinet.generate_text(
            prompt = full_prompt,
            chat_history = chat_history
        )
        
        return answer, full_prompt, chat_history