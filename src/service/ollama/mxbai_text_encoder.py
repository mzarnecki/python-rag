import json

from service.ollama.abstract_ollama_api_client import AbstractOllamaAPIClient
from service.pipeline.payload import Payload
from service.text_encoder_interface import TextEncoderInterface
from service.text_splitter import TextSplitter


class MxbaiTextEncoder(AbstractOllamaAPIClient, TextEncoderInterface):
    def __init__(self, text_splitter: TextSplitter):
        self.embedding_model = 'mxbai-embed-large'
        self.text_splitter = text_splitter

    def get_embeddings(self, document: str) -> list[str]:
        chunks = self.text_splitter.split_document_into_chunks(document, 9000, 200)
        embeddings = []

        for chunk in chunks:
            response = self._request(chunk)
            embeddings.append(json.dumps(json.loads(response)['embedding'], separators=(',', ':')))

        return embeddings

    def __call__(self, payload: Payload) -> Payload:
        return payload.set_embedding_prompt(self.get_embeddings(payload.get_prompt())[0])

    def _get_endpoint(self) -> str:
        return '/api/embeddings'

    def _get_body_params(self, input_text: str) -> dict:
        return {
            'model': self.embedding_model,
            'prompt': input_text,
        }
