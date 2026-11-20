from service.claude.abstract_claude_api_client import AbstractClaudeAPIClient


class ClaudeTextEncoder(AbstractClaudeAPIClient):
    """
    "Anthropic does not offer its own embedding model."
    Use encoder from other LLM API
    see https://docs.anthropic.com/en/docs/build-with-claude/embeddings
    """
