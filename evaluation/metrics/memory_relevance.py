def calculate_memory_precision(
    retrieved_ids: list[str],
    relevant_ids: list[str],
) -> float:
    """
    Calculate precision of retrieved historical incidents.
    """

    if not isinstance(retrieved_ids, list):
        raise ValueError("retrieved_ids must be a list")

    if not isinstance(relevant_ids, list):
        raise ValueError("relevant_ids must be a list")

    if not retrieved_ids:
        raise ValueError(
            "retrieved_ids cannot be empty"
        )

    relevant_set = {
        item.strip()
        for item in relevant_ids
        if isinstance(item, str) and item.strip()
    }

    retrieved_set = {
        item.strip()
        for item in retrieved_ids
        if isinstance(item, str) and item.strip()
    }

    if not retrieved_set:
        return 0.0

    relevant_retrieved = (
        retrieved_set & relevant_set
    )

    return len(relevant_retrieved) / len(retrieved_set)
