# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/38

**Issue title:** Add an integration test that runs the full RAG pipeline against a mock LLM

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The RAG subsystem currently has unit tests for individual components, but it does not have an integration test that verifies the complete pipeline works across component boundaries. The new test will execute a query through retrieval, reranking, generation, and output parsing using deterministic test data and a mock LLM provider. It should verify that the components exchange data correctly while avoiding external LLM requests and nondeterministic responses. The primary change will be the addition of `tests/integration/test_rag_pipeline.py`.


**Branch name:** `test/38-rag-pipeline-integration`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
