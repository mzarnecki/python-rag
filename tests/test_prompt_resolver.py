import os
import sys

from service.prompt_resolver import PromptResolver

SYSTEM_PROMPT = 'You are a helpful assistant that answers questions based on source documents.' + os.linesep


def test_prompt_is_default_prompt_provided_when_no_input_is_send(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli'])
    assert PromptResolver().get_prompt_from_input() == SYSTEM_PROMPT + 'What is the result of 2 + 2?'


def test_prompt_is_provided_when_console_arg_given(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['minicli', 'What is the result of 3 + 3?'])
    assert PromptResolver().get_prompt_from_input() == SYSTEM_PROMPT + 'What is the result of 3 + 3?'


def test_prompt_is_provided_when_post_given():
    prompt = PromptResolver({'prompt': 'What is the result of 4 + 4?'}).get_prompt_from_input()
    assert prompt == SYSTEM_PROMPT + 'What is the result of 4 + 4?'
