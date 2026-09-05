import pytest

from app.tools.error_extraction import extract_errors


def test_extract_errors():
    logs = extract_errors("INC-001")

    assert len(logs) == 6


def test_extract_only_warn_and_error():
    logs = extract_errors("INC-001")

    assert all(
        log.level.upper() in {"WARN", "ERROR"}
        for log in logs
    )


def test_extract_contains_errors():
    logs = extract_errors("INC-001")

    error_logs = [
        log
        for log in logs
        if log.level.upper() == "ERROR"
    ]

    assert len(error_logs) == 4


def test_extract_contains_warnings():
    logs = extract_errors("INC-001")

    warning_logs = [
        log
        for log in logs
        if log.level.upper() == "WARN"
    ]

    assert len(warning_logs) == 2


def test_missing_incident():
    with pytest.raises(FileNotFoundError):
        extract_errors("INC-999")
