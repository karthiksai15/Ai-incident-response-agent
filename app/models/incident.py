from datetime import datetime
from pydantic import BaseModel


class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    service: str
    message: str


class Incident(BaseModel):
    incident_id: str
    service: str
    severity: str
    status: str
    logs: list[LogEntry]
