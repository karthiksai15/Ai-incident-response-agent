def recall_at_k(
    retrieved_sources: list[str],
    expected_sources: list[str],
    k: int,
) -> float:
    """
    Calculate Recall@K for a single query.
    """

    if k <= 0:
        raise ValueError(
            "k must be greater than 0"
        )

    if not expected_sources:
        raise ValueError(
            "expected_sources cannot be empty"
        )

    retrieved_top_k = set(
        retrieved_sources[:k]
    )

    expected = set(expected_sources)

    relevant_retrieved = (
        retrieved_top_k & expected
    )

    return (
        len(relevant_retrieved)
        / len(expected)
    )


def precision_at_k(
    retrieved_sources: list[str],
    expected_sources: list[str],
    k: int,
) -> float:
    """
    Calculate Precision@K for a single query.
    """

    if k <= 0:
        raise ValueError(
            "k must be greater than 0"
        )

    retrieved_top_k = retrieved_sources[:k]

    if not retrieved_top_k:
        return 0.0

    expected = set(expected_sources)

    relevant_retrieved = [
        source
        for source in retrieved_top_k
        if source in expected
    ]

    return (
        len(relevant_retrieved)
        / len(retrieved_top_k)
    )
