from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore


def retrieve_incident_knowledge(
    query: str,
    top_k: int = 3,
) -> list[str]:
    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    results = pipeline.retrieve(
        query=query,
        top_k=top_k,
    )

    return [
        result.content
        for result in results
    ]
