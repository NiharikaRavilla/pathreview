# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/38

**Issue title:** Add an integration test that runs the full RAG pipeline against a mock LLM

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The RAG subsystem currently has unit tests for individual components, but it does not have an integration test that verifies the complete pipeline works across component boundaries. The new test will execute a query through retrieval, reranking, generation, and output parsing using deterministic test data and a mock LLM provider. It should verify that the components exchange data correctly while avoiding external LLM requests and nondeterministic responses. The primary change will be the addition of `tests/integration/test_rag_pipeline.py`.

**Selection notes:**
This issue is appropriate for me because it has a clearly identified test file and a defined end-to-end behavior. It requires understanding multiple related RAG components, which matches its Tier 2 classification, but it does not require changing the production architecture unless the test reveals an integration problem. The mock LLM should allow the test to run deterministically without making paid external API calls. I will review the existing retrieval, reranking, generation, parsing, and mock-provider interfaces before implementing the test.


**Branch name:** `test/38-rag-pipeline-integration`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/NiharikaRavilla/pathreview/commit/c918049
**Reproduction summary:**  
I confirmed that the repository does not yet have the full end-to-end RAG integration test described in the issue. I traced the relevant flow through retrieval, generation, and parsing, and the missing piece is a single deterministic test that connects those steps with a mock LLM.

**PLAN.md link:** (https://github.com/NiharikaRavilla/pathreview/blob/test/38-rag-pipeline-integration/PLAN.md)


**Blockers or open questions:**  
The main open question is how reranking should be handled in the test if it is implemented separately. I also want to confirm the cleanest way to mock the LLM client so the test stays stable in CI.