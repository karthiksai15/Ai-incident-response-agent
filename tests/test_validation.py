import pytest

from app.tools.validation import (
    validate_incident_id,
    validate_keyword,
    validate_log_level,
    validate_service,
)


def test_valid_incident_id():
    assert validate_incident_id("INC-001") == "INC-001"


def test_incident_id_is_trimmed():
    assert validate_incident_id("  INC-001  ") == "INC-001"


def test_invalid_incident_id():
    with pytest.raises(ValueError):
        validate_incident_id("invalid")


def test_path_traversal_incident_id():
    with pytest.raises(ValueError):
        validate_incident_id("../../file")


def test_empty_incident_id():
    with pytest.raises(ValueError):
        validate_incident_id("")


def test_valid_log_level():
    assert validate_log_level("error") == "ERROR"


def test_invalid_log_level():
    with pytest.raises(ValueError):
        validate_log_level("DEBUG")


def test_none_log_level():
    assert validate_log_level(None) is None


def test_valid_keyword():
    assert validate_keyword("connection") == "connection"


def test_empty_keyword():
    with pytest.raises(ValueError):
        validate_keyword("")


def test_valid_service():
    assert validate_service("payment-service") == "payment-service"


def test_empty_service():
    with pytest.raises(ValueError):
        validate_service("")
