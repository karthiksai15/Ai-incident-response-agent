from app.memory.retrieval import retrieve_similar_incidents


def test_retrieve_similar_incidents_from_evidence():
    results = retrieve_similar_incidents(
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Database connection timeout",
            "Failed to acquire JDBC connection",
            "Connection pool exhausted",
        ],
        top_k=1,
    )

    assert results
    assert results[0]["incident_id"] == "TEST-MEMORY-VECTOR-001"
