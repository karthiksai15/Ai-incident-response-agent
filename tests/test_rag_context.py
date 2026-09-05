from app.rag.context import RAGContext


def test_rag_context_structure():
    context = RAGContext(
        incident_id="INC-001",
        service="payment-service",
        severity="HIGH",
        evidence=[],
        retrieved_knowledge=[],
    )

    assert context.incident_id == "INC-001"
    assert context.service == "payment-service"
    assert context.severity == "HIGH"
    assert context.evidence == []
    assert context.retrieved_knowledge == []
