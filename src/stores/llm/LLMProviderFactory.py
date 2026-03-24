from .providers import CoHereProvider, OpenRouterProvider, OpenAIProvider
from .LLMEnums import LLMEnums


class LLMProviderFactory:

    def __init__(self, config):
        self.config = config

    def create(self, provider: str):

        if provider == LLMEnums.OPENAI.value:
            instance = OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                base_url=self.config.OPENAI_API_URL or "https://api.openai.com/v1"
            )

        elif provider == LLMEnums.OPENROUTER.value:
            instance = OpenRouterProvider(
                api_key=self.config.OPENROUTER_API_KEY,
                base_url=self.config.OPENROUTER_API_URL,
                huggingface_api_key=self.config.HF_API_KEY
            )

        elif provider == LLMEnums.COHERE.value:
            instance = CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )

        else:
            raise ValueError(f"Unsupported provider: {provider}")

        self._initialize_base(instance)
        return instance

    def _initialize_base(self, instance):

        # defaults
        if hasattr(instance, "default_input_max_characters"):
            instance.default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS

        if hasattr(instance, "default_generation_max_output_tokens"):
            instance.default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS

        if hasattr(instance, "default_generation_temperature"):
            instance.default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE

        # models
        if hasattr(instance, "set_generation_model"):
            instance.set_generation_model(self.config.GENERATION_MODEL_ID)

        if hasattr(instance, "set_embedding_model"):
            instance.set_embedding_model(
                self.config.EMBEDDING_MODEL_ID,
                self.config.EMBEDDING_MODEL_SIZE
            )