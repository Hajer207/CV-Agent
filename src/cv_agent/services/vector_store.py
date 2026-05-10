import os
import chromadb
from openai import OpenAI
from cv_agent.config import OPENAI_API_KEY

_client = OpenAI(api_key=OPENAI_API_KEY)

_STORE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "vector_store")
_chroma = chromadb.PersistentClient(path=os.path.abspath(_STORE_PATH))
_collection = _chroma.get_or_create_collection("cvs")


def _embed(text: str) -> list[float]:
    response = _client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000],
    )
    return response.data[0].embedding


def add_cv(cv_id: str, cv_text: str, metadata: dict = None) -> None:
    """Store a CV embedding in the vector database."""
    _collection.upsert(
        ids=[cv_id],
        embeddings=[_embed(cv_text)],
        documents=[cv_text[:8000]],
        metadatas=[metadata or {}],
    )


def search_similar_cvs(query: str, n_results: int = 3) -> list[dict]:
    """Find CVs similar to the query text."""
    count = _collection.count()
    if count == 0:
        return []
    results = _collection.query(
        query_embeddings=[_embed(query)],
        n_results=min(n_results, count),
    )
    return [
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]


def get_rag_context(job_description: str, n_results: int = 3) -> str:
    """RAG: retrieve stored CVs relevant to a job description as context."""
    similar = search_similar_cvs(job_description, n_results)
    if not similar:
        return ""
    return "\n\n---\n\n".join(
        f"Reference Candidate {i + 1}:\n{cv['text']}"
        for i, cv in enumerate(similar)
    )
