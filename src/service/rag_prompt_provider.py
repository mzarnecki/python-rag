import tiktoken

from service.pipeline.payload import Payload


class RAGPromptProvider:
    CONTEXT_TOKEN_COUNT = 5000

    def get_rag_prompt(self, documents: list[str], prompt: str) -> str:
        encoding = tiktoken.encoding_for_model('gpt-4')
        context_token_count = self.CONTEXT_TOKEN_COUNT - len(encoding.encode(prompt)) - 20
        input_text = ''
        for document in documents:
            input_text += document + "\n\n"
            tokens = encoding.encode(input_text)

            if len(tokens) > context_token_count:
                break

        return input_text

    def __call__(self, payload: Payload) -> Payload:
        return payload.set_rag_prompt(self.get_rag_prompt(payload.get_similar_documents(), payload.get_prompt()))
