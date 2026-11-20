import os
import sys

from service.abstract_document_repository import AbstractDocumentRepository
from service.document_trimmer import DocumentTrimmer
from service.text_encoder_interface import TextEncoderInterface


class DocumentLoader(AbstractDocumentRepository):
    def __init__(self, text_encoder: TextEncoderInterface, document_trimmer: DocumentTrimmer):
        self.text_encoder = text_encoder
        self.document_trimmer = document_trimmer
        super().__init__()

    def load_documents(self, skipped_documents_number: int = 0) -> None:
        path = os.path.join(os.path.dirname(__file__), '..', 'documents')
        files = sorted(os.listdir(path))
        total = len(files)

        for index, file in enumerate(files):
            if index < skipped_documents_number:
                continue
            with open(os.path.join(path, file), encoding='utf-8', errors='replace') as f:
                document = f.read()

            # cut document to tokens limit 8192
            document = self.document_trimmer.trim(document)

            # load documents to postgres database
            try:
                response_documents_chunks = self.text_encoder.get_embeddings(document)
            except Exception as e:
                print(e, file=sys.stderr)
                return

            for chunk in response_documents_chunks:
                self._insert_document(file, document, chunk)
            self._show_progress(index, total, skipped_documents_number)
        print('Loading documents complete')

    def _show_progress(self, index: int, total: int, skip: int) -> None:
        all_documents = total - skip
        num_loaded = index - skip + 1
        if num_loaded % 10 == 0:
            progress = '-' * (num_loaded // 10)
            print(f'{progress}\nLoaded {num_loaded} of {all_documents} source documents to vector DB')

    def _insert_document(self, name: str, document: str, embedding: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO document(name, text, embedding) VALUES(%(name)s, %(doc)s, %(embed)s)',
                {'name': name, 'doc': document, 'embed': embedding},
            )
