from pathlib import Path

import pytest

from app.rag.document_loader import (
    Document,
    load_document,
    load_runbooks,
)


def test_load_single_document():
    file_path = (
        Path("knowledge/runbooks/database_connection_pool.md")
    )

    document = load_document(file_path)

    assert isinstance(document, Document)
    assert document.source == "database_connection_pool.md"
    assert len(document.content) > 0
    assert document.metadata["type"] == "runbook"
    assert document.metadata["format"] == "markdown"


def test_load_all_runbooks():
    documents = load_runbooks()

    assert len(documents) == 4

    sources = {
        document.source
        for document in documents
    }

    assert "database_connection_pool.md" in sources
    assert "redis_failure.md" in sources
    assert "high_api_latency.md" in sources
    assert "service_crash.md" in sources


def test_documents_have_content():
    documents = load_runbooks()

    assert all(
        document.content.strip()
        for document in documents
    )


def test_missing_document():
    with pytest.raises(FileNotFoundError):
        load_document(
            Path("knowledge/runbooks/missing.md")
        )


def test_invalid_document_format(tmp_path):
    file_path = tmp_path / "document.txt"

    file_path.write_text(
        "This is not Markdown."
    )

    with pytest.raises(ValueError):
        load_document(file_path)


def test_empty_document(tmp_path):
    file_path = tmp_path / "empty.md"

    file_path.write_text("")

    with pytest.raises(ValueError):
        load_document(file_path)
