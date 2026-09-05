from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore


def create_pipeline(tmp_path):
    embedding_model = EmbeddingModel()

    vector_store = VectorStore(
        persist_directory=tmp_path / "chroma"
    )

    return RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


def test_build_knowledge_base(tmp_path):
    pipeline = create_pipeline(tmp_path)

    count = pipeline.build_knowledge_base()

    assert count > 0
    assert pipeline.vector_store.count() == count


def test_retrieve_database_knowledge(tmp_path):
    pipeline = create_pipeline(tmp_path)

    pipeline.build_knowledge_base()

    results = pipeline.retrieve(
        "Why are database connections timing out?",
        top_k=3,
    )

    assert len(results) == 3

    sources = [
        result.source
        for result in results
    ]

    assert "database_connection_pool.md" in sources


def test_retrieve_redis_knowledge(tmp_path):
    pipeline = create_pipeline(tmp_path)

    pipeline.build_knowledge_base()

    results = pipeline.retrieve(
        "Redis is unavailable",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "redis_failure.md" in sources


def test_retrieve_latency_knowledge(tmp_path):
    pipeline = create_pipeline(tmp_path)

    pipeline.build_knowledge_base()

    results = pipeline.retrieve(
        "API response time is very slow",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "high_api_latency.md" in sources


def test_retrieve_crash_knowledge(tmp_path):
    pipeline = create_pipeline(tmp_path)

    pipeline.build_knowledge_base()

    results = pipeline.retrieve(
        "The service keeps restarting",
        top_k=3,
    )

    sources = [
        result.source
        for result in results
    ]

    assert "service_crash.md" in sources
