class TextSplitter:
    def split_document_into_chunks(self, document: str, chunk_size: int, overlap: int) -> list[str]:
        chunks = []
        length = len(document)
        start = 0

        while start < length:
            end = min(start + chunk_size, length)
            chunks.append(document[start:end])
            start += chunk_size - overlap

        return chunks
