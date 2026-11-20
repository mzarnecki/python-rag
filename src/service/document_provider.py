import sys

from service.abstract_document_repository import AbstractDocumentRepository
from service.pipeline.payload import Payload


class DocumentProvider(AbstractDocumentRepository):
    def get_similar_documents(
        self,
        prompt: str,
        embedding_prompt: str,
        use_reranking: bool = False,
        limit: int = 10,
        distance_function: str = 'l2',
    ) -> tuple[list[str], list[str]]:
        """:param distance_function: l2|cosine|innerProduct"""
        query = self._get_query_for_distance_function(distance_function, limit)
        with self.connection.cursor() as cursor:
            cursor.execute(query, {'embeddingPrompt': embedding_prompt})
            documents = cursor.fetchall()
        print('RETRIEVED DOCUMENTS:', file=sys.stderr)
        documents_names = []
        for document in documents:
            documents_names.append(document['name'])
            print(document['name'], file=sys.stderr)
        if use_reranking:
            documents = self.rerank(prompt, documents)
        else:
            documents = [document['text'] for document in documents]

        return documents, documents_names

    def rerank(self, prompt: str, documents: list[dict]) -> list[str]:
        """Sometimes its worth to use efficient algorithm for querying vector DB and more precise to rerank chosen documents in"""
        documents_reranked = {}
        prompt_words = set(prompt.split(' '))
        for document in documents:
            intersection = [word for word in document['text'].split(' ') if word in prompt_words]
            index = len(intersection)
            while index in documents_reranked:
                index += 1
            documents_reranked[index] = document['text']

        return [documents_reranked[key] for key in sorted(documents_reranked, reverse=True)]

    def _get_query_for_distance_function(self, distance_function: str, limit: int = 10) -> str:
        match distance_function:
            case 'l2':
                return self._get_query_for_l2_distance(limit)
            case 'cosine':
                return self._get_query_for_cosine_distance(limit)
            case 'innerProduct':
                return self._get_query_for_inner_product(limit)
            case _:
                raise ValueError('Unknown distance function: ' + distance_function)

    def _get_query_for_l2_distance(self, limit: int = 10) -> str:
        return f'SELECT name, text from document order by embedding <-> %(embeddingPrompt)s limit {int(limit)};'

    def _get_query_for_cosine_distance(self, limit: int = 10) -> str:
        return f'SELECT name, text from document order by 1 - (embedding <=> %(embeddingPrompt)s) limit {int(limit)};'

    def _get_query_for_inner_product(self, limit: int = 10) -> str:
        return f'SELECT name, text from document order by (embedding <#> %(embeddingPrompt)s) * -1 limit {int(limit)};'

    def __call__(self, payload: Payload) -> Payload:
        documents, documents_names = self.get_similar_documents(
            payload.get_prompt(),
            payload.get_embedding_prompt(),
            payload.use_reranking(),
        )
        payload.set_similar_documents(documents)
        payload.set_similar_documents_names(documents_names)

        return payload
