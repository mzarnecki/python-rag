import math
import os

from service.text_splitter import TextSplitter


def get_lorem_ipsum() -> str:
    with open(os.path.join(os.path.dirname(__file__), 'lorem-ipsum.txt'), encoding='utf-8') as f:
        return f.read()


def test_text_splitter_keeps_common_part_between_chunks():
    chunks = TextSplitter().split_document_into_chunks(get_lorem_ipsum(), 300, 100)
    assert chunks[0][-100:] == chunks[1][:100]


def test_text_splitter_splits_to_expected_number_of_chunks():
    text = get_lorem_ipsum()
    chunks = TextSplitter().split_document_into_chunks(text, 200, 10)
    assert len(chunks) == math.ceil(len(text) / 190)
