import os

from dotenv import load_dotenv


def load_env() -> None:
    """Equivalent of Dotenv::createImmutable(...)->load() - does not override already set variables."""
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
