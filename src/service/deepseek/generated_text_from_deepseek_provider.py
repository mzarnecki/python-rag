from service.deepseek.abstract_deepseek_api_client import AbstractDeepSeekAPIClient
from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.pipeline.payload import Payload


class GeneratedTextFromDeepSeekProvider(AbstractDeepSeekAPIClient, GeneratedTextProviderInterface):
    def __init__(self):
        self.model = 'deepseek-chat'
        super().__init__()

    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': source_documents + "\n\n" + prompt},
        ]

        response = self._request(
            messages=messages,
            model=self.model,
            stream=False,
        )

        return response.get('choices', [{}])[0].get('message', {}).get('content', '')

    def set_model(self, model: str) -> "GeneratedTextFromDeepSeekProvider":
        self.model = model
        return self

    def __call__(self, payload: Payload) -> str:
        return self.generate_text(payload.get_prompt(), payload.get_rag_prompt())
