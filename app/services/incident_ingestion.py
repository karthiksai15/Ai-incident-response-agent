from pathlib import Path

from app.core.config import LOG_DIRECTORY
from app.models.incident import Incident
from app.services.log_parser import parse_log_file


def ingest_incident(
    incident_id: str,
    service: str,
    severity: str,
) -> Incident:

    log_file = LOG_DIRECTORY / f"{incident_id}.log"

    if not log_file.exists():
        raise FileNotFoundError(
            f"Log file not found for incident: {incident_id}"
        )

    logs = parse_log_file(str(log_file))

    return Incident(
        incident_id=incident_id,
        service=service,
        severity=severity,
        status="OPEN",
        logs=logs,
    )
