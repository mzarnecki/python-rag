class Payload:
    def __init__(self):
        self.prompt: str = ''
        self.embedding_prompt: str = ''
        self.similar_documents: list[str] = []
        self.similar_documents_names: list[str] = []
        self.rag_prompt: str = ''
        self._use_reranking: bool = False

    def get_prompt(self) -> str:
        return self.prompt

    def set_prompt(self, prompt: str) -> "Payload":
        self.prompt = prompt
        return self

    def get_embedding_prompt(self) -> str:
        return self.embedding_prompt

    def set_embedding_prompt(self, embedding_prompt: str) -> "Payload":
        self.embedding_prompt = embedding_prompt
        return self

    def get_similar_documents(self) -> list[str]:
        return self.similar_documents

    def set_similar_documents(self, similar_documents: list[str]) -> "Payload":
        self.similar_documents = similar_documents
        return self

    def get_similar_documents_names(self) -> list[str]:
        return self.similar_documents_names

    def set_similar_documents_names(self, similar_documents_names: list[str]) -> "Payload":
        self.similar_documents_names = similar_documents_names
        return self

    def get_rag_prompt(self) -> str:
        return self.rag_prompt

    def set_rag_prompt(self, rag_prompt: str) -> "Payload":
        self.rag_prompt = rag_prompt
        return self

    def use_reranking(self) -> bool:
        return self._use_reranking

    def set_use_reranking(self, use_reranking: bool) -> "Payload":
        self._use_reranking = use_reranking
        return self
