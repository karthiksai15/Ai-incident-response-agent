from evaluation.runners.configurations import (
    ExperimentConfiguration,
)

from app.agents.analysis_executor import (
    analyze_investigation,
    analyze_memory_rag_investigation,
)
from app.agents.prompts import (
    build_llm_only_analysis_prompt,
)
from app.agents.structured_llm import analyze_with_llm


def run_analysis(
    configuration: ExperimentConfiguration,
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
    runbooks: list[str] | None = None,
    similar_incidents: list[str] | None = None,
):
    """
    Run the appropriate analysis pipeline for an experiment.
    """

    if not isinstance(
        configuration,
        ExperimentConfiguration,
    ):
        raise ValueError(
            "Invalid experiment configuration"
        )

    runbooks = runbooks or []
    similar_incidents = similar_incidents or []

    if configuration == ExperimentConfiguration.LLM_ONLY:

        prompt = build_llm_only_analysis_prompt(
            incident_id=incident_id,
            service=service,
            severity=severity,
            evidence=evidence,
        )

        return analyze_with_llm(
            prompt=prompt
        )

    if configuration == ExperimentConfiguration.RAG:

        return analyze_investigation(
            incident_id=incident_id,
            service=service,
            severity=severity,
            evidence=evidence,
            retrieved_knowledge=runbooks,
        )

    if configuration == ExperimentConfiguration.RAG_MEMORY:

        return analyze_memory_rag_investigation(
            incident_id=incident_id,
            service=service,
            severity=severity,
            evidence=evidence,
            runbooks=runbooks,
            similar_incidents=similar_incidents,
        )

    raise ValueError(
        f"Unsupported configuration: {configuration}"
    )
