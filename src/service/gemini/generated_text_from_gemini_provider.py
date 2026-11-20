from service.gemini.abstract_gemini_api_client import AbstractGeminiAPIClient
from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.pipeline.payload import Payload


class GeneratedTextFromGeminiProvider(AbstractGeminiAPIClient, GeneratedTextProviderInterface):
    def __init__(self):
        self.model = 'gemini-2.0-flash-exp'
        super().__init__()

    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        # Prepare the content
        content = source_documents + "\n\n##### INPUT: \n" + prompt + "\n##### RESPONSE:\n"

        # Create the request
        response_data = self._request(
            'generateContent',
            self.model,
            {
                'contents': {
                    'parts': [
                        {'text': content},
                    ],
                },
            },
        )

        return response_data['candidates'][0]['content']['parts'][0]['text']

    def set_model(self, model: str) -> "GeneratedTextFromGeminiProvider":
        self.model = model
        return self

    def __call__(self, payload: Payload) -> str:
        return self.generate_text(payload.get_prompt(), payload.get_rag_prompt())
