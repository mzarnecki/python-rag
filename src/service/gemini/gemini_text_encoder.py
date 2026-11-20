import json

from service.gemini.abstract_gemini_api_client import AbstractGeminiAPIClient
from service.pipeline.payload import Payload
from service.text_encoder_interface import TextEncoderInterface
from service.text_splitter import TextSplitter


class GeminiTextEncoder(AbstractGeminiAPIClient, TextEncoderInterface):
    def __init__(self, text_splitter: TextSplitter):
        self.embedding_model = 'text-embedding-004'
        self.text_splitter = text_splitter
        super().__init__()

    def get_embeddings(self, document: str) -> list[str]:
        # Split document into overlapping chunks of 9000 characters with 200-character overlap
        chunks = self.text_splitter.split_document_into_chunks(document, 9000, 200)
        embeddings = []

        for chunk in chunks:
            response = self._request(
                'embedContent',
                self.embedding_model,
                {
                    'content': {'parts': [{
                        'text': chunk,
                    }]},
                },
            )
            embeddings.append(json.dumps(response['embedding']['values'], separators=(',', ':')))

        return embeddings

    def __call__(self, payload: Payload) -> Payload:
        return payload.set_embedding_prompt(self.get_embeddings(payload.get_prompt())[0])
