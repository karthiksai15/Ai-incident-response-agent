from datetime import datetime

from app.models.incident import LogEntry
from app.rag.context import RAGContext
from app.rag.context_formatter import format_rag_context
from app.rag.vector_store import RetrievedChunk


def test_format_rag_context():
    context = RAGContext(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[
            LogEntry(
                timestamp=datetime(
                    2026,
                    9,
                    5,
                    14,
                    40,
                    4,
                ),
                level="ERROR",
                service="payment-service",
                message="Timeout waiting for database connection",
            )
        ],
        retrieved_knowledge=[
            RetrievedChunk(
                content="Database connection pool is exhausted.",
                source="database_connection_pool.md",
                chunk_index=0,
                metadata={
                    "type": "runbook"
                },
                distance=0.2,
            )
        ],
    )

    formatted = format_rag_context(context)

    assert "INCIDENT" in formatted
    assert "INC-001" in formatted
    assert "payment-service" in formatted
    assert "HIGH" in formatted

    assert "EVIDENCE" in formatted
    assert "Timeout waiting for database connection" in formatted

    assert "RETRIEVED KNOWLEDGE" in formatted
    assert "database_connection_pool.md" in formatted
    assert "Database connection pool is exhausted." in formatted
