from app.agents.prompts import (
    build_incident_analysis_prompt,
)


def test_incident_analysis_prompt():

    prompt = build_incident_analysis_prompt(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[
            "Timeout waiting for database connection",
            "Connection pool exhausted",
        ],
        retrieved_knowledge=[
            "Database connection pool exhaustion occurs "
            "when all available connections are occupied."
        ],
    )

    assert "INC-001" in prompt
    assert "payment-service" in prompt
    assert "HIGH" in prompt
    assert "Connection pool exhausted" in prompt
    assert "database connection" in prompt.lower()
    assert "root cause" in prompt.lower()
    assert "recommendation" in prompt.lower()
