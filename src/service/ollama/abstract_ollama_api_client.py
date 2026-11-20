import json
import sys
from abc import ABC, abstractmethod

import requests


class AbstractOllamaAPIClient(ABC):
    def _request(self, input_text: str) -> str:
        # get response
        response = requests.post(
            'http://ollama-container:11434' + self._get_endpoint(),
            data=json.dumps(self._get_body_params(input_text)),
        )

        return response.text

    def generate_text(self, prompt: str, source_documents: str = '') -> str:
        # prepare input
        input_text = "Source documents:\n" + source_documents + "\n\n##### INPUT: \n" + prompt + "\n##### RESPONSE:\n"
        print('Source documents: ' + source_documents, file=sys.stderr)
        print("\n\n##### INPUT: \n" + prompt + "\n##### RESPONSE:\n", file=sys.stderr)
        body = self._request(input_text)

        # ollama streams response as one JSON object per line
        response = []
        for item in body.split("\n"):
            if not item.strip():
                continue
            row = json.loads(item)
            response.append(row.get('response', '') if row else '')

        return ''.join(response)

    @abstractmethod
    def _get_endpoint(self) -> str:
        pass

    @abstractmethod
    def _get_body_params(self, input_text: str) -> dict:
        pass
