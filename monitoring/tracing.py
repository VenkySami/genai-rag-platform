import logging
from collections.abc import Mapping
from typing import Any

logger = logging.getLogger("genai_platform.llm")


def trace_llm_call(
    model: Any,
    *,
    prompt: str,
    response: Any,
    metadata: Mapping[str, Any] | None = None,
    started_at: float | None = None,
    finished_at: float | None = None,
) -> None:
    try:
        model_name = getattr(model, "model_name", None) or getattr(
            model, "model", model.__class__.__name__
        )
    except Exception:
        model_name = model.__class__.__name__

    latency_ms: float | None = None
    if started_at is not None and finished_at is not None:
        latency_ms = (finished_at - started_at) * 1000.0

    log_record = {
        "model_name": model_name,
        "prompt_preview": prompt[:200],
        "metadata": dict(metadata or {}),
        "latency_ms": latency_ms,
    }
    logger.info("LLM call", extra={"llm_trace": log_record})
