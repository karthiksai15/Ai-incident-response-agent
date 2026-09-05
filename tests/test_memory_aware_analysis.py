from app.agents import analysis_executor


def test_memory_aware_analysis_receives_all_sources(monkeypatch):

    captured = {}

    def fake_analyze_with_llm(prompt):
        captured["prompt"] = prompt

        return type(
            "Analysis",
            (),
            {
                "root_cause": "Database connection pool exhaustion",
                "confidence": 0.95,
                "evidence": [
                    "Connection pool exhausted"
                ],
                "recommendation": (
                    "Investigate database connections."
                ),
            },
        )()

    monkeypatch.setattr(
        analysis_executor,
        "analyze_with_llm",
        fake_analyze_with_llm,
    )

    result = analysis_executor.analyze_memory_rag_investigation(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Connection pool exhausted",
            "Database connection timeout",
        ],
        runbooks=[
            "Database connection pool exhaustion runbook."
        ],
        similar_incidents=[
            "Previous database pool exhaustion incident."
        ],
    )

    assert result.root_cause == (
        "Database connection pool exhaustion"
    )

    prompt = captured["prompt"]

    assert "CURRENT INCIDENT EVIDENCE" in prompt
    assert "Connection pool exhausted" in prompt

    assert "OFFICIAL RUNBOOK KNOWLEDGE" in prompt
    assert "Database connection pool exhaustion runbook." in prompt

    assert "SIMILAR HISTORICAL INCIDENTS" in prompt
    assert "Previous database pool exhaustion incident." in prompt
