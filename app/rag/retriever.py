
from pathlib import Path

import numpy as np
from openai import OpenAI


class DocumentRetriever:
    def __init__(
        self,
        client: OpenAI | None = None,
        embedding_model: str = "text-embedding-3-small",
    ):
        self.client = client or OpenAI()
        self.embedding_model = embedding_model

        self.chunks: list[str] = []
        self.embeddings: np.ndarray | None = None

    def chunk_document(self, text: str) -> list[str]:
        sections = text.split("\n## ")

        chunks = []

        for section in sections:
            section = section.strip()

            if not section:
                continue

            # Skip a document title with no substantive content.
            if section.startswith("# ") and "\n" not in section:
                continue

            # Restore the heading removed by split().
            if not section.startswith("#"):
                section = "## " + section

            chunks.append(section)

        return chunks


    def embed_texts(self, texts: list[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=texts,
        )

        vectors = [
            item.embedding
            for item in sorted(
                response.data,
                key=lambda item: item.index,
            )
        ]

        return np.array(vectors, dtype=np.float32)

    def index_document(self, file_path: str) -> None:
        text = Path(file_path).read_text(encoding="utf-8")

        self.chunks = self.chunk_document(text)

        if not self.chunks:
            raise ValueError("Document contains no usable chunks")

        self.embeddings = self.embed_texts(self.chunks)

    def retrieve(
        self,
        question: str,
        top_k: int = 3,
    ) -> list[dict]:
        if self.embeddings is None:
            raise RuntimeError("Index a document before retrieval")

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        query_embedding = self.embed_texts([question])[0]

        document_norms = np.linalg.norm(
            self.embeddings,
            axis=1,
        )

        query_norm = np.linalg.norm(query_embedding)

        similarities = (
            self.embeddings @ query_embedding
        ) / (
            np.maximum(document_norms, 1e-12)
            * max(query_norm, 1e-12)
        )

        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            {
                "chunk_id": int(index),
                "text": self.chunks[index],
                "score": float(similarities[index]),
            }
            for index in top_indices
        ]
