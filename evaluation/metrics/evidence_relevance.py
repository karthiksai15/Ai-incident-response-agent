def calculate_evidence_recall(
    predicted: list[str],
    expected: list[str],
) -> float:
    """
    Calculate evidence recall using normalized exact matching.
    """

    if not isinstance(predicted, list):
        raise ValueError("predicted must be a list")

    if not isinstance(expected, list):
        raise ValueError("expected must be a list")

    if not expected:
        raise ValueError("expected cannot be empty")

    predicted_normalized = {
        item.strip().lower()
        for item in predicted
        if isinstance(item, str) and item.strip()
    }

    expected_normalized = {
        item.strip().lower()
        for item in expected
        if isinstance(item, str) and item.strip()
    }

    if not expected_normalized:
        raise ValueError("expected must contain valid evidence")

    relevant = (
        predicted_normalized
        & expected_normalized
    )

    return len(relevant) / len(expected_normalized)
