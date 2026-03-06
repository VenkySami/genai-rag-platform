from pathlib import Path

from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from app.agents.langgraph_agent import app as agent  # noqa: E402
from app.vector_db.qdrant_client import get_vector_store  # noqa: E402

api = FastAPI()


def _message_to_content(msg):
    """Extract string content from LangChain message for JSON response."""
    if msg is None:
        return ""
    if hasattr(msg, "content"):
        return msg.content if isinstance(msg.content, str) else str(msg.content)
    return str(msg)


@api.post("/chat")
def chat(query: str = Body(..., embed=True)):
    try:
        vector_store = get_vector_store()  # connects to Qdrant "documents" collection
        result = agent.invoke({"query": query, "vector_store": vector_store})
        answer = result.get("answer")
        return {"answer": _message_to_content(answer), "query": query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
