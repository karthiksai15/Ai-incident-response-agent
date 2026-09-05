import pytest

from app.rag.chunker import (
    DocumentChunk,
    chunk_document,
    chunk_documents,
)
from app.rag.document_loader import Document


def create_test_document(content: str) -> Document:
    return Document(
        content=content,
        source="test.md",
        metadata={
            "type": "runbook",
            "format": "markdown",
        },
    )


def test_chunk_document():
    document = create_test_document(
        "A" * 2000
    )

    chunks = chunk_document(
        document,
        chunk_size=800,
        overlap=100,
    )

    assert len(chunks) > 1
    assert all(
        isinstance(chunk, DocumentChunk)
        for chunk in chunks
    )


def test_chunk_size():
    document = create_test_document(
        "A" * 2000
    )

    chunks = chunk_document(
        document,
        chunk_size=800,
        overlap=100,
    )

    assert all(
        len(chunk.content) <= 800
        for chunk in chunks
    )


def test_chunk_source():
    document = create_test_document(
        "A" * 2000
    )

    chunks = chunk_document(document)

    assert all(
        chunk.source == "test.md"
        for chunk in chunks
    )


def test_chunk_indexes():
    document = create_test_document(
        "A" * 2000
    )

    chunks = chunk_document(document)

    indexes = [
        chunk.chunk_index
        for chunk in chunks
    ]

    assert indexes == list(range(len(chunks)))


def test_chunk_metadata():
    document = create_test_document(
        "A" * 2000
    )

    chunks = chunk_document(document)

    assert all(
        chunk.metadata["type"] == "runbook"
        for chunk in chunks
    )


def test_multiple_documents():
    documents = [
        create_test_document("A" * 1000),
        create_test_document("B" * 1000),
    ]

    chunks = chunk_documents(documents)

    assert len(chunks) >= 4


def test_invalid_chunk_size():
    document = create_test_document("test")

    with pytest.raises(ValueError):
        chunk_document(
            document,
            chunk_size=0,
        )


def test_invalid_overlap():
    document = create_test_document("test")

    with pytest.raises(ValueError):
        chunk_document(
            document,
            chunk_size=100,
            overlap=100,
        )
