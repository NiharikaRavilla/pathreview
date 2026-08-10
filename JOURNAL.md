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

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
I traced the implemented RAG flow and confirmed that the repository does not yet contain a standalone reranker; it is listed as a separate Tier 3 enhancement. I added `tests/integration/test_rag_pipeline.py`, which uses deterministic retrieval data and a mock LLM response to exercise hybrid retrieval, prompt construction, generation, JSON parsing, and source citations without contacting external services.

**Next steps:**
I will run the project checks, review the test against the contribution standards, open a pull request, and update this journal with the final PR link and verification results.

**Blockers:**
`make` is not installed in this Windows environment, so I ran the equivalent commands directly from `.venv`. The repository has pre-existing lint, formatting, and unit-test failures that are unrelated to this change; the new integration test passes.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/NiharikaRavilla/pathreview/pull/1

**Branch:** `test/38-rag-pipeline-integration`

**What you built:**
I added a deterministic integration test for the implemented RAG flow. It combines hybrid retrieval with a mocked LLM client, then verifies that the generated JSON is parsed into structured feedback and retains citations for the retrieved sources. The test does not call a live model, ChromaDB, or any other external service.

**Tests added or updated:**
I added `tests/integration/test_rag_pipeline.py`. It verifies the profile collection and query embedding passed to retrieval, confirms retrieved context is included in the LLM prompt, checks that all five review prompts are generated, and asserts the mock JSON response is parsed with its suggestion and source citations.

**Self-review confirmation:** [x] make check passes (no new failures; pre-existing lint and formatting failures documented)  [x] make test-unit passes (no new failures; 53 pre-existing unit-test failures documented)

**Draft PR feedback received from:** none

## Week 10 — Iteration & reflection

### Reviewer feedback

**Feedback received:** [ ] Yes  [x] No — still awaiting review

**Summary of feedback:**
No reviewer feedback came in. Reviewer feedback was not provided for this Summer 2026 cohort, so there were no comments to address on my PR.

**How you responded:**
No changes or replies were needed because no reviewer comments were received.

---

### Reflection

**What was harder than you expected?**
Understanding how the RAG pieces connect was harder than I expected. I had to read the retriever, generator, prompt templates, and output parser before I could write one useful integration test. I also had to separate existing project failures from problems caused by my own change.

**What did you learn about working in a large codebase?**
I learned that a change can look small but still depend on several parts of the codebase. In my own projects, I usually know where everything is. In this project, I needed to follow existing patterns, understand the test setup, and avoid changing code outside my issue.

**How did AI tools help — and where did they fall short?**
AI tools helped me quickly find related files, understand unfamiliar code, and draft the first version of the test. They could not decide the correct scope by themselves. I still needed to read the code and notice that the repository does not have a reranker yet, even though the issue mentioned one.

**What would you do differently if you started over?**
I would open a draft PR earlier and ask for feedback sooner. I would also first check all project commands and existing failures before starting implementation, so I could document the baseline more efficiently.

**What are you most proud of from this module?**
I am most proud that I added a test that does not depend on a real LLM or external services. The test is repeatable, free to run, and checks the connection between retrieval, generation, parsing, and citations.
