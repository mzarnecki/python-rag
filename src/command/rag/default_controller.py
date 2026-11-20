from service.document_provider import DocumentProvider
from service.openai.ada002_text_encoder import Ada002TextEncoder
from service.openai.generated_text_from_gpt_provider import GeneratedTextFromGPTProvider
from service.pipeline.payload import Payload
from service.pipeline.pipeline import Pipeline
from service.prompt_resolver import PromptResolver
from service.rag_prompt_provider import RAGPromptProvider
from service.text_splitter import TextSplitter


class DefaultController:
    def handle(self) -> None:
        print('Python Rag application')

        while True:
            question = input(
                'Find answer in websites database.\n'
                '(e.g. What is specialization of programmer and lecturer Michał Żarnecki based on his website content...)\n> '
            ).strip()
            if not question:
                print('A question is required.')
                continue

            print('Fetching response...')
            self._process(question)

    def _process(self, question: str) -> None:
        prompt_resolver = PromptResolver({'prompt': question})
        text_encoder = Ada002TextEncoder(TextSplitter())
        document_provider = DocumentProvider()
        rag_prompt_provider = RAGPromptProvider()
        generated_text_provider = GeneratedTextFromGPTProvider()
        payload = Payload()

        pipeline = (Pipeline()
                    .pipe(prompt_resolver)  # get prompt from POST or CLI
                    .pipe(text_encoder)  # get embeddings for prompt
                    .pipe(document_provider)  # find documents with similarity to prompt
                    .pipe(rag_prompt_provider)  # prepare RAG input - combine prompt with matched source documents
                    .pipe(generated_text_provider))  # get API response
        response = pipeline.process(payload)

        print(payload.get_rag_prompt())
        print('You asked: ' + question)
        print('\033[92mResponse: ' + response + '\033[0m')
        print()
