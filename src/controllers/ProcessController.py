from .BaseController import BaseController 
from .ProjectController import ProjectController
from .DataController import DataController
from models import ProcessingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 
from uuid import uuid4

class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__() 
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    
    # extract file extension 
    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    
    # load using proper loader from langchain 
    def get_proper_loader(self, file_id:str):
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path,file_id)
        
        if file_ext == ProcessingEnum.TEXT.value:
            return TextLoader(file_path, encoding='utf-8')
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
            
        else:
            return None
        
    # get content
    def get_content(self, file_id:str):
        loader = self.get_proper_loader(file_id=file_id)
        return loader.load()
    
    
    # chunk
    def process_file_content(self, file_content: list, file_id:str,
                            chunk_size: int=100, overlap: int=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        
        # store file content and metadata
        file_content_texts = [doc.page_content for doc in file_content]
        file_content_metadata = [doc.metadata for doc in file_content]
        
        chunks = text_splitter.create_documents(
            file_content_texts, 
            metadatas = file_content_metadata
        )
        
        # add id
        for i, chunk in enumerate(chunks):
            chunk.id = f"{file_id}_{i}"
            chunk.metadata["chunk_id"] = f"{file_id}_{i}"
            chunk.metadata["doc_id"] = file_id
            chunk.metadata["uuid"] = str(uuid4())
        
        return chunks
    
    
    