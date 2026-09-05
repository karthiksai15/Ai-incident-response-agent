FORBIDDEN_MEMORY_FIELDS = {
    "prompt",
    "system_prompt",
    "api_key",
    "password",
    "token",
    "secret",
    "chain_of_thought",
}


def validate_memory_content(
    memory: dict,
) -> bool:
    if not isinstance(memory, dict):
        raise ValueError(
            "memory must be a dictionary"
        )

    for field in memory:
        if field.lower() in FORBIDDEN_MEMORY_FIELDS:
            raise ValueError(
                f"Forbidden memory field: {field}"
            )

    return True


def sanitize_memory_text(
    text: str,
) -> str:
    if not isinstance(text, str):
        raise ValueError(
            "memory text must be a string"
        )

    return text.strip()
