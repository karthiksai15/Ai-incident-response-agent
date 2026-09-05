from app.memory import knowledge_retrieval


def test_combined_knowledge_uses_relevant_memory(monkeypatch):

    monkeypatch.setattr(
        knowledge_retrieval,
        "retrieve_similar_incidents",
        lambda **kwargs: [
            {
                "incident_id": "INC-HISTORY-001",
                "document": "Previous database pool exhaustion incident.",
                "metadata": {
                    "service": "payment-service",
                    "severity": "HIGH",
                },
                "distance": 0.20,
            }
        ],
    )

    monkeypatch.setattr(
        knowledge_retrieval,
        "retrieve_runbook_knowledge",
        lambda **kwargs: [
            "Database connection pool exhaustion runbook."
        ],
    )

    result = knowledge_retrieval.retrieve_combined_knowledge(
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Connection pool exhausted",
            "Database connection timeout",
        ],
        top_k=3,
    )

    assert result.runbooks == [
        "Database connection pool exhaustion runbook."
    ]

    assert result.similar_incidents == [
        "Previous database pool exhaustion incident."
    ]
