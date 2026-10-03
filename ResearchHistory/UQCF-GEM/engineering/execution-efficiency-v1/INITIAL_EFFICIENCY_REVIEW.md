# Independent engineering review — execution efficiency v1

**Reviewer:** independent Codex agent `/root/a11_x6_review`
**Candidate:** `38e54c69404dfad7e5b302584122eb65c9cd4cac`
**Decision:** **REVISE — one minor prospective-binding inconsistency.** No unsupported speedup claim or substantive baseline error found.

## Required correction

PERFORMANCE_CONTRACT.md says:

> Freeze before launch: campaign run ID and attempt … expected job IDs/stage names

GitHub assigns run and job IDs during instantiation. The pipeline correctly says to bind exact upstream job IDs **when instantiated**.

Make the contract consistent:
- Freeze caller-controlled immutable request, source/helper/protocol bindings, workload/stage identities, publication target and budgets before launch.
- Bind platform-assigned run/attempt/job identities immutably when instantiated, before downstream readiness is accepted.
- A conflicting rebinding must reject.

This does not authorize execution or weaken any evidence gate.

## Independent source and evidence checks

I independently fetched all eight candidate files and compared the candidate with certified base 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. GitHub reports one added commit and exactly the eight packet files. No scientific source, workflow, implementation or certificate changed.

I independently queried live run metadata and attempt-1 paginated job endpoints for all nine historical runs:
- Campaigns: 37059520424, 37069226242, 37075311542.
- Aggregation: 37063427057, 37073565129, 37084743074.
- Preservation: 37069220208, 37074296257, 37085148218.

All report attempt one. Returned counts exhaust pagination: campaign job counts 10,11,11, and one job per aggregation/preservation run. Stored run identity/status/timestamps, job identity/timestamps, and all stored step summaries match independent API retrieval.

All nine workflow bodies independently fetched at their exact run SHAs match the packet. All fourteen recorded provenance-source bodies independently fetched at their recorded SHAs also match.

## Independent arithmetic

| Campaign | Creation → final job | Runner-job spans | Duration-weighted critical path |
| --- | ---: | ---: | ---: |
| Primary | 2083s | 5595s | 2076s |
| Reproduction | 2803s | 5938s | 2793s |
| Actual merge | 2922s | 5967s | 2912s |

Every recorded metric for all nine runs independently recalculates exactly.

The actual-merge facts are correct:
- Domain 7: 23:04:34Z → 23:34:15Z =1781s,29m41s.
- Inherited: 23:34:18Z → 23:47:36Z =798s,13m18s.
- Final computation → aggregation creation: 23:47:36Z → 01:05:33Z =4677s,77m57s.
- Aggregation span248s; preservation span92s.
- Campaign creation → preservation completion8062s,134m22s.

The final-computation-to-aggregation interval is correctly distinguished from runner queue. Its cause is unavailable. Run updated_at is correctly retained as a separate proxy.

Source needs establishes the campaign graph: primary development → eight domains → inherited; reproduction/actual merge add route → development. Critical paths exclude queue and interjob gaps; runner spans are not CPU attribution.

## Design assessment

Apart from the binding wording above, the bounded design is coherent:
- Development gates scientific work.
- Complete inherited work may overlap the full eight-domain matrix under seven domain workers plus one inherited worker, total eight.
- Every domain remains required; changing concurrency does not establish net speedup.
- Aggregation checks exact upstream run/attempt/job identities and complete successful outcomes.
- A separate terminal audit retains whole-run success requirements, avoiding a circular in-run prerequisite.
- Duplicate events use run/attempt/stage identity, immutable input digests and compare-and-set revisions.
- Failed, skipped, cancelled, missing or unfinished work cannot pass.
- Assertion failures cannot automatically retry.
- Unknown publication outcomes require readback before any bounded resume.
- Scientific/workflow/protocol/helper/source bindings remain pinned.
- Artifacts remain untrusted data; privileged publication uses the approved helper, exact publication prefix, absent-ref lease and committed-byte readback.
- Existing scientific resource and dependency pins remain preserved.
- A3 prepared-universe distribution is deferred; phase costs are unmeasured.
- The tiny end-to-end success/refusal fixture is expressly designed, not executed.
- The receipt schema is expressly structural; semantic invariants are not represented as already validated.

No new code, workflow, test or scientific execution was performed in this review. Local operations handled source bytes, hashes and observational timestamp arithmetic only.

## Exact candidate hashes

| File | Bytes | SHA-256 | Git blob |
| --- | ---: | --- | --- |
| README.md | 2698 | 5049d457d4aaeea8f759e69490aaf17c662f54ddc2bdf652ca085f892c7c9826 | b6744611882c217793f979a79b0a290d93e6b0f2 |
| BASELINE.md | 5945 | 44f48d3996ba2da603a0f900551711f184b9a28bb64177b48d14cec3b6a8df24 | e320561053f1d663c15ae4bfc6100f9dc6e5085a |
| timing_baseline.json | 327269 | a529b78d6d1403e6b0fa48e13214779c4d46e47054ad1e119805453714b169e1 | 2473eb55efc24c22436d17ea43bf7fb6ef399461 |
| PERFORMANCE_CONTRACT.md | 3640 | fe9ced5f59bb252d7adf1a60cb715e7b77bdb114db2f2f0b19ee5393f59b7d61 | c44e3fcdb259416f10eb9490db89657c448eccf9 |
| DECISION_LEDGER.md | 3020 | 474643e17266362d8f6f15c974f8f0618e4b47fc2a0c37915b0e45d0505e70b4 | 0d41496b18ed5b3a957c3ee48216591def77368a |
| PIPELINE_DESIGN.md | 5160 | a4dd5ba8dbb0e40b0aeb1252b6b7da30edc22373918ece86d93ce0a50bfa8acb | 83e4a4bf9fb29b26b58161571d125fb402ce6b69 |
| RUN_STATE_SCHEMA.json | 12057 | 93f96f578c077d5b5d12ae5bbbf561d346ad32ac41b1c5a3a93cb3fff0012349 | 58e918bfd03e5b6bdc500f88977cdfb98bfad4a6 |
| VALIDATION_DESIGN.md | 4999 | 654c583d14c376cee614f38c05fc10681da34b7450e1cf7ac7dba58669ec3f86 | 47fbf0da910e6617cdfc0db705b3d9f9df9791d0 |

These exact UTF-8 bytes independently reproduce the candidate's Git blob identities.

**Completion boundary:** after the minor correction and exact-source readback review, this packet can complete the promised observational baseline, bounded proposal and validation design. Engineering implementation, fixture execution, controlled performance evaluation and performance acceptance remain unstarted. No measured speedup or numerical certification follows from accepting these documents.
