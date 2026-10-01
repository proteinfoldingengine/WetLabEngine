# v16.44 prospective two-branch unit-barrier theorem
Status: PREREGISTERED / NOT EXECUTED / NOT CERTIFIED.
Exact verified parent: 278be101e2c3c9e1cc4745533be94b306967bdf1, merged PR91, successful actual-merge run36798921114; durable receipt7aacac0138901ad8fca60fef53db5d93248a5110.

## Question and disclosed analytical hypothesis
Does every admitted rooted tree with exactly two internal vertices have B1=Binf=Bs=1 between distinct exact-profile components? Write T(a,b) for root degree a>=2 with one internal child of degree b>=2, and l=a-1 side leaves. For target root/inner profile (r,s), the side-leaf hitting number t belongs to {r-1,r}. The proposed construction normalizes the side leaves while fixing the inner support, expands that support to the full label set, normalizes inner leaves with a spare label when possible, chooses a canonical inner support, adjusts the side palette, then finishes inner normalization only after the root profile is exact. This scheduling is intended to prevent simultaneous deviations. It is an analytical hypothesis, not a measured result.
Prior v16.41/v16.42 include some small two-branch trees and profiles; v16.43 proves the local-star normal form used here. No blind replication is claimed. New two-branch general proof and its canonical representative-path certificates are prospective.

## Frozen universe and certificate scope
Exactly (a,b,k) in {2,3} x {2,3} x {2,3,4}; labels indexed, root carries all k labels. For every graph independently enumerate ALL admitted states, primitive moves, attained profiles, exact/unit components and unordered exact-component pairs. Require complete canonical identity equality at each level.
Store a candidate path from the minimum state ID of EVERY exact component of EVERY attained profile to a separately defined canonical endpoint. This is exhaustive quotient coverage, not every-state path sampling. Complete exact-component connectivity plus representative paths suffices for the finite upper bound; the general proof must cover all states.
Each path must be admitted, primitive and have total L1 profile deviation <=1. Primary B1,Binf,Bs remain three independent scalar minima; LEX remains separate. If all bounds pass, distinct-component lower bound1 establishes each scalar value1.

## Competing outcomes
NONUNIT_WITNESS: complete independent unit cut plus admitted unrestricted path, naming the scalar that exceeds1.
CONSTRUCTION_REFUTED: candidate representative normalization fails without an independently certified nonunit barrier; preserve the distinction.
TWO_BRANCH_THEOREM_VALIDATED: independent proof review accepts the general all-a,b,k argument and every frozen finite check passes.
INCOMPLETE: any coverage, resource, provenance or verification failure. Preserve artifacts and block closure.
Neither finite validation alone nor a failed construction proves/refutes the universal unit-barrier conjecture. Trees with three or more internal vertices remain outside this theorem. No physical inference is licensed.

## Controls, resources and closure
Reject omission/duplication/substitution of domain/state/edge/profile/component/pair/path identities. Include packed side-star downward excursions, a single side leaf, s=1, k=s delayed inner repair, maximum-root-degree disjoint support, overlapping root/inner q=2, and both spare leaf and spare label controls. Include invalid admitted-path moves/costs/endpoints, explicit construction-failure adjudication, abstract nonunit cut/path controls, wrong objective/provenance, and verifier-disabled expected RED.
GitHub-only numerical execution. All475 inherited tests plus new controls; fresh v16.43 and nested parent science byte reproduction; pinned Python3.11, Sympy1.13.3, mpmath1.3.0. Preflight<=5min, science/publication/post-merge<=45min each, receipt<=10min, ubuntu24.04. No outcome-driven domain relaxation or automatic expansion.
Preserve full source/input/Git-blob bindings, parent/prereg/head/run/attempt/workflow bindings, complete artifact and publication manifests. Fresh publication reproduction, independent review, exact-head merge, actual-merge replay and durable audited receipt are mandatory before CLOSED/CERTIFIED.
If a publication ZIP exceeds safe Git blob size, preserve it losslessly as ordered chunks of at most24MiB with size and SHA256 manifest, requiring reconstructed equality to the API artifact digest. This storage rule never changes scientific contents, membership or acceptance criteria.

