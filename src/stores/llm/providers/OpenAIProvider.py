from .BaseOpenAIProvider import BaseOpenAIProvider 


class OpenAIProvider(BaseOpenAIProvider):
    
    def __init__(self, api_key: str):
        super().__init__(api_key= api_key,
                        api_url= None)