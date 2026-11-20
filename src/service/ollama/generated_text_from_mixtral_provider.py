from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.ollama.abstract_ollama_api_client import AbstractOllamaAPIClient
from service.pipeline.payload import Payload


class GeneratedTextFromMixtralProvider(AbstractOllamaAPIClient, GeneratedTextProviderInterface):
    def __init__(self):
        self.model = ''

    def set_model(self, model: str) -> "GeneratedTextFromMixtralProvider":
        self.model = model
        return self

    def __call__(self, payload: Payload) -> str:
        return self.generate_text(payload.get_prompt(), payload.get_rag_prompt())

    def _get_endpoint(self) -> str:
        return '/api/generate'

    def _get_body_params(self, input_text: str) -> dict:
        return {
            'model': 'mistral',
            'prompt': input_text,
        }
