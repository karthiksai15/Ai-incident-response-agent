from app.memory.relevance import filter_relevant_memories


def test_filter_relevant_memories():

    memories = [
        {
            "incident_id": "INC-OLD-001",
            "document": "Database connection pool exhaustion",
            "metadata": {
                "service": "payment-service",
                "severity": "MEDIUM",
            },
            "distance": 0.20,
        },
        {
            "incident_id": "INC-OLD-002",
            "document": "Redis connection failure",
            "metadata": {
                "service": "redis-service",
                "severity": "HIGH",
            },
            "distance": 0.10,
        },
        {
            "incident_id": "INC-OLD-003",
            "document": "Unrelated payment incident",
            "metadata": {
                "service": "payment-service",
                "severity": "HIGH",
            },
            "distance": 0.90,
        },
    ]

    result = filter_relevant_memories(
        memories=memories,
        service="payment-service",
        severity="HIGH",
        max_distance=0.60,
    )

    assert len(result) == 1
    assert result[0]["incident_id"] == "INC-OLD-001"
