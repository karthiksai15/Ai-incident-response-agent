from pydantic import BaseModel

from app.models.incident import LogEntry
from app.rag.vector_store import RetrievedChunk


class RAGContext(BaseModel):
    """
    Combined incident evidence and retrieved knowledge
    used by the incident analysis system.
    """

    incident_id: str
    service: str
    severity: str

    evidence: list[LogEntry]
    retrieved_knowledge: list[RetrievedChunk]
