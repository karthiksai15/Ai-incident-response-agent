from app.rag.context_builder import RAGContextBuilder
from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore


def test_build_rag_context():
    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    pipeline.build_knowledge_base()

    builder = RAGContextBuilder(
        retrieval_pipeline=pipeline,
    )

    context = builder.build(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        top_k=3,
    )

    assert context.incident_id == "INC-001"
    assert context.service == "payment-service"
    assert context.severity == "HIGH"

    assert len(context.evidence) == 6

    assert len(context.retrieved_knowledge) == 3

    sources = [
        chunk.source
        for chunk in context.retrieved_knowledge
    ]

    assert "database_connection_pool.md" in sources
