import pytest

from app.memory.safety import (
    sanitize_memory_text,
    validate_memory_content,
)


def test_valid_memory():
    assert validate_memory_content(
        {
            "root_cause": "Redis failure",
            "evidence": [
                "Redis unavailable"
            ],
        }
    )


def test_forbidden_secret():
    with pytest.raises(ValueError):
        validate_memory_content(
            {
                "api_key": "secret"
            }
        )


def test_sanitize_memory_text():
    assert (
        sanitize_memory_text(
            "  Redis failure  "
        )
        == "Redis failure"
    )
