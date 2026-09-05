from app.memory.knowledge_retrieval import retrieve_combined_knowledge


def test_retrieve_combined_knowledge():
    context = retrieve_combined_knowledge(
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Database connection timeout",
            "Failed to acquire JDBC connection",
            "Connection pool exhausted",
        ],
        top_k=3,
    )

    assert context.runbooks
    assert context.similar_incidents
