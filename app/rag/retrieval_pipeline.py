from app.rag.chunker import chunk_documents
from app.rag.document_loader import load_runbooks
from app.rag.embeddings import EmbeddingModel
from app.rag.semantic_search import SemanticSearch
from app.rag.vector_store import RetrievedChunk, VectorStore


class RetrievalPipeline:
    """
    End-to-end pipeline for knowledge ingestion
    and semantic retrieval.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

        self.semantic_search = SemanticSearch(
            embedding_model=self.embedding_model,
            vector_store=self.vector_store,
        )

    def build_knowledge_base(self) -> int:
        """
        Load, chunk, embed, and store all runbooks.

        Returns the number of stored chunks.
        """

        documents = load_runbooks()

        chunks = chunk_documents(
            documents,
            chunk_size=800,
            overlap=100,
        )

        embeddings = self.embedding_model.embed_texts(
            [
                chunk.content
                for chunk in chunks
            ]
        )

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant knowledge for a query.
        """

        return self.semantic_search.search(
            query=query,
            top_k=top_k,
        )
