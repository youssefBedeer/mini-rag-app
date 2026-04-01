from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import logging 
import cohere


class CoHereProvider(LLMInterface):
    def __init__(self, api_key: str, base_url: str= None,
                    default_input_max_characters: int= 1000,
                    default_generation_max_output_tokens: int= 1000,
                    default_generation_temperature: float= 0.1,
                    ):
        self.api_key = api_key 
        
        self.default_input_max_characters = default_input_max_characters 
        self.default_generation_max_output_tokens = default_generation_max_output_tokens 
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id= None 
        self.embedding_model_id= None
        self.embedding_size= None 
        
        self.client = cohere.ClientV2(api_key= self.api_key)
        
        self.enums = CoHereEnums
        self.logger = logging.getLogger(__name__)
        
        
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
        
        
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
        
    def embed_text(self, text: str, document_type: str= None):
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None 
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set")
            return None
        
        
        input_type = DocumentTypeEnum.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = document_type
            
        response = self.client.embed(
            texts=[self.process_text(text)],
            model=self.embedding_model_id,
            input_type=input_type,
            output_dimension=self.embedding_size,
            embedding_types=["float"],
        )

        
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None 
        
        return response.embeddings.float[0]
    
    
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    
    def construct_prompt(self, prompt: str, role: str):
        return  {
                    "role": role, 
                    "text": prompt
                }            
    
    
    def generate_text(self, prompt: str, max_output_tokens: int, 
                    temperature: float = None,
                    chat_history: list = []):
                
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None 
        
        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat.completion.create(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            max_tokens = max_output_tokens,
            temperature = temperature
        )
        
        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None 
        
        return response.text