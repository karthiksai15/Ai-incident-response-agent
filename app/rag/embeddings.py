from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:
    """
    Wrapper around the sentence-transformers embedding model.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
    ):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """
        Convert one text string into an embedding vector.
        """

        if not isinstance(text, str):
            raise ValueError("text must be a string")

        if not text.strip():
            raise ValueError("text cannot be empty")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Convert multiple text strings into embedding vectors.
        """

        if not texts:
            raise ValueError("texts cannot be empty")

        if not all(
            isinstance(text, str) and text.strip()
            for text in texts
        ):
            raise ValueError(
                "texts must contain non-empty strings"
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        return embeddings.tolist()
