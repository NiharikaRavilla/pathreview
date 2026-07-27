**PLAN.md**

# Solution plan

**Issue:** [Add an integration test that runs the full RAG pipeline against a mock LLM](https://github.com/ascherj/pathreview/issues/38)

## **Understand**

The repo already has unit tests for separate RAG pieces, but it still needs one test that covers the full flow end to end. The expected result is a deterministic integration test that runs retrieval, reranking, generation, and parsing without calling a live LLM.

## **Map**

The main files involved are `tests/integration/test_rag_pipeline.py`, `rag/retriever/hybrid.py`, `rag/generator/review_generator.py`, and `rag/generator/output_parser.py`. I will also look for any existing mock helpers or shared test fixtures that can be reused.

## **Plan**

I will first trace how the current RAG components connect so I understand where the mock should go. Then I will add a focused integration test with fixed inputs and expected output. After that, I will verify that the test covers the complete pipeline path and adjust it if reranking or parsing needs a different setup.

## **Inputs & outputs**

The test should take a sample query and controlled document data as input. It should produce a parsed structured response from the pipeline and confirm that the final output matches the expected review format.

## **Risks & unknowns**

The biggest unknown is how reranking is handled in the current codebase and whether it is already implemented in a reusable way. Another risk is how the LLM client is wired, since it may need to be mocked carefully to keep the test deterministic.

## **Edge cases**

The test should handle empty or minimal retrieved context, unexpected LLM output formatting, and cases where the pipeline returns no strong matches. It should also avoid depending on external services or flaky model responses.
