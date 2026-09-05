import re


INCIDENT_ID_PATTERN = re.compile(r"^INC-\d{3,}$")

ALLOWED_LOG_LEVELS = {
    "INFO",
    "WARN",
    "ERROR",
}


def validate_incident_id(incident_id: str) -> str:
    """
    Validate an incident ID.

    Expected format:
        INC-001
        INC-123
    """

    if not isinstance(incident_id, str):
        raise ValueError("incident_id must be a string")

    incident_id = incident_id.strip()

    if not incident_id:
        raise ValueError("incident_id cannot be empty")

    if not INCIDENT_ID_PATTERN.fullmatch(incident_id):
        raise ValueError(
            "Invalid incident_id format. Expected format: INC-001"
        )

    return incident_id


def validate_log_level(level: str | None) -> str | None:
    """
    Validate an optional log level.
    """

    if level is None:
        return None

    if not isinstance(level, str):
        raise ValueError("level must be a string")

    level = level.strip().upper()

    if level not in ALLOWED_LOG_LEVELS:
        raise ValueError(
            "Invalid log level. Allowed values: INFO, WARN, ERROR"
        )

    return level


def validate_keyword(keyword: str | None) -> str | None:
    """
    Validate an optional keyword.
    """

    if keyword is None:
        return None

    if not isinstance(keyword, str):
        raise ValueError("keyword must be a string")

    keyword = keyword.strip()

    if not keyword:
        raise ValueError("keyword cannot be empty")

    if len(keyword) > 100:
        raise ValueError(
            "keyword cannot exceed 100 characters"
        )

    return keyword


def validate_service(service: str) -> str:
    """
    Validate a service name.
    """

    if not isinstance(service, str):
        raise ValueError("service must be a string")

    service = service.strip()

    if not service:
        raise ValueError("service cannot be empty")

    if len(service) > 100:
        raise ValueError(
            "service cannot exceed 100 characters"
        )

    return service
