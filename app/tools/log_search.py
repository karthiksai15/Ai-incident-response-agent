from app.core.config import LOG_DIRECTORY
from app.models.incident import LogEntry
from app.services.log_parser import parse_log_file
from app.tools.validation import (
    validate_incident_id,
    validate_keyword,
    validate_log_level,
)


def search_logs(
    incident_id: str,
    level: str | None = None,
    keyword: str | None = None,
) -> list[LogEntry]:
    """
    Search logs for a specific incident.
    """

    incident_id = validate_incident_id(incident_id)
    level = validate_log_level(level)
    keyword = validate_keyword(keyword)

    log_file = LOG_DIRECTORY / f"{incident_id}.log"

    if not log_file.exists():
        raise FileNotFoundError(
            f"Log file not found for incident: {incident_id}"
        )

    logs = parse_log_file(str(log_file))

    results = logs

    if level:
        results = [
            log
            for log in results
            if log.level.upper() == level
        ]

    if keyword:
        keyword_lower = keyword.lower()

        results = [
            log
            for log in results
            if keyword_lower in log.message.lower()
        ]

    return results
