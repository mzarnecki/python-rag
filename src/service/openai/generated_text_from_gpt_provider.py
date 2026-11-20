from service.generated_text_provider_interface import GeneratedTextProviderInterface
from service.openai.abstract_gpt_api_client import AbstractGPTAPIClient
from service.pipeline.payload import Payload


class GeneratedTextFromGPTProvider(AbstractGPTAPIClient, GeneratedTextProviderInterface):
    def __init__(self):
        self.model = 'gpt-5-mini'
        super().__init__()

    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        # prepare API input
        input_text = source_documents + "\n\n##### INPUT: \n" + prompt + "\n##### RESPONSE:\n"

        # get API response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'content': input_text,
                    'role': 'user',
                },
            ],
        )

        return str(response.choices[0].message.content)

    def set_model(self, model: str) -> "GeneratedTextFromGPTProvider":
        self.model = model
        return self

    def __call__(self, payload: Payload) -> str:
        return self.generate_text(payload.get_prompt(), payload.get_rag_prompt())
