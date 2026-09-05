from evaluation.baselines.rule_based_analyzer import (
    analyze_incident,
)
from evaluation.dataset.incident_dataset import (
    INCIDENT_DATASET,
)
from evaluation.metrics.analysis_metrics import (
    accuracy,
)


def evaluate_baseline() -> dict:
    predictions = []
    expected = []
    results = []

    for item in INCIDENT_DATASET:
        incident_id = item["incident_id"]
        expected_root_cause = item["expected_root_cause"]

        analysis = analyze_incident(
            incident_id=incident_id
        )

        predicted_root_cause = analysis.root_cause

        predictions.append(
            predicted_root_cause
        )

        expected.append(
            expected_root_cause
        )

        results.append(
            {
                "incident_id": incident_id,
                "expected": expected_root_cause,
                "predicted": predicted_root_cause,
                "correct": (
                    predicted_root_cause
                    == expected_root_cause
                ),
            }
        )

    overall_accuracy = accuracy(
        predictions=predictions,
        expected=expected,
    )

    return {
        "num_incidents": len(INCIDENT_DATASET),
        "accuracy": overall_accuracy,
        "results": results,
    }


if __name__ == "__main__":
    evaluation = evaluate_baseline()

    print("\n=== Baseline Evaluation ===")

    print(
        f"Incidents: {evaluation['num_incidents']}"
    )

    print(
        f"Accuracy: {evaluation['accuracy']:.4f}"
    )

    print("\nIncident Results:")

    for result in evaluation["results"]:
        status = (
            "✓"
            if result["correct"]
            else "✗"
        )

        print(
            f"{result['incident_id']} "
            f"{status} "
            f"| Expected: {result['expected']} "
            f"| Predicted: {result['predicted']}"
        )
