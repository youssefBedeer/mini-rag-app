from stores.llm.LLMEnums import OpenRouterEnums

from .BaseOpenAIProvider import BaseOpenAIProvider 
from huggingface_hub import InferenceClient



class OpenRouterProvider(BaseOpenAIProvider):
        
    def __init__(
        self,
        api_key: str,
        base_url: str,
        huggingface_api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            default_input_max_characters=default_input_max_characters,
            default_generation_max_output_tokens=default_generation_max_output_tokens,
            default_generation_temperature=default_generation_temperature,
        )
        
        self.embedding_client = InferenceClient(
            provider="hf-inference",
            api_key=huggingface_api_key,
        )
        
    def embed_text(self, text: str, document_type: str = None):
        if not self.embedding_client:
            self.logger.error("HF client was not set")
            return None 
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model was not set")
            return None
        
        response = self.embedding_client.feature_extraction(
            text,
            model=self.embedding_model_id
        )
        
        if response.size == 0:
            self.logger.error("Error while embedding text with Huggingface")
            return None 
        
        return response