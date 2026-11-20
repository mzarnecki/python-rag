import json
import os
import sys

import requests

from service.env_loader import load_env


class AbstractDeepSeekAPIClient:
    def __init__(self):
        if 'DEEPSEEK_API_KEY' not in os.environ:
            load_env()

        self.api_key = os.environ['DEEPSEEK_API_KEY']

        self.base_uri = 'https://api.deepseek.com/'
        self.http_client = requests.Session()

    def _request(self, messages: list[dict], model: str, stream: bool = False, options: dict | None = None) -> dict:
        data = {
            'model': model,
            'messages': messages,
            'stream': stream,
            **(options or {}),
        }

        try:
            response = self.http_client.post(
                self.base_uri + 'chat/completions',
                json=data,
                headers={
                    'Authorization': 'Bearer ' + self.api_key,
                    'Content-Type': 'application/json',
                },
                timeout=180,
            )
            response.raise_for_status()
            response_data = response.json()
            print(json.dumps(response_data), file=sys.stderr)

            return response_data or {}
        except requests.RequestException as e:
            raise RuntimeError('DeepSeek API request failed: ' + str(e)) from e
