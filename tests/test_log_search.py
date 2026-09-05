import pytest

from app.tools.log_search import search_logs


def test_search_all_logs():
    logs = search_logs("INC-001")

    assert len(logs) == 8


def test_search_error_logs():
    logs = search_logs(
        "INC-001",
        level="ERROR",
    )

    assert len(logs) == 4

    assert all(
        log.level == "ERROR"
        for log in logs
    )


def test_search_keyword():
    logs = search_logs(
        "INC-001",
        keyword="connection",
    )

    assert len(logs) == 3

    assert all(
        "connection" in log.message.lower()
        for log in logs
    )


def test_search_error_keyword():
    logs = search_logs(
        "INC-001",
        level="ERROR",
        keyword="connection",
    )

    assert len(logs) == 3


def test_missing_incident():
    with pytest.raises(FileNotFoundError):
        search_logs("INC-999")
