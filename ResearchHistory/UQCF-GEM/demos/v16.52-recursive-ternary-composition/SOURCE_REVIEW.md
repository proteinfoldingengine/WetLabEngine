# Independent pre-science source review

Reviewer: independent assistant source_review, 2026-10-01. Reviewed implementation head2ff0832d3a7b592e1499365c4ad57bd9821743b2 and the proposed campaign workflow; read-only source and byte/hash inspection, no local numerical execution.

Initial verdict: REQUEST CHANGES before definitive science. No Critical findings. Three Important findings:

1. Completed transport moves can disappear from failure evidence. `transport_child` privately accumulates primitives and `_normalize` copies them only after success. A later exception loses completed transport moves. Preserve and merge the exact partial path, and inject an exception after real moves to verify it.
2. New assertion hashes are recorded but not enforced. Package verification checks names but ignores assertions_sha256, expected, and count. Reconstruct the complete AST assertion manifest and enforce exact equality before execution; reject mutations.
3. Resource/infrastructure exceptions become scientific construction failures. All exceptions are recorded and then converted into InterfaceNotPreserved. Preserve original exception identity and an explicit category; resource errors must yield INCOMPLETE.

Strengths: induced palette order and skipped width-k transport; one recursive interface for both parent arities; independent total-L1 checks; exact ordered7236 identity equality; support-set hitting enumeration and incidence-region minimality at every interface. Static inspection confirms all1071 inherited identities and hashes, current76 new test identities/hashes, and both initial RED archive digests/source bindings. Source snapshots, raw/extracted archive binding, ordered merge parents and tree equality form coherent provenance checks.

Minor: historical preimplementation status text should be explicitly dated as historical before freezing definitive source.

The reviewer did not adjudicate pending runtime GREEN/performance, fresh scientific reproduction, live GitHub publication/merge/receipt, or re-prove inherited science outside supplied analytical context. Those are separate mandatory execution/closure gates; none is waived.

The construction and verifier appear consistent with R1–R6. Suitability for definitive science is conditional on the three fixes, their RED-to-GREEN controls, and review of the corrected source. Certification remains pending all execution and post-merge gates.

## Corrected-source scoped re-review

Independent reviewer source_review inspected corrected source37cc2729b76f60b7a470acf434a0be21c864ced9 and the proposed campaign workflow. Verdict: all three Important findings ADDRESSED; no new blocking source defect. Suitable for definitive science contingent on79 GitHub controls passing and retained frozen source/manifest bindings.

Partial-path retention is addressed at both levels: transport captures completed primitives; its caller appends retained steps after the duplicate initial state before propagating, so normalize retains the full outer path and recursive callers project it into ancestor coordinates. Assertion-manifest reconstruction now enforces identities, expected results, hashes and count in preflight and package verification; all79 entries statically match source. Original exception types survive wrappers; recorded resource/infrastructure categories remain INCOMPLETE through the end-to-end verifier/runner classifier.

The reviewer verified the review RED archive digest, unchanged test source, and exactly3 intended failures with0 errors. Historical statuses are clarified. Preflight, separate fresh executions, publication checks and actual-merge receipt workflow remain suitable. This acceptance does not assert runtime success or certification; no numerical science/tests were run by the reviewer.

Runtime gate resolved by executor after review: GitHub run36909426860 passed all79 exact test identities. Downloaded archive SHA25625dc33ee704eef4be27fa37532d0c1fea879acb9e12bb3e881f850ab33aa3303 and all four logs independently inspected. This satisfies the reviewer’s GREEN condition; definitive science remains a separate subsequent execution.
