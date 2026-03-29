from .BaseOpenAIProvider import BaseOpenAIProvider 

class OpenRouterProvider(BaseOpenAIProvider):

    def __init__(
        self,
        api_key: str,
        base_url: str,
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