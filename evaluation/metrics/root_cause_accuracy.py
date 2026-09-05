def calculate_root_cause_accuracy(
    predicted: list[str],
    expected: list[str],
) -> float:
    """
    Calculate root-cause accuracy using exact normalized matching.
    """

    if not isinstance(predicted, list):
        raise ValueError("predicted must be a list")

    if not isinstance(expected, list):
        raise ValueError("expected must be a list")

    if len(predicted) != len(expected):
        raise ValueError(
            "predicted and expected must have the same length"
        )

    if not expected:
        raise ValueError(
            "expected cannot be empty"
        )

    correct = 0

    for prediction, ground_truth in zip(
        predicted,
        expected,
    ):
        if not isinstance(prediction, str):
            continue

        if not isinstance(ground_truth, str):
            continue

        normalized_prediction = prediction.strip().lower()
        normalized_ground_truth = ground_truth.strip().lower()

        if normalized_prediction == normalized_ground_truth:
            correct += 1

    return correct / len(expected)
