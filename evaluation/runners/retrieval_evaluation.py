from app.rag.embeddings import EmbeddingModel
from app.rag.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store import VectorStore

from evaluation.dataset.retrieval_dataset import RETRIEVAL_DATASET
from evaluation.metrics.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
)
from evaluation.metrics.source_metrics import unique_sources


def evaluate_retrieval(
    top_k: int = 3,
) -> dict:
    """
    Evaluate retrieval at the document/source level.
    """

    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    pipeline = RetrievalPipeline(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    pipeline.build_knowledge_base()

    results = []

    for item in RETRIEVAL_DATASET:
        query = item["query"]
        expected_sources = item["expected_sources"]

        retrieved_chunks = pipeline.retrieve(
            query=query,
            top_k=top_k,
        )

        retrieved_sources = [
            chunk.source
            for chunk in retrieved_chunks
        ]

        retrieved_sources = unique_sources(
            retrieved_sources
        )

        evaluation_k = min(
            top_k,
            len(retrieved_sources),
        )

        recall = recall_at_k(
            retrieved_sources=retrieved_sources,
            expected_sources=expected_sources,
            k=evaluation_k,
        )

        precision = precision_at_k(
            retrieved_sources=retrieved_sources,
            expected_sources=expected_sources,
            k=evaluation_k,
        )

        results.append(
            {
                "query": query,
                "expected_sources": expected_sources,
                "retrieved_sources": retrieved_sources,
                "recall_at_k": recall,
                "precision_at_k": precision,
            }
        )

    average_recall = (
        sum(
            result["recall_at_k"]
            for result in results
        )
        / len(results)
    )

    average_precision = (
        sum(
            result["precision_at_k"]
            for result in results
        )
        / len(results)
    )

    return {
        "top_k": top_k,
        "num_queries": len(results),
        "average_recall_at_k": average_recall,
        "average_precision_at_k": average_precision,
        "results": results,
    }


if __name__ == "__main__":
    evaluation = evaluate_retrieval(top_k=3)

    print("\n=== Retrieval Evaluation ===")

    print(
        f"Queries: {evaluation['num_queries']}"
    )

    print(
        f"Recall@3: "
        f"{evaluation['average_recall_at_k']:.4f}"
    )

    print(
        f"Precision@3: "
        f"{evaluation['average_precision_at_k']:.4f}"
    )

    print("\nQuery Results:")

    for result in evaluation["results"]:
        print("\nQuery:")
        print(result["query"])

        print("Expected:")
        print(result["expected_sources"])

        print("Retrieved:")
        print(result["retrieved_sources"])

        print(
            f"Recall@3: "
            f"{result['recall_at_k']:.4f}"
        )

        print(
            f"Precision@3: "
            f"{result['precision_at_k']:.4f}"
        )
