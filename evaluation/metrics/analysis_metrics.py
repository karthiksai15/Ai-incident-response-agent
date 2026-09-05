def accuracy(
    predictions: list[str],
    expected: list[str],
) -> float:
    if len(predictions) != len(expected):
        raise ValueError(
            "predictions and expected must have the same length"
        )

    if not expected:
        raise ValueError(
            "expected cannot be empty"
        )

    correct = sum(
        prediction == actual
        for prediction, actual
        in zip(predictions, expected)
    )

    return correct / len(expected)
