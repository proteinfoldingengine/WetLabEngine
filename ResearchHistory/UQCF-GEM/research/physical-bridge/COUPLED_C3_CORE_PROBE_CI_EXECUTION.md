# C3 core-probe — algorithmically independent check and actual GitHub execution

Date: 2026-10-08.
Disposition: ALGORITHMICALLY INDEPENDENT BOUNDED CHECK PASSED. INDEPENDENT MATHEMATICAL REVIEW NOT OBTAINED. AUTOMATIC EVIDENCE-BRANCH PUBLICATION FAILED.

This is an execution report, not a scientific closeout or the post-acceptance publication audit. Same-assistant authorship remains explicit. The original theorem is unchanged; broader C3 and C4-C6 remain OPEN.

## Exact source and algorithmic difference

Verified starting parent: b10762d0f807d77cfa16cc1afe36acc91ccc1a95.
Prospective follow-on scope: 4d5a092b91f8e75e0277da802561585420be3d61.
Tests-first commit: 6a4ba75ca3a1ce332e6481e383bfecf6046f31b9.
Implemented checker / executed scientific commit: ad42d751f69c6fba7af585e6ba15b00941bc201f.
Frozen theorem proof: e7dc592d0f98121c7c232f33018a0a199c30ba8e, blob d619932c44d051f2a0c698365709d6f42e02f078.

The older replay's check_graph called build_graph again; its --check command called make_report again. Those are valid fresh reproductions, but they are not algorithmically independent verification. This follow-on adds verification/c3_core_probe_independent.py without importing or executing the producer in its verification path.

The new checker enumerates all full root-4 supports as integer masks, directly computes floor and hitting-number admissibility, builds the complete command relation and observation partition, and computes reachable sets of full states by relational images to a fixed point. Crucially, D is NOT in the reachability key and the target formula is NOT used to generate hidden possibilities. Only after constructing the entire observation graph does it propagate all possible maximum floor-deficit labels and compare the resulting exact labelled completion sets and canonical graph with the saved evidence.

An isolation test copies only the checker and evidence into an empty temporary directory and invokes Python with -I. A separate integration test runs the original producer in a subprocess, compares it with its saved report, and then passes that output through the independent checker. The original producer remains unchanged.

This establishes distinct algorithms, not distinct authorship or a fresh-context mathematical verdict.

## Actual RED evidence

Workflow: .github/workflows/uqcf-a12-self-contained.yml, unchanged blob 43b634e3efe6156c6e74974d2627ea74b7c425f9.
Run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37832509819
Attempt: 1. Numeric job: 113501157376.
Workflow and checked-out scientific SHA: 6a4ba75ca3a1ce332e6481e383bfecf6046f31b9.

The tests were committed before the checker existed. The actual GitHub contract step ran 18 tests: the 10 inherited A12 contracts passed; the 8 new C3 tests failed with the expected assertion, 'Independent checker not implemented (expected RED)'. The step exited 1. This is genuine failing execution, not a retrospectively written RED narrative. A local pre-implementation run also failed all eight new tests for the same assertion.

The workflow then failed to push its evidence branch. Artifact upload still succeeded; that is separate from durable repository publication.

Artifact ID: 11574560540. ZIP size: 11,406 bytes.
Downloaded ZIP SHA-256: c2b4645fa1c066b3c606c80f55a112e35d67cef5177edbff8644e8b978344312.
All five ZIP members were extracted and inspected. The downloaded ZIP digest matched the actual upload digest, and its context identifies the exact RED scientific SHA.

## Actual implemented execution

Run: https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/37832751396
Attempt: 1. Numeric job: 113501992613.
Workflow and checked-out scientific SHA: ad42d751f69c6fba7af585e6ba15b00941bc201f.
Environment: CPython 3.11.17, Ubuntu 22.04.5 runner. The report uses actual runner metadata, not the workflow's less-specific 3.11 selector as an exact version claim.

All 18 contract tests passed: eight new C3 contracts and ten inherited A12 contracts. The C3 result printed by the actual job is:

```json
{"deficit_used_to_generate_beliefs":false,"edges":[46,96],"full_assignments_enumerated":[64,128],"independent_mathematical_review":false,"nodes":[4,8],"scope":"fixed triangle; root-4 core edits; N=1,2 only","status":"ALGORITHMICALLY_INDEPENDENT_BOUNDED_PASS"}
```

The new tests reject omitted, duplicated and substituted graph records; altered spectator identities; wrong deficits; Boolean values substituted for integers; changed proof provenance, status or graph coverage; modified refuting examples; and duplicate JSON keys. They check all three restored-core history classes, the empty-core boundary, fresh producer output, and execution without the producer present.

The existing A12 bounded baseline also ran, without changing its implementation: 35,792 primary identities, 508 collective-family subsets, 33 fixture states, and 11 rejecting controls. Its fresh-process reproduction with another Python hash seed was byte-identical. These are A12 baseline counts, NOT additional C3 cases or a full inherited v16 stack replay.

The downloaded primary.json and reproduction.json were compared again locally and were exactly equal, each 10,057 bytes, SHA-256 954f0fb3f51c23ca67fa2958bddded7cb06eeb2d20c6c79814bdab0cf952bf87. Their scientific check digest is 650851cf5ad2f91ef2be7c60bd549039aa5e9daee79f9a6eedff21c003a9ea3c. The existing baseline emits overall_A12_gate=OPEN_PENDING_REPORTING_AUDIT; this run does not retroactively change earlier scoped dispositions.

## The workflow is NOT green overall

Both the RED and implemented runs failed at 'Preserve output on unique evidence-only branch'. The implemented run's tests, rejecting controls, primary execution, reproduction, comparison and artifact upload all succeeded, but its OVERALL GitHub conclusion is FAILURE.

The remote rejection in both actual logs was:

```text
Unable to determine if workflow can be created or updated due to timeout; `workflows` scope may be required.
```

This is the reported server error, not proof that permissions alone are the root cause. No workflow, token permission, branch protection, or authentication setting was altered to conceal or bypass this failure. Runner-local commits 0aa8a80 and 847dde8 appeared in logs, but their evidence branches were rejected; they are NOT represented as verified published commits.

The implemented run uploaded artifact ID 11574595760, ZIP size 18,798 bytes. The downloaded archive was hashed and checked against the API/upload digest:

    d04fda1889c362d3ed590cf953bf3e42bf9e0625a0bd4f8788589201ad244246

All 12 archive members were extracted. The context contains 179 source hashes, including the exact checker and test bytes below. Artifact upload, downloaded-byte verification, and permanent Git publication are distinct events.

## Source-byte checks

| Source | Git blob | SHA-256 |
|---|---|---|
| verification/c3_core_probe_independent.py | 806d504e3a902e8d7006cb3c4aba5c05b6b3744d | 67d8d92d5f2ab9f4f66eb44acf99d7d2aa97bc55217f0ef6f3762f7f63c09c70 |
| verification/test_c3_core_probe_independent.py | a44964a9ff213a51608b88ec6b8da7be23682aeb | 249c2f1650d8fc1f25b73686b56fce56abea043d73d6212659a9bf2475abe5d9 |

The local checker bytes matched immutable GitHub blob readback. Both local source files matched the hashes in the downloaded execution context. The RED context separately matched the pre-implementation test bytes.

## Reproduction

From ResearchHistory/UQCF-GEM/research/physical-bridge at the implemented scientific commit:

```sh
python -m unittest discover -s verification -p 'test_*.py' -v
python verification/c3_core_probe_independent.py COUPLED_C3_CORE_PROBE_REPLAY_EVIDENCE.json
python COUPLED_C3_CORE_PROBE_REPLAY.py > /tmp/c3-produced.json
python verification/c3_core_probe_independent.py /tmp/c3-produced.json
```

The checker itself needs only standard-library Python and the evidence JSON. The actual GitHub job already performed its isolated check and producer comparison. Local full-repository execution is not claimed: the local container could not resolve the public raw-file host, so repository execution and downloaded artifacts supply the exact-source evidence.

## Scientific meaning and unfulfilled gates

The exact native-history completion formula now survives a repository-executed algorithmic cross-check that reconstructs observations first and adds the proposed history statistic afterward. This removes a circular-verification risk without changing the mathematical theorem or adding observer information. It verifies the same 12 states and 142 transitions, rather than disguising extra passing-case counts as a new theorem.

The scope is still the fixed triangle and root-4-only edits with one or two spectator labels. No all-root or arbitrary-palette numerical certification follows. Algorithmic independence does not establish a separate author's mathematical acceptance.

Independent mathematical review, a subsequent independent publication audit, automatic durable evidence publication, full inherited-stack/post-merge requirements for any numbered-stage certification, native observer access, and operational progress are not closed by this report. No merge to main, new physical mechanism, force, geometry, energy, GR/ADM, continuum, or fundamental time is claimed. Broader C3 and C4-C6 remain OPEN.
