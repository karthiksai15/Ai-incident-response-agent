def calculate_investigation_success(
    root_cause_accuracy: float,
    evidence_recall: float,
) -> float:
    """
    Return 1.0 when both root-cause accuracy and
    evidence recall are perfect; otherwise return 0.0.
    """

    if not 0.0 <= root_cause_accuracy <= 1.0:
        raise ValueError(
            "root_cause_accuracy must be between 0 and 1"
        )

    if not 0.0 <= evidence_recall <= 1.0:
        raise ValueError(
            "evidence_recall must be between 0 and 1"
        )

    if (
        root_cause_accuracy == 1.0
        and evidence_recall == 1.0
    ):
        return 1.0

    return 0.0
