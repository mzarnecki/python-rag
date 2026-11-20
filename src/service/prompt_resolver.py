import os
import sys

from service.pipeline.payload import Payload


class PromptResolver:
    def __init__(self, post: dict | None = None):
        # equivalent of PHP $_POST
        self.post = post or {}

    def get_prompt_from_input(self) -> str:
        prompt = self.post.get('prompt')
        if not prompt:
            prompt = sys.argv[1] if len(sys.argv) > 1 else None
        if not prompt:
            prompt = 'What is the result of 2 + 2?'

        return self._get_system_prompt() + prompt

    def __call__(self, payload: Payload) -> Payload:
        return payload.set_prompt(self.get_prompt_from_input())

    def _get_system_prompt(self) -> str:
        return 'You are a helpful assistant that answers questions based on source documents.' + os.linesep
