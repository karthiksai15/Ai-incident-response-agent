import json
from pathlib import Path

from evaluation.metrics.evidence_relevance import (
    calculate_evidence_recall,
)
from evaluation.metrics.investigation_success import (
    calculate_investigation_success,
)
from evaluation.metrics.root_cause_accuracy import (
    calculate_root_cause_accuracy,
)


DATASET_PATH = Path(
    "evaluation/dataset/incidents.json"
)


def load_evaluation_dataset() -> list[dict]:
    with DATASET_PATH.open() as file:
        return json.load(file)


def evaluate_predictions(
    predictions: list[dict],
) -> dict:

    dataset = load_evaluation_dataset()

    expected_root_causes = [
        incident["expected_root_cause"]
        for incident in dataset
    ]

    predicted_root_causes = [
        prediction["root_cause"]
        for prediction in predictions
    ]

    root_cause_accuracy = (
        calculate_root_cause_accuracy(
            predicted=predicted_root_causes,
            expected=expected_root_causes,
        )
    )

    evidence_scores = []

    for prediction, incident in zip(
        predictions,
        dataset,
    ):
        evidence_score = calculate_evidence_recall(
            predicted=prediction["evidence"],
            expected=incident["expected_evidence"],
        )

        evidence_scores.append(evidence_score)

    evidence_recall = (
        sum(evidence_scores)
        / len(evidence_scores)
    )

    investigation_success = (
        calculate_investigation_success(
            root_cause_accuracy=root_cause_accuracy,
            evidence_recall=evidence_recall,
        )
    )

    return {
        "root_cause_accuracy": root_cause_accuracy,
        "evidence_recall": evidence_recall,
        "investigation_success": investigation_success,
    }


if __name__ == "__main__":

    predictions = [
        {
            "root_cause": "Database connection pool exhaustion",
            "evidence": [
                "Connection pool exhausted",
                "Failed to acquire JDBC connection",
            ],
        },
        {
            "root_cause": "Redis failure",
            "evidence": [
                "Redis unavailable",
                "Unable to connect to Redis",
            ],
        },
        {
            "root_cause": "High API latency",
            "evidence": [
                "Request latency exceeded threshold",
                "API response time increased",
            ],
        },
        {
            "root_cause": "Service crash",
            "evidence": [
                "Service process terminated",
                "Service crashed",
            ],
        },
    ]

    results = evaluate_predictions(predictions)

    print(json.dumps(results, indent=2))
