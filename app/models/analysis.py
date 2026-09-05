from pydantic import BaseModel, Field


class IncidentAnalysis(BaseModel):
    """
    Structured result produced by the AI incident analyzer.
    """

    incident_id: str
    root_cause: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    evidence: list[str]
    recommendation: str
