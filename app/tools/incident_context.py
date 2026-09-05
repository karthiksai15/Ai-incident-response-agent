from pydantic import BaseModel

from app.core.config import LOG_DIRECTORY
from app.services.log_parser import parse_log_file
from app.tools.validation import (
    validate_incident_id,
    validate_service,
)


class IncidentContext(BaseModel):
    incident_id: str
    service: str
    severity: str
    status: str
    log_count: int


def get_incident_context(
    incident_id: str,
    service: str,
    severity: str,
) -> IncidentContext:
    """
    Get structured context about an incident.
    """

    incident_id = validate_incident_id(incident_id)
    service = validate_service(service)

    if not isinstance(severity, str):
        raise ValueError("severity must be a string")

    severity = severity.strip().upper()

    if severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError(
            "Invalid severity. Allowed values: "
            "LOW, MEDIUM, HIGH, CRITICAL"
        )

    log_file = LOG_DIRECTORY / f"{incident_id}.log"

    if not log_file.exists():
        raise FileNotFoundError(
            f"Log file not found for incident: {incident_id}"
        )

    logs = parse_log_file(str(log_file))

    return IncidentContext(
        incident_id=incident_id,
        service=service,
        severity=severity,
        status="OPEN",
        log_count=len(logs),
    )
