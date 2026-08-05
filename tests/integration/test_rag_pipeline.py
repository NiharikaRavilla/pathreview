"""Integration tests for the deterministic RAG review pipeline."""

from types import SimpleNamespace

import pytest

from rag.generator.review_generator import ReviewConfig, ReviewGenerator
from rag.retriever.hybrid import HybridRetriever
from rag.retriever.keyword_search import KeywordSearcher


class StubVectorStore:
    """Provide deterministic vector retrieval results without ChromaDB."""

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.queries: list[tuple[list[float], str, int]] = []

    def query(
        self, query_embedding: list[float], collection_name: str, n_results: int
    ) -> list[dict]:
        """Return fixed vector results for the requested profile collection."""
        self.queries.append((query_embedding, collection_name, n_results))
        return self.chunks

    def get_collection(self, collection_name: str) -> SimpleNamespace:
        """Return the stored chunks in the shape expected by HybridRetriever."""
        return SimpleNamespace(
            get=lambda include: {
                "ids": [chunk["id"] for chunk in self.chunks],
                "documents": [chunk["text"] for chunk in self.chunks],
                "metadatas": [chunk["metadata"] for chunk in self.chunks],
            }
        )


class MockCompletions:
    """Capture prompts and return parseable mock LLM responses."""

    def __init__(self):
        self.calls: list[dict] = []

    def create(self, **kwargs) -> SimpleNamespace:
        """Return a fixed JSON response that exercises the output parser."""
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"review": {"summary": "Strong Python portfolio", '
                        '"suggestions": ["Add deployment details"]}}'
                    )
                )
            ]
        )


@pytest.mark.integration
class TestRagPipeline:
    """Verify retrieved context reaches the mocked LLM and is parsed into feedback."""

    def test_retrieval_generation_and_parsing_with_mock_llm(self) -> None:
        """Run the implemented RAG pipeline without network or database services."""
        chunks = [
            {
                "id": "project-readme",
                "text": "Built a Python FastAPI service with PostgreSQL and Docker.",
                "metadata": {"source_id": "weather-api"},
                "score": 0.9,
            },
            {
                "id": "profile-readme",
                "text": "Maintains TypeScript frontend projects with clear documentation.",
                "metadata": {"source_id": "portfolio"},
                "score": 0.6,
            },
        ]
        vector_store = StubVectorStore(chunks)
        retriever = HybridRetriever(vector_store=vector_store, keyword_searcher=KeywordSearcher())
        retriever.keyword_searcher.index(chunks)

        retrieved_chunks = retriever.retrieve(
            query="Python service experience",
            profile_id="candidate-42",
            query_embedding=[0.1, 0.2, 0.3],
            max_chunks=2,
            min_score=0.0,
        )

        generator = ReviewGenerator(
            ReviewConfig(api_key="test-key", base_url="https://mock.local", model="mock-model")
        )
        completions = MockCompletions()
        generator.client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
        sections = generator.generate_full_review(
            profile_data={"github_username": "janedoe", "projects": [{"name": "Weather API"}]},
            retrieved_chunks=retrieved_chunks,
        )

        assert vector_store.queries == [([0.1, 0.2, 0.3], "profile_candidate-42", 4)]
        assert [chunk["id"] for chunk in retrieved_chunks] == [
            "project-readme",
            "profile-readme",
        ]
        assert len(completions.calls) == 5
        assert "Built a Python FastAPI service" in completions.calls[0]["messages"][1]["content"]
        assert len(sections) == 1
        assert sections[0].section_name == "review"
        assert "Strong Python portfolio" in sections[0].content
        assert sections[0].suggestions == ["Add deployment details"]
        assert "Sources: portfolio, weather-api" in sections[0].content
