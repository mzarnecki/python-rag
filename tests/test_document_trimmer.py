from service.document_trimmer import DocumentTrimmer


def test_trim_returns_original_string_if_below_threshold():
    short_text = 'This is a short document.'
    assert DocumentTrimmer().trim(short_text) == short_text


def test_trim_cuts_document_to_6000_words_when_over_threshold():
    # The threshold is 0.75 * 8000 = 6000 letters/tokens
    # Creating a string with 7000 words (mostly letters) to trigger the trim
    long_text = 'word ' * 7000
    result = DocumentTrimmer().trim(long_text.strip())

    # Should be trimmed to exactly 6000 words
    assert len(result.split(' ')) == 6000
    assert result.startswith('word word word')
