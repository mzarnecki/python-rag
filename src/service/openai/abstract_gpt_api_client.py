import os

from openai import OpenAI

from service.env_loader import load_env


class AbstractGPTAPIClient:
    def __init__(self):
        if 'OPENAI_API_KEY' not in os.environ:
            load_env()

        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
