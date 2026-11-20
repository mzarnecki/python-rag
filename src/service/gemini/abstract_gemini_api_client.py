import os

import requests

from service.env_loader import load_env


class AbstractGeminiAPIClient:
    def __init__(self):
        # Load environment variables
        if 'GOOGLE_GEMINI_API_KEY' not in os.environ:
            load_env()

        # Get API key from environment
        self.api_key = os.environ['GOOGLE_GEMINI_API_KEY']

        # Initialize HTTP client
        self.base_uri = 'https://generativelanguage.googleapis.com/v1beta/'
        self.http_client = requests.Session()

    def _request(self, method: str, model: str, data: dict) -> dict:
        url = f'{self.base_uri}models/{model}:{method}?key={self.api_key}'

        try:
            response = self.http_client.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=180,
            )
            response.raise_for_status()

            return response.json() or {}
        except requests.RequestException as e:
            # Handle the exception and log or rethrow as needed
            raise RuntimeError('Request failed: ' + str(e)) from e
