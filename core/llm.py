"""
core/llm.py
-----------
Central LLM wrapper. Returns a LangChain-compatible ChatOllama instance
so every agent and chain in the project uses the same model/config.
"""
from langchain_ollama import ChatOllama
from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL


def get_llm(temperature: float = 0.3, model: str | None = None) -> ChatOllama:
    """Return a configured ChatOllama instance."""
    return ChatOllama(
        model=model or OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )
