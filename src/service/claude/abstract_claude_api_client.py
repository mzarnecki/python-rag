import json
import os
import sys

import requests

from service.env_loader import load_env


class AbstractClaudeAPIClient:
    def __init__(self):
        # Load environment variables
        if 'ANTHROPIC_API_KEY' not in os.environ:
            load_env()

        # Get API key from environment
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')

        # Initialize HTTP client
        self.base_uri = 'https://api.anthropic.com/v1/'
        self.http_client = requests.Session()

    def _request(self, prompt: str, endpoint: str, model: str) -> dict:
        data = {
            'model': model,
            'max_tokens': 2048,
            'temperature': 0,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        }

        try:
            response = self.http_client.post(
                self.base_uri + endpoint,
                json=data,
                headers={
                    'x-api-key': self.api_key,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json',
                },
                timeout=180,
            )
            response.raise_for_status()
            response_data = response.json()

            # Log the response for debugging
            print(json.dumps(response_data), file=sys.stderr)

            return response_data or {}
        except requests.RequestException as e:
            # Handle the exception and log or rethrow as needed
            raise RuntimeError('Request failed: ' + str(e)) from e
