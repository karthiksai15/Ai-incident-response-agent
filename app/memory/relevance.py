def filter_relevant_memories(
    memories: list[dict],
    service: str,
    severity: str,
    max_distance: float = 0.60,
) -> list[dict]:
    """
    Filter retrieved historical incidents using simple
    deterministic relevance checks.

    A memory is considered relevant when:
    - it belongs to the same service
    - its vector distance is within the configured threshold

    Severity is used as supporting context but is not required
    to match because severity can legitimately differ between
    recurring incidents.
    """

    if not isinstance(memories, list):
        raise ValueError("memories must be a list")

    if not isinstance(service, str) or not service.strip():
        raise ValueError("service cannot be empty")

    if not isinstance(severity, str) or not severity.strip():
        raise ValueError("severity cannot be empty")

    relevant = []

    for memory in memories:
        if not isinstance(memory, dict):
            continue

        metadata = memory.get("metadata", {})

        if metadata.get("service") != service:
            continue

        distance = memory.get("distance")

        if distance is None:
            continue

        if distance <= max_distance:
            relevant.append(memory)

    return relevant
