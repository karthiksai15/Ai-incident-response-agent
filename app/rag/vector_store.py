from pathlib import Path

import chromadb
from pydantic import BaseModel

from app.core.config import BASE_DIR
from app.rag.chunker import DocumentChunk


CHROMA_DIRECTORY = BASE_DIR / "data" / "chroma"
COLLECTION_NAME = "incident_runbooks"


class RetrievedChunk(BaseModel):
    content: str
    source: str
    chunk_index: int
    metadata: dict[str, str]
    distance: float


class VectorStore:
    """
    Persistent ChromaDB vector store for incident runbook chunks.
    """

    def __init__(
        self,
        persist_directory: Path = CHROMA_DIRECTORY,
        collection_name: str = COLLECTION_NAME,
    ):
        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store chunks and their embeddings.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings"
            )

        if not chunks:
            raise ValueError(
                "chunks cannot be empty"
            )

        ids = [
            f"{chunk.source}:{chunk.chunk_index}"
            for chunk in chunks
        ]

        documents = [
            chunk.content
            for chunk in chunks
        ]

        metadatas = [
            {
                **chunk.metadata,
                "source": chunk.source,
                "chunk_index": str(chunk.chunk_index),
            }
            for chunk in chunks
        ]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def count(self) -> int:
        """
        Return the number of stored chunks.
        """

        return self.collection.count()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        """
        Search for the most similar chunks.
        """

        if not query_embedding:
            raise ValueError(
                "query_embedding cannot be empty"
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0"
            )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            retrieved_chunks.append(
                RetrievedChunk(
                    content=document,
                    source=str(metadata["source"]),
                    chunk_index=int(metadata["chunk_index"]),
                    metadata={
                        key: str(value)
                        for key, value in metadata.items()
                        if key not in {
                            "source",
                            "chunk_index",
                        }
                    },
                    distance=float(distance),
                )
            )

        return retrieved_chunks
