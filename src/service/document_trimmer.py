import re


class DocumentTrimmer:
    def trim(self, document: str) -> str:
        """cut document to tokens limit 8192"""
        # [^\W\d_]+ is the Python `re` equivalent of PCRE \p{L}+ (sequence of unicode letters)
        if len(re.findall(r'[^\W\d_]+', document)) >= 0.75 * 8000:
            words = document.split(' ')
            return ' '.join(words[:6000])

        return document
