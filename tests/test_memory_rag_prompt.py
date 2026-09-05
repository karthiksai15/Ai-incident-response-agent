from app.agents.prompts import build_memory_rag_analysis_prompt


def test_memory_rag_prompt_contains_all_sources():
    prompt = build_memory_rag_analysis_prompt(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Connection pool exhausted",
        ],
        runbooks=[
            "Check database connection pool configuration."
        ],
        similar_incidents=[
            "Previous incident caused by connection leakage."
        ],
    )

    assert "CURRENT INCIDENT EVIDENCE" in prompt
    assert "OFFICIAL RUNBOOK KNOWLEDGE" in prompt
    assert "SIMILAR HISTORICAL INCIDENTS" in prompt

    assert "Connection pool exhausted" in prompt
    assert "Check database connection pool configuration." in prompt
    assert "Previous incident caused by connection leakage." in prompt
