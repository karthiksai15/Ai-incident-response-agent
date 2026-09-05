from app.memory.embedding import create_memory_embedding
from app.memory.vector_store import IncidentMemoryVectorStore


def test_memory_vector_search():
    text = (
        "Service: payment-service\n"
        "Severity: HIGH\n"
        "Root Cause: Database connection pool exhaustion\n"
        "Evidence: Connection pool exhausted JDBC connection timeout"
    )

    embedding = create_memory_embedding(text)

    store = IncidentMemoryVectorStore()

    store.add_memory(
        incident_id="TEST-MEMORY-VECTOR-001",
        text=text,
        embedding=embedding,
        metadata={
            "service": "payment-service",
            "severity": "HIGH",
            "status": "RESOLVED",
        },
    )

    results = store.search(
        embedding=embedding,
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["incident_id"] == "TEST-MEMORY-VECTOR-001"
