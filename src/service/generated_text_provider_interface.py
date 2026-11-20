from abc import ABC, abstractmethod


class GeneratedTextProviderInterface(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        pass

    @abstractmethod
    def set_model(self, model: str) -> "GeneratedTextProviderInterface":
        pass
