from app.memory.runbook_retrieval import retrieve_runbook_knowledge


def test_retrieve_runbook_knowledge():
    results = retrieve_runbook_knowledge(
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Database response time exceeded threshold",
            "Timeout waiting for database connection",
            "Connection pool exhausted",
        ],
        top_k=3,
    )

    assert results
    assert any(
        "connection" in result.lower()
        for result in results
    )
