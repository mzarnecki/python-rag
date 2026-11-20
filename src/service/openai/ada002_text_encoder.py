import json

from service.openai.abstract_gpt_api_client import AbstractGPTAPIClient
from service.pipeline.payload import Payload
from service.text_encoder_interface import TextEncoderInterface
from service.text_splitter import TextSplitter


class Ada002TextEncoder(AbstractGPTAPIClient, TextEncoderInterface):
    def __init__(self, text_splitter: TextSplitter):
        self.embedding_model = 'text-embedding-ada-002'
        self.text_splitter = text_splitter
        super().__init__()

    def get_embeddings(self, document: str) -> list[str]:
        chunks = self.text_splitter.split_document_into_chunks(document, 9000, 200)
        embeddings = []

        for chunk in chunks:
            response = self.client.embeddings.create(
                input=chunk,
                model=self.embedding_model,
            )
            embeddings.append(json.dumps(response.data[0].embedding, separators=(',', ':')))

        return embeddings

    def __call__(self, payload: Payload) -> Payload:
        return payload.set_embedding_prompt(self.get_embeddings(payload.get_prompt())[0])
