from .BaseOpenAIProvider import BaseOpenAIProvider 
from huggingface_hub import InferenceClient


class OpenRouterProvider(BaseOpenAIProvider):
        
    def __init__(
        self,
        api_key: str,
        api_url: str,
        huggingface_api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        
        super().__init__(
            api_key=api_key,
            api_url=api_url,
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
        
        # Normalize input
        texts = [text] if isinstance(text, str) else text
        
        response = self.embedding_client.feature_extraction(
            texts,
            model=self.embedding_model_id
        )
        
        if not response:
            self.logger.error("Error while embedding text with Huggingface")
            return None 
        
        return response