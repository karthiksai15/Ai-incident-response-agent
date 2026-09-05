def unique_sources(
    retrieved_sources: list[str],
) -> list[str]:
    """
    Remove duplicate sources while preserving retrieval order.
    """

    seen = set()
    unique = []

    for source in retrieved_sources:
        if source not in seen:
            seen.add(source)
            unique.append(source)

    return unique
