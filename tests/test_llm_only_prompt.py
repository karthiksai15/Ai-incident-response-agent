from app.agents.prompts import (
    build_llm_only_analysis_prompt,
)


def test_llm_only_prompt():

    prompt = build_llm_only_analysis_prompt(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Timeout waiting for database connection",
            "Connection pool exhausted",
        ],
    )

    assert "INC-001" in prompt
    assert "payment-service" in prompt
    assert "HIGH" in prompt
    assert "Connection pool exhausted" in prompt

    assert "retrieved knowledge" not in prompt.lower()
    assert "root cause" in prompt.lower()
    assert "recommendation" in prompt.lower()
