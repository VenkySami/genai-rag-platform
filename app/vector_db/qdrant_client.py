from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, VectorParams

from app.ingestion.embeddings import embedding_model

client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "documents"
CONTENT_KEY = "page_content"
METADATA_KEY = "metadata"


class QdrantVectorStore:
    def __init__(self, client: QdrantClient, collection_name: str, embedding_model):
        self.client = client
        self.collection_name = collection_name
        self.embedding_model = embedding_model

    def similarity_search(self, query: str, k: int = 5):
        embedding = self.embedding_model.embed_query(query)
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=k,
            with_payload=True,
            with_vectors=False,
        )
        docs = []
        for point in response.points:
            payload = point.payload or {}
            content = payload.get(CONTENT_KEY, "")
            metadata = payload.get(METADATA_KEY, {})
            if not isinstance(metadata, dict):
                metadata = {}
            docs.append(Document(page_content=content, metadata=metadata))
        return docs


def create_vector_store(chunks):
    sample_embedding = embedding_model.embed_documents([" "])
    vector_size = len(sample_embedding[0])

    try:
        client.get_collection(collection_name=COLLECTION_NAME)
    except UnexpectedResponse as e:
        if e.status_code == 404:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        else:
            raise

    vector_store = Qdrant.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name=COLLECTION_NAME,
    )
    return vector_store


def get_vector_store():
    """Return a vector store for the existing collection (for search only)"""
    return QdrantVectorStore(client, COLLECTION_NAME, embedding_model)

