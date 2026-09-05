from app.agents import decision_executor


def build_state():
    return {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [
            "Connection pool exhausted",
            "Timeout waiting for database connection",
        ],
        "retrieved_knowledge": [],
        "similar_incidents": [],
        "root_cause": "",
        "confidence": 0.0,
        "recommendation": "",
        "investigation_notes": [],
        "current_goal": "retrieve_knowledge",
        "completed_goals": [],
        "next_action": "retrieve_knowledge",
        "tools_used": [],
        "iteration": 0,
        "investigation_complete": False,
    }


def test_memory_rag_knowledge_retrieval(monkeypatch):
    def fake_retrieve_combined_knowledge(
        service,
        severity,
        evidence,
        top_k=3,
    ):
        assert service == "payment-service"
        assert severity == "HIGH"
        assert evidence
        assert top_k == 3

        return type(
            "KnowledgeContext",
            (),
            {
                "runbooks": [
                    "Check database connection pool configuration."
                ],
                "similar_incidents": [
                    "Previous incident involved connection exhaustion."
                ],
            },
        )()

    monkeypatch.setattr(
        decision_executor,
        "retrieve_combined_knowledge",
        fake_retrieve_combined_knowledge,
    )

    result = decision_executor.execute_memory_rag_decision(
        build_state()
    )

    assert result["knowledge"] == [
        "Check database connection pool configuration."
    ]

    assert result["similar_incidents"] == [
        "Previous incident involved connection exhaustion."
    ]
