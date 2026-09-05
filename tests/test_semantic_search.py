from app.rag.chunker import chunk_documents
from app.rag.document_loader import load_runbooks
from app.rag.embeddings import EmbeddingModel
from app.rag.semantic_search import SemanticSearch
from app.rag.vector_store import VectorStore


def create_search_system(tmp_path):
    documents = load_runbooks()

    chunks = chunk_documents(
        documents,
        chunk_size=800,
        overlap=100,
    )

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.embed_texts(
        [
            chunk.content
            for chunk in chunks
        ]
    )

    vector_store = VectorStore(
        persist_directory=tmp_path / "chroma"
    )

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    return SemanticSearch(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


def test_database_incident_search(tmp_path):
    search_system = create_search_system(tmp_path)

    results = search_system.search(
        "Why are database connections timing out?",
        top_k=3,
    )

    assert len(results) == 3

    sources = [
        result.source
        for result in results
    ]

    assert "database_connection_pool.md" in sources


def test_redis_incident_search(tmp_path):
    search_system = create_search_system(tmp_path)

    results = search_system.search(
        "Redis is unavailable and requests are failing",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "redis_failure.md" in sources


def test_api_latency_search(tmp_path):
    search_system = create_search_system(tmp_path)

    results = search_system.search(
        "The API response time has become very slow",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "high_api_latency.md" in sources


def test_service_crash_search(tmp_path):
    search_system = create_search_system(tmp_path)

    results = search_system.search(
        "The application service keeps restarting",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "service_crash.md" in sources


def test_empty_query(tmp_path):
    search_system = create_search_system(tmp_path)

    try:
        search_system.search("")
        assert False
    except ValueError:
        assert True
