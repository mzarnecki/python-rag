from service.claude.abstract_claude_api_client import AbstractClaudeAPIClient
from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.pipeline.payload import Payload


class GeneratedTextFromClaudeProvider(AbstractClaudeAPIClient, GeneratedTextProviderInterface):
    def __init__(self):
        self.model = 'claude-3-7-sonnet-latest'
        super().__init__()

    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        # Make API request
        response = self._request(
            source_documents + "\n\n##### INPUT: \n" + prompt + "\n##### RESPONSE:\n",
            'messages',
            self.model,
        )

        return response['content'][0]['text']

    def set_model(self, model: str) -> "GeneratedTextFromClaudeProvider":
        self.model = model
        return self

    def __call__(self, payload: Payload) -> str:
        return self.generate_text(payload.get_prompt(), payload.get_rag_prompt())
