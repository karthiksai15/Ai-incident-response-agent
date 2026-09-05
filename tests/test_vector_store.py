import pytest

from app.rag.chunker import DocumentChunk
from app.rag.vector_store import VectorStore


def create_chunk(
    content: str,
    index: int,
) -> DocumentChunk:
    return DocumentChunk(
        content=content,
        source="test.md",
        chunk_index=index,
        metadata={
            "type": "runbook",
            "format": "markdown",
        },
    )


def create_embedding(value: float) -> list[float]:
    return [value] * 384


@pytest.fixture
def vector_store(tmp_path):
    return VectorStore(
        persist_directory=tmp_path / "chroma"
    )


def test_add_chunks(vector_store):
    chunks = [
        create_chunk(
            "Database connection pool exhausted",
            0,
        ),
        create_chunk(
            "Redis server unavailable",
            1,
        ),
    ]

    embeddings = [
        create_embedding(0.1),
        create_embedding(0.2),
    ]

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    assert vector_store.count() == 2


def test_search(vector_store):
    chunks = [
        create_chunk(
            "Database connection pool exhausted",
            0,
        ),
        create_chunk(
            "Redis server unavailable",
            1,
        ),
    ]

    embeddings = [
        create_embedding(0.1),
        create_embedding(0.9),
    ]

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    results = vector_store.search(
        query_embedding=create_embedding(0.1),
        top_k=1,
    )

    assert len(results) == 1
    assert (
        results[0].content
        == "Database connection pool exhausted"
    )


def test_search_returns_metadata(vector_store):
    chunks = [
        create_chunk(
            "Database connection pool exhausted",
            0,
        )
    ]

    embeddings = [
        create_embedding(0.1)
    ]

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    results = vector_store.search(
        query_embedding=create_embedding(0.1)
    )

    assert results[0].source == "test.md"
    assert results[0].chunk_index == 0
    assert results[0].metadata["type"] == "runbook"


def test_mismatched_chunks_and_embeddings(vector_store):
    chunks = [
        create_chunk("Test", 0)
    ]

    embeddings = []

    with pytest.raises(ValueError):
        vector_store.add_chunks(
            chunks,
            embeddings,
        )


def test_empty_chunks(vector_store):
    with pytest.raises(ValueError):
        vector_store.add_chunks(
            [],
            [],
        )


def test_empty_query(vector_store):
    with pytest.raises(ValueError):
        vector_store.search([])


def test_invalid_top_k(vector_store):
    with pytest.raises(ValueError):
        vector_store.search(
            query_embedding=create_embedding(0.1),
            top_k=0,
        )
