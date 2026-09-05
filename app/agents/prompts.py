def build_incident_analysis_prompt(
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
    retrieved_knowledge: list[str],
) -> str:

    evidence_text = "\n".join(
        f"- {item}"
        for item in evidence
    )

    knowledge_text = "\n\n".join(
        retrieved_knowledge
    )

    return f"""
You are an AI incident investigation assistant.

Analyze a production incident using the provided
incident information, evidence, and retrieved
operational knowledge.

Your objectives are:

1. Identify the most likely root cause.

2. Distinguish the root cause from symptoms.

3. Use the provided evidence to support your conclusion.

4. Use retrieved knowledge when it is relevant.

5. Do not invent logs, metrics, or system behavior.

6. If the evidence is insufficient, clearly state that
   the root cause is uncertain.

7. Provide a practical recommendation for investigation
   or remediation.

INCIDENT

Incident ID: {incident_id}

Service: {service}

Severity: {severity}

EVIDENCE

{evidence_text}

RETRIEVED KNOWLEDGE

{knowledge_text}

Analyze the incident and provide:

Root Cause:

Confidence:

Evidence:

Recommendation:

""".strip()


def build_llm_only_analysis_prompt(
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
) -> str:

    evidence_text = "\n".join(
        f"- {item}"
        for item in evidence
    )

    return f"""
You are an AI incident investigation assistant.

Analyze the production incident using only the
incident information and evidence provided below.

Your objectives are:

1. Identify the most likely root cause.

2. Distinguish the root cause from symptoms.

3. Use the provided evidence to support your conclusion.

4. Do not invent logs, metrics, or system behavior.

5. If the evidence is insufficient, clearly state that
   the root cause is uncertain.

6. Provide a practical recommendation for investigation
   or remediation.

INCIDENT

Incident ID: {incident_id}

Service: {service}

Severity: {severity}

EVIDENCE

{evidence_text}

Do not assume that external operational knowledge
has been provided.

Analyze the incident and provide:

Root Cause:

Confidence:

Evidence:

Recommendation:

""".strip()


def build_memory_rag_analysis_prompt(
    incident_id: str,
    service: str,
    severity: str,
    evidence: list[str],
    runbooks: list[str],
    similar_incidents: list[str],
) -> str:

    evidence_text = "\n".join(
        f"- {item}"
        for item in evidence
    )

    runbook_text = "\n\n".join(
        runbooks
    ) if runbooks else "No relevant runbooks found."

    memory_text = "\n\n".join(
        similar_incidents
    ) if similar_incidents else "No similar incidents found."

    return f"""
You are an AI incident investigation assistant.

Analyze the production incident using three sources:

1. Current incident evidence
2. Official operational runbooks
3. Historical similar incidents

SOURCE PRIORITY

Current incident evidence is the primary source.

Runbooks provide documented operational guidance.

Historical incidents provide supporting historical
evidence and must not automatically be treated as the
cause of the current incident.

Your objectives are:

1. Identify the most likely root cause.

2. Distinguish the root cause from symptoms.

3. Use current incident evidence to support the conclusion.

4. Use runbooks when they are relevant to the incident.

5. Use similar historical incidents as supporting evidence.

6. Do not assume that a previous incident has the same
   root cause as the current incident.

7. Do not invent logs, metrics, system behavior, or
   historical events.

8. If the evidence is insufficient, clearly state that
   the root cause is uncertain.

9. Provide a practical recommendation for investigation
   or remediation.

CURRENT INCIDENT

Incident ID: {incident_id}

Service: {service}

Severity: {severity}

CURRENT INCIDENT EVIDENCE

{evidence_text}

OFFICIAL RUNBOOK KNOWLEDGE

{runbook_text}

SIMILAR HISTORICAL INCIDENTS

{memory_text}

Analyze the incident and provide:

Root Cause:

Confidence:

Evidence:

Recommendation:

""".strip()
