# v16.42 prospective overlapping-core repair campaign
Status: PREREGISTERED / NOT EXECUTED / NOT CERTIFIED.
Verified integrated parent: 6c5dae8ace7b06f3b7f071f5398976c532da2578 (PR89).
Actual-parent run: 36791188422; verified receipt: 86ac4897fb6e354d5ace113c12991b6e997c1aea.
This document must be committed directly on that parent before new campaign implementation or numerical execution.

## Question and prior analytical rationale
Can a fresh-label substitution lemma extend unit repair beyond partition profiles to an overlapping terminal core behind arbitrarily many binary branches?
The proposed family T(d,m), d>=0,m>=3, consists of an m-leaf star with d successive binary parents, each with one additional side leaf. Set k=d+2; q=2 at every internal vertex, zero at leaves.
Analytical expectations, NOT new measured results: every side leaf is a singleton, the core has two labels, and core leaf supports are A, B, or AB with at least one A and one B. Predict k!/2 exact components, each containing 3^m-2*2^m+1 states. For d=0 there is one exact component; that is a zero-connectivity test, not nontrivial barrier evidence.
The proof attempt will use fresh-label cloning (add the fresh label wherever the old label occurs, top-down; remove the old label bottom-up) and exchanges between disjoint palette blocks. Core normalization is a separate zero-cost construction. These are prospective candidates, not accepted theorems.

## Frozen numerical domain
Exactly (d,m)=(0,3),(0,4),(0,5),(1,3),(1,4),(2,3), with k=d+2. Re-enumerate all admitted indexed states, primitive incidence moves, and attained profiles for each graph. Barrier-test ONLY the stated all-internal-2 profile. Independently derive the canonical family identities and require exact set equality; do not call this every tree of a given size.
For every target state retain a claimed zero-cost normalization path. For every unordered pair of exact components retain both corrected threshold evidence and the proposed theorem path. Include the d=0,m=2 two-component boundary as a diagnostic outside the theorem domain.
The d=2,m=3 threshold result was already observed in v16.41. It is disclosed inherited evidence; the new prospective measurements concern the construction, state normalizations, and remaining frozen cases. It is not a blinded replication.

## Frozen objectives and outcomes
Primary B1, Binf, Bs are independent scalar minimax objectives. LEX remains a separately named diagnostic.
- NONUNIT_WITNESS: complete independent unit-threshold cut plus admitted unrestricted path; state which scalar is proved nonunit. Never promote an abstract graph.
- CONSTRUCTION_REFUTED: a legal endpoint pair or exact state defeats the candidate path while threshold evidence remains separately adjudicated. Preserve the failing certificate. Failure of one algorithm alone does not disprove existence of another unit path.
- FAMILY_THEOREM_VALIDATED: independent mathematical review accepts the all-d,all-m proof, and every frozen finite admission/edge/profile/component/pair/path/normalization check passes.
- INCOMPLETE: resource or provenance failure; no certification.
A bounded unit result without an accepted proof remains bounded. Universal unit barriers and intrinsic indecomposability remain unclaimed. The family is expressly compositional.

## Controls and closure
Require omission/duplication/domain/edge/profile/component/pair/path mutations; wrong component-count and normalization mutations; a constructed-path failure distinguishable from a genuine nonunit outcome; abstract nonunit positive control and invalid-cut/path controls; m=2 boundary; expected-failure verifier-disabling control.
Execute numerical work on GitHub Actions only. Rerun all 387 inherited checks plus new controls, and freshly reproduce v16.41 science with nested parent evidence. Source and dependencies pinned; source/input membership, Git blobs, run/attempt/workflow/head, prospective commit and verified parent bound to artifacts. Preserve certificate before verification.
Fresh publication execution must reproduce scientific bytes. Verify artifact API hashes and complete manifests; publish evidence and report. Review before marking ready; merge with exact expected publication head; rerun on actual merge; verify parents/tree/results; retain durable audit receipt. Do not call the numbered stage complete before this chain closes.
