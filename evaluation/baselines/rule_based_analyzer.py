from app.models.analysis import IncidentAnalysis
from app.tools.error_extraction import extract_errors


RULES = {
    "database connection pool exhaustion": [
        "connection pool exhausted",
        "timeout waiting for database connection",
        "failed to acquire jdbc connection",
    ],
    "redis failure": [
        "redis connection refused",
        "redis timeout",
        "redis unavailable",
        "failed redis operation",
    ],
    "high api latency": [
        "latency exceeded",
        "response time",
        "request latency",
    ],
    "service crash": [
        "service unavailable",
        "process terminated",
        "container restart",
        "out-of-memory",
        "unhandled exception",
    ],
}


RECOMMENDATIONS = {
    "database connection pool exhaustion":
        "Investigate database connection pool utilization and active connections.",

    "redis failure":
        "Check Redis availability, latency, memory usage, and connectivity.",

    "high api latency":
        "Investigate slow dependencies, database latency, and service resource usage.",

    "service crash":
        "Investigate the final error before termination and check service health.",
}


def analyze_incident(
    incident_id: str,
) -> IncidentAnalysis:
    """
    Analyze an incident using deterministic rules.
    """

    errors = extract_errors(
        incident_id=incident_id,
    )

    messages = [
        error.message.lower()
        for error in errors
    ]

    scores = {}

    matched_evidence = {}

    for root_cause, keywords in RULES.items():
        matches = []

        for message in messages:
            for keyword in keywords:
                if keyword in message:
                    matches.append(message)
                    break

        scores[root_cause] = len(matches)
        matched_evidence[root_cause] = matches

    best_root_cause = max(
        scores,
        key=scores.get,
    )

    best_score = scores[best_root_cause]

    if best_score == 0:
        return IncidentAnalysis(
            incident_id=incident_id,
            root_cause="Unknown",
            confidence=0.0,
            evidence=[],
            recommendation="Manual investigation required.",
        )

    total_matches = sum(scores.values())

    confidence = (
        best_score / total_matches
        if total_matches > 0
        else 0.0
    )

    return IncidentAnalysis(
        incident_id=incident_id,
        root_cause=best_root_cause,
        confidence=confidence,
        evidence=matched_evidence[best_root_cause],
        recommendation=RECOMMENDATIONS[
            best_root_cause
        ],
    )
