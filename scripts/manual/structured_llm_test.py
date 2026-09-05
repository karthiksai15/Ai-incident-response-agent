from app.agents.prompts import (
    build_incident_analysis_prompt,
)
from app.agents.structured_llm import (
    analyze_with_llm,
)


prompt = build_incident_analysis_prompt(
    incident_id="INC-001",
    service="payment-service",
    severity="HIGH",
    evidence=[
        "Timeout waiting for database connection",
        "Connection pool exhausted",
        "Failed to acquire JDBC connection",
        "Payment request failed",
    ],
    retrieved_knowledge=[
        (
            "Database connection pool exhaustion occurs when "
            "all available database connections are occupied. "
            "Investigate active connections, pool utilization, "
            "connection leaks, and pool configuration."
        )
    ],
)

analysis = analyze_with_llm(prompt)

print("\n=== Structured AI Analysis ===")
print(f"Incident ID: {analysis.incident_id}")
print(f"Root Cause: {analysis.root_cause}")
print(f"Confidence: {analysis.confidence}")
print("Evidence:")

for item in analysis.evidence:
    print(f"- {item}")

print(f"Recommendation: {analysis.recommendation}")
