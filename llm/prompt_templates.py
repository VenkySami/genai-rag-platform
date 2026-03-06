"""Central repository for LLM prompts used by the application."""

from langchain_core.prompts import PromptTemplate

rag_qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful AI assistant.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Answer clearly and concisely."
    ),
)

