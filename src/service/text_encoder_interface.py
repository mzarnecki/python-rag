from abc import ABC, abstractmethod


class TextEncoderInterface(ABC):
    @abstractmethod
    def get_embeddings(self, document: str) -> list[str]:
        """:return: chunks with embeddings"""
