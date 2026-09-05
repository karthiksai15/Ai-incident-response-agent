from app.agents.rag_tool_prompt import build_rag_tool_prompt
from app.agents.tool_calling import (
    ask_gemini_with_tools,
    execute_tool_calls,
)
from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore


def main():

    incident_id = "INC-001"
    service = "payment-service"
    severity = "HIGH"

    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    query = """
    Database connection timeout.
    Connection pool exhausted.
    Failed to acquire JDBC connection.
    Payment request failed.
    """

    retrieved_chunks = pipeline.retrieve(
        query=query,
        top_k=3,
    )

    retrieved_knowledge = [
        chunk.content
        for chunk in retrieved_chunks
    ]

    prompt = build_rag_tool_prompt(
        incident_id=incident_id,
        service=service,
        severity=severity,
        retrieved_knowledge=retrieved_knowledge,
    )

    print("=== RAG + TOOL CALLING ===")

    chat, response = ask_gemini_with_tools(prompt)

    if response.function_calls:

        for function_call in response.function_calls:

            print(
                f"\nGemini selected tool: "
                f"{function_call.name}"
            )

            print(
                f"Arguments: "
                f"{function_call.args}"
            )

        final_response = execute_tool_calls(
            chat=chat,
            response=response,
        )

        print("\n=== FINAL ANALYSIS ===")
        print(final_response.text)

    else:

        print("\nGemini did not request a tool.")
        print(response.text)


if __name__ == "__main__":
    main()
