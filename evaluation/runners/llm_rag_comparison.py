from app.agents.prompts import (
    build_incident_analysis_prompt,
    build_llm_only_analysis_prompt,
)
from app.agents.structured_llm import analyze_with_llm
from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore
from app.services.incident_ingestion import ingest_incident
from app.tools.error_extraction import extract_errors


def run_llm_only(incident_id: str, service: str, severity: str):
    evidence_logs = extract_errors(
        incident_id=incident_id
    )

    evidence = [
        log.message
        for log in evidence_logs
    ]

    prompt = build_llm_only_analysis_prompt(
        incident_id=incident_id,
        service=service,
        severity=severity,
        evidence=evidence,
    )

    return analyze_with_llm(prompt)


def run_llm_with_rag(
    incident_id: str,
    service: str,
    severity: str,
):
    incident = ingest_incident(
        incident_id=incident_id,
        service=service,
        severity=severity,
    )

    evidence_logs = extract_errors(
        incident_id=incident_id
    )

    evidence = [
        log.message
        for log in evidence_logs
    ]

    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    query = " ".join(evidence)

    retrieved_chunks = pipeline.retrieve(
        query=query,
        top_k=3,
    )

    retrieved_knowledge = [
        chunk.content
        for chunk in retrieved_chunks
    ]

    prompt = build_incident_analysis_prompt(
        incident_id=incident.incident_id,
        service=incident.service,
        severity=incident.severity,
        evidence=evidence,
        retrieved_knowledge=retrieved_knowledge,
    )

    return analyze_with_llm(prompt)


if __name__ == "__main__":

    incident_id = "INC-001"
    service = "payment-service"
    severity = "HIGH"

    print("\n==============================")
    print("LLM-ONLY ANALYSIS")
    print("==============================")

    llm_only_result = run_llm_only(
        incident_id=incident_id,
        service=service,
        severity=severity,
    )

    print(f"\nRoot Cause: {llm_only_result.root_cause}")
    print(f"Confidence: {llm_only_result.confidence}")
    print(
        f"Recommendation: "
        f"{llm_only_result.recommendation}"
    )

    print("\n==============================")
    print("LLM + RAG ANALYSIS")
    print("==============================")

    rag_result = run_llm_with_rag(
        incident_id=incident_id,
        service=service,
        severity=severity,
    )

    print(f"\nRoot Cause: {rag_result.root_cause}")
    print(f"Confidence: {rag_result.confidence}")
    print(
        f"Recommendation: "
        f"{rag_result.recommendation}"
    )
