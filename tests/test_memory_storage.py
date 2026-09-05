from datetime import datetime

from app.memory.memory_service import store_incident_memory
from app.models.analysis import IncidentAnalysis


def test_store_incident_memory():
    analysis = IncidentAnalysis(
        incident_id="TEST-MEMORY-001",
        root_cause="Database connection pool exhaustion",
        confidence=0.9,
        evidence=[
            "Connection pool exhausted",
            "Failed to acquire JDBC connection",
        ],
        recommendation="Investigate database connections.",
    )

    memory = store_incident_memory(
        analysis=analysis,
        service="payment-service",
        severity="HIGH",
        investigation_notes=[
            "Incident context retrieved.",
            "Error evidence collected.",
        ],
    )

    assert memory.incident_id == "TEST-MEMORY-001"
    assert memory.root_cause == "Database connection pool exhaustion"
    assert memory.confidence == 0.9
    assert isinstance(memory.created_at, datetime)
