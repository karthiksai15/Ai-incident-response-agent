from app.rag.context import RAGContext
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.services.incident_ingestion import ingest_incident
from app.tools.error_extraction import extract_errors


class RAGContextBuilder:
    """
    Builds a complete RAG context for an incident.

    The context combines:
    - incident metadata
    - log evidence
    - retrieved runbook knowledge
    """

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
    ):
        self.retrieval_pipeline = retrieval_pipeline

    def build(
        self,
        incident_id: str,
        service: str,
        severity: str,
        top_k: int = 3,
    ) -> RAGContext:
        """
        Build RAG context for an incident.
        """

        incident = ingest_incident(
            incident_id=incident_id,
            service=service,
            severity=severity,
        )

        evidence = extract_errors(
            incident_id=incident_id,
        )

        query_parts = [
            log.message
            for log in evidence
        ]

        query = " ".join(query_parts)

        retrieved_knowledge = (
            self.retrieval_pipeline.retrieve(
                query=query,
                top_k=top_k,
            )
        )

        return RAGContext(
            incident_id=incident.incident_id,
            service=incident.service,
            severity=incident.severity,
            evidence=evidence,
            retrieved_knowledge=retrieved_knowledge,
        )
