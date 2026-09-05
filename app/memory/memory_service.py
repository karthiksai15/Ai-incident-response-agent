from datetime import datetime

from app.memory.embedding import (
    create_memory_embedding,
    create_memory_text,
)
from app.memory.repository import save_memory
from app.memory.vector_store import IncidentMemoryVectorStore
from app.models.analysis import IncidentAnalysis
from app.models.memory import IncidentMemory


def store_incident_memory(
    analysis: IncidentAnalysis,
    service: str,
    severity: str,
    investigation_notes: list[str],
    status: str = "RESOLVED",
) -> IncidentMemory:

    memory = IncidentMemory(
        incident_id=analysis.incident_id,
        service=service,
        severity=severity,
        root_cause=analysis.root_cause,
        confidence=analysis.confidence,
        evidence=analysis.evidence,
        recommendation=analysis.recommendation,
        investigation_notes=investigation_notes,
        status=status,
        created_at=datetime.now(),
    )

    save_memory(memory)

    memory_text = create_memory_text(
        service=memory.service,
        severity=memory.severity,
        root_cause=memory.root_cause,
        evidence=memory.evidence,
    )

    embedding = create_memory_embedding(memory_text)

    vector_store = IncidentMemoryVectorStore()

    vector_store.add_memory(
        incident_id=memory.incident_id,
        text=memory_text,
        embedding=embedding,
        metadata={
            "service": memory.service,
            "severity": memory.severity,
            "status": memory.status,
        },
    )

    return memory
