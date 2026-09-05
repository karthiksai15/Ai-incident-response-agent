from app.graph.state import IncidentState
from app.services.incident_ingestion import ingest_incident


def load_incident(state: IncidentState):
    incident = ingest_incident(
        incident_id=state["incident_id"],
        service=state["service"],
        severity=state["severity"],
    )

    logs = [
        (
            f"{log.timestamp} | "
            f"{log.level} | "
            f"{log.service} | "
            f"{log.message}"
        )
        for log in incident.logs
    ]

    return {
        "logs": logs,
        "investigation_notes": [
            "Incident logs loaded successfully."
        ],
    }


from app.tools.error_extraction import extract_errors


def extract_evidence(state: IncidentState):
    errors = extract_errors(
        incident_id=state["incident_id"]
    )

    evidence = [
        error.message
        for error in errors
    ]

    return {
        "evidence": evidence,
        "investigation_notes": [
            "WARN and ERROR logs extracted as evidence."
        ],
    }


from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore


def retrieve_knowledge(state: IncidentState):
    embedding_model = EmbeddingModel()

    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    query = " ".join(state["evidence"])

    retrieved_chunks = pipeline.retrieve(
        query=query,
        top_k=3,
    )

    knowledge = [
        chunk.content
        for chunk in retrieved_chunks
    ]

    return {
        "retrieved_knowledge": knowledge,
        "investigation_notes": [
            "Relevant incident knowledge retrieved from runbooks."
        ],
    }

def manual_investigation(state: IncidentState):
    return {
        "investigation_notes": [
            "No WARN or ERROR evidence found. Manual investigation required."
        ],
    }
