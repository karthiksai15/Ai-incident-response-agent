from app.rag.embeddings import EmbeddingModel
from app.rag.vector_store import RetrievedChunk, VectorStore


class SemanticSearch:
    """
    Performs semantic search over the incident knowledge base.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Convert the query into an embedding and search
        the vector database.
        """

        if not isinstance(query, str):
            raise ValueError("query must be a string")

        query = query.strip()

        if not query:
            raise ValueError("query cannot be empty")

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0"
            )

        query_embedding = (
            self.embedding_model.embed_text(query)
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )
