# C3 core-probe replay — algorithmically independent check scope

Date: 2026-10-08.
Verified integrated parent: b10762d0f807d77cfa16cc1afe36acc91ccc1a95.
Status: VERIFICATION FOLLOW-ON, not independent mathematical acceptance or scientific closeout.

## Why this work is needed

The published replay's check_graph calls build_graph again, and its --check path calls make_report again. This is fresh reproduction but not an algorithmically independent verifier. The earlier reports correctly withhold a separate mathematical-review verdict; this work must preserve that distinction.

Original theorem scope: 4e0cb8c68c807265fb48652b1f990a18d4a43a2c.
Original theorem proof: e7dc592d0f98121c7c232f33018a0a199c30ba8e, blob d619932c44d051f2a0c698365709d6f42e02f078.
Published producer: 4374f342a12c73bed8bffc7dad94e77316fbe14b, blob fdb103d73dfcdba0350acb710c18b46414b061f7.
Published bounded evidence: 93f2a284f5b9fb423f064fd4f86a7f7467787269, blob 857f2d69a26d758455850d20467c08687c12a2ee.

## Frozen scope and known findings

No enlargement of the prior slice: fixed first roots {a,b},{b,c},{a,c}; root 4 starts with core {d,e}; all ten signed core commands; immutable spectators only at root 4; T={u} or {u,v}; floor 2; protected band 3<=tau<=4; legal requests may reject. Existing known outputs are 4/46 and 8/96 retained nodes/command-outcome edges. These are known findings, not new blinded predictions. The original arbitrary-palette/all-root proof remains unchanged and is not certified by this finite check.

## Independent implementation

Add verification/c3_core_probe_independent.py without importing, executing, copying functions from, or invoking the producer as part of verification. Represent full supports as integer bit masks. Enumerate the entire admissible full-state and command relation by exhaustive bit-mask hitting-set tests. Form observation-equivalence blocks and compute reachable sets of possible full states by relational images to a fixed point. Do not include D in the reachability state or use the claimed threshold formula to generate hidden possibilities.

Only after the entire observational graph is constructed, propagate every attainable maximum floor-deficit value along its edges. Require a unique D for each resulting knowledge state; then compare the reconstructed exact labelled hidden subsets and canonical command/outcome graph to the saved report. Compare the threshold formula only after construction. This differs from the producer's string/set, D-augmented breadth-first traversal.

Validate graph coverage, duplicate/missing/substituted records, false values, wrong source/status metadata, Boolean-for-integer substitutions and malformed JSON. Retain all spectator identities. Reconstruct expected coverage rather than trusting record counts. Preserve the producer's four refuting examples and check their contents; do not interpret their presence as a separate review.

## Test and repository execution plan

Publish tests first under the existing verification directory, execute and preserve an actual RED result before adding the checker. Tests must cover successful verification, all three restored-history classes, missing and duplicate nodes/edges, changed same-cardinality identity, wrong deficit and metadata, and a fresh producer subprocess compared to the independent checker. The checker itself must work in an isolated directory containing no producer.

Use the existing .github/workflows/uqcf-a12-self-contained.yml without rewriting its scientific harness. Its path trigger includes verification/** and preserves actual logs/context on a unique evidence branch and as an artifact. Inspect the exact RED and GREEN jobs, record workflow/scientific SHAs, and read back durable evidence. Existing A12 verification running with this job is a bounded baseline replay, not the full inherited v16 stack. Record missing execution or artifacts honestly; an upload receipt alone is not a digest audit.

Bounded resource limits: standard-library Python only; at most 128 full root-4 core/spectator assignments per palette; no random sampling; no unbounded campaign; fixed-point termination within the finite powerset construction; test process timeout 60 seconds. Existing workflow timeout/budget remain unchanged.

## Publication and acceptance boundary

Publish actual source, tests, run provenance, and an additive continuation-index update. Do not rewrite historical proof/audits, create an external-AI dependency, invent a review job, merge to main, or mark this theorem CLOSED/CERTIFIED. Same-assistant authorship remains disclosed even if the algorithms differ. Separate independent mathematical review, its subsequent publication-consistency audit, and the broader C3/C4-C6 obligations remain OPEN unless genuinely completed.
