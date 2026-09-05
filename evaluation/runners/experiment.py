from datetime import datetime

from evaluation.runners.analysis_adapter import run_analysis
from evaluation.runners.configurations import (
    ExperimentConfiguration,
)


def run_single_experiment(
    incident: dict,
    configuration: ExperimentConfiguration,
    runbooks: list[str] | None = None,
    similar_incidents: list[str] | None = None,
) -> dict:
    """
    Run one evaluation incident under one configuration.
    """

    runbooks = runbooks or []
    similar_incidents = similar_incidents or []

    analysis = run_analysis(
        configuration=configuration,
        incident_id=incident["incident_id"],
        service=incident["service"],
        severity=incident["severity"],
        evidence=incident["logs"],
        runbooks=runbooks,
        similar_incidents=similar_incidents,
    )

    return {
        "incident_id": incident["incident_id"],
        "configuration": configuration.value,
        "root_cause": analysis.root_cause,
        "evidence": analysis.evidence,
        "confidence": analysis.confidence,
        "recommendation": analysis.recommendation,
        "timestamp": datetime.now().isoformat(),
    }
