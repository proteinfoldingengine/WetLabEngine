# v16.27 — Increment-attribution closure

Parent: v16.26 published head `dcb97686766490a4847a57db40a2286aad468733`.

## Question
v16.26 proved that every legal atomic same-union pruning has delta h in {0,1}, and every endpoint refinement has a telescoping total. Does the unit increment belong canonically to the **removed incidence/event**, independent of legal pruning order, or is only the endpoint total invariant?

## Frozen alternatives
A. EVENT_ATTRIBUTION_CANONICAL: for any fixed endpoint refinement and any two legal atomic factorizations, each removed (view,node) event has the same delta h.
B. EVENT_ATTRIBUTION_PATH_DEPENDENT: there exists an admissible endpoint refinement and two legal factorizations where the same removed event has delta h=0 in one order and 1 in another, while total delta h agrees.
C. UNRESOLVED if exhaustive bounded search finds no witness and no theorem decides it.

Do not select an outcome in advance.

## Further classification
Even if event attribution is path-dependent, test whether the set of events capable of carrying a unit increment is characterized by the local minimum-cover trigger at the state immediately before deletion. Distinguish state-dependent trigger from endpoint-invariant attribution.

## Verification
Enumerate all endpoint same-union componentwise refinements on rooted trees through 4 vertices, at most 4 views, with at most 5 removed nodes total. Enumerate **all legal atomic deletion orders** preserving prefix closure and union at every step. Compare per-event delta-h maps and total sums.

Require an explicit witness for path dependence, including both paths and state certificates. If no witness, a bounded absence is not a universal theorem.

Reject: changed-union paths, illegal non-leaf deletion, missing endpoint event, altered delta, and two paths that do not reach the same indexed endpoint.

General invariant: total sum equals h(final)-h(initial) by v16.26 telescoping.

No fundamental time, response law, or geometry.
