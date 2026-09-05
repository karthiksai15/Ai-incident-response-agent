from app.memory import retrieval


def test_retrieve_similar_incidents_filters_memories(monkeypatch):

    class FakeEmbedding:
        pass

    monkeypatch.setattr(
        retrieval,
        "create_memory_embedding",
        lambda text: [0.1, 0.2],
    )

    class FakeVectorStore:
        def search(self, embedding, top_k):
            assert embedding == [0.1, 0.2]
            assert top_k == 6

            return [
                {
                    "incident_id": "INC-001",
                    "document": "Database pool exhaustion",
                    "metadata": {
                        "service": "payment-service",
                        "severity": "HIGH",
                    },
                    "distance": 0.20,
                },
                {
                    "incident_id": "INC-002",
                    "document": "Redis failure",
                    "metadata": {
                        "service": "redis-service",
                        "severity": "HIGH",
                    },
                    "distance": 0.10,
                },
            ]

    monkeypatch.setattr(
        retrieval,
        "IncidentMemoryVectorStore",
        FakeVectorStore,
    )

    result = retrieval.retrieve_similar_incidents(
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Connection pool exhausted",
        ],
        top_k=3,
    )

    assert len(result) == 1
    assert result[0]["incident_id"] == "INC-001"
