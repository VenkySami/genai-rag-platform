import time
from typing import Any

from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from app.retrieval.hybrid_search import hybrid_retrieve
from llm.llm_router import get_chat_model
from llm.prompt_templates import rag_qa_prompt
from monitoring.tracing import trace_llm_call


class State(TypedDict, total=False):
    """State schema so LangGraph knows which keys nodes can write to."""
    query: str
    vector_store: Any
    vector: Any
    graph: Any
    answer: Any


def retrieve(state: State) -> dict:
    query = state["query"]
    vector_store = state.get("vector_store")
    if not vector_store:
        return {"vector": [], "graph": []}
    vector, graph = hybrid_retrieve(vector_store, query)
    return {"vector": vector, "graph": graph}


def generate(state: State) -> dict:
    """Generate an answer using retrieved vector/graph context and the LLM router."""
    context = f"{state.get('vector', '')}{state.get('graph', '')}"
    prompt = rag_qa_prompt.format(context=context, question=state["query"])

    llm = get_chat_model(task="rag_qa")
    started_at = time.perf_counter()
    answer = llm.invoke(prompt)
    finished_at = time.perf_counter()

    trace_llm_call(
        llm,
        prompt=prompt,
        response=answer,
        metadata={"task": "rag_qa", "query": state["query"]},
        started_at=started_at,
        finished_at=finished_at,
    )

    return {"answer": answer}


graph = StateGraph(State)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
app = graph.compile()

