import pytest

from app.rag.embeddings import EmbeddingModel


@pytest.fixture(scope="module")
def embedding_model():
    return EmbeddingModel()


def test_embed_text(embedding_model):
    embedding = embedding_model.embed_text(
        "Database connection pool exhausted"
    )

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(
        isinstance(value, float)
        for value in embedding
    )


def test_embedding_dimensions(embedding_model):
    embedding = embedding_model.embed_text(
        "Database connection pool exhausted"
    )

    assert len(embedding) == 384


def test_embed_multiple_texts(embedding_model):
    embeddings = embedding_model.embed_texts(
        [
            "Database connection pool exhausted",
            "Redis server unavailable",
            "High API latency",
        ]
    )

    assert len(embeddings) == 3
    assert all(
        len(embedding) == 384
        for embedding in embeddings
    )


def test_empty_text(embedding_model):
    with pytest.raises(ValueError):
        embedding_model.embed_text("")


def test_invalid_text(embedding_model):
    with pytest.raises(ValueError):
        embedding_model.embed_text(None)


def test_empty_text_list(embedding_model):
    with pytest.raises(ValueError):
        embedding_model.embed_texts([])


def test_semantically_similar_texts(embedding_model):
    first = embedding_model.embed_text(
        "Database connection pool exhausted"
    )

    second = embedding_model.embed_text(
        "Database connections are unavailable"
    )

    assert len(first) == len(second)
