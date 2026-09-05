from datetime import datetime

from pydantic import BaseModel, Field


class IncidentMemory(BaseModel):
    incident_id: str
    service: str
    severity: str

    root_cause: str
    confidence: float = Field(ge=0.0, le=1.0)

    evidence: list[str]
    recommendation: str

    investigation_notes: list[str]

    status: str
    created_at: datetime
