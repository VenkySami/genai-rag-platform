import os
from typing import Literal

from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

TaskType = Literal["rag_qa", "qa", "code", "math", "general", "search"]


def _load_openai(model: str, temperature: float) -> BaseChatModel:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not set. Add it to .env or export it. "
        )
    return ChatOpenAI(model=model, temperature=temperature, api_key=api_key)


def _load_ollama(model: str, temperature: float) -> BaseChatModel:
    return ChatOllama(model=model, temperature=temperature)


def get_chat_model(
    task: TaskType | None = None,
    *,
    temperature: float = 0.0,
) -> BaseChatModel:
    """Return a chat model instance for the given task.

    Current routing rules:
    - If USE_OLLAMA is truthy, use a local Ollama model (default: llama3.2).
    - Otherwise prefer OpenAI (default: gpt-4o-mini).

    The ``task`` parameter is reserved for future routing logic
    (e.g. different models for code, math, QA, etc.).
    """
    use_ollama = os.environ.get("USE_OLLAMA", "").strip().lower() in ("1", "true", "yes")

    if use_ollama:
        model_name = os.environ.get("OLLAMA_MODEL", "llama3.2")
        return _load_ollama(model=model_name, temperature=temperature)

    model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    return _load_openai(model=model_name, temperature=temperature)

