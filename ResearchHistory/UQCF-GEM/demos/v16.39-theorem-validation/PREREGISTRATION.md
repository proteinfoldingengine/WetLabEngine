# v16.39 prospective theorem validation and obstruction campaign

Exact verified integrated parent: e4de671b3e483cc82a2e240dbd6a8d4d83e6518f; actual-merge audit36757689353 succeeded at that checkout/workflow SHA.

## Prior knowledge and chronology
v16.38 already exhaustively reconstructed n<=6,k=1,2,3:111 graphs,52907 states,244 component pairs,1497 endpoint pairs, all independent primary barriers and LEX_BARRIER equal1. This is NOT a new prediction of this campaign.
Exploratory PR85 at c934fee96516042aa48bcd004dc10dbb7142728f already contains the independently reviewed sufficient-condition proof and five-vertex four/eight-move example. Those findings are not retrospectively preregistered. This registration precedes implementation and execution of the new constructive and obstruction classification tests.

## Frozen domain and objectives
Keep the exact admitted definitions and independent scalar primary objectives of v16.37/v16.38; LEX_BARRIER remains separately defined. Re-enumerate the complete existing n<=6,k=1,2,3 universe with both independent engines. No seven-vertex expansion. Compare exact complete graph records with the durable v16.38 parent, not merely counts or supplied records.

For each of all244 canonical unordered distinct fixed-q component pairs, use canonical representatives and full component membership to cover all endpoints. Compute:
A={v:q_v>=2}; saturated={v:q_v=k>=2}; H=root union ancestor closure of A.
SC holds iff every H-edge u->w with u active has a saturated vertex in w's subtree.
Endpoint-full holds iff both representatives have all k labels at w on every such H-edge.
Emit exact violating edges, including whether each endpoint has restricted support. Classifications must be independently reconstructed.

## Constructive theorem test
For every SC or endpoint-full pair, implement the proof's zero-cost skeleton/subtree normalization, local transversal-to-singleton reduction, palette alignment, same-palette assignment repair, subtree lifting and inverse target normalization. No graph search is allowed to supply this constructive path. Emit every state/move. An independent checker reconstructs supports, legality, q, endpoints and width (at most one deviating coordinate, absolute deviation<=1). Full numerical threshold evidence remains a separate oracle.
A bad constructed path is IMPLEMENTATION_FAILURE, not automatically a mathematical refutation. A valid admitted SC pair with independently certified B1>1 would refute the theorem; do not infer such a result from a selected algorithm's failure.

## Remaining obstruction experiment
For every pair failing both SC and endpoint-full, test STATIC-COORDINATE repair separately for each vertex v: graph induced by q_i=q0_i for all i!=v and |q_v-q0_v|<=1. Emit an attaining path for every successful v and the complete reachable component for every failed v. A second implementation independently recomputes connectivity and checks all paths/cuts.
Also certify connectivity in the full L1<=1 graph. If full-unit connectivity holds but every static-coordinate test fails, report MOVING_LOCATION_REQUIRED for this pair, with all failed-coordinate cuts and an explicit full-unit path. Otherwise report STATIC_COORDINATE_SUFFICIENT. No static-path failure alone is a nonunit witness. The known parent unit results are disclosed; the new information is the exact structural partition and fixed-coordinate versus changing-coordinate requirement.
Zero-cost paths lie in every constrained graph, so these connectivity properties are representative-independent.

## Competing outcomes and resources
THEOREM_CONSTRUCTION_VALIDATED_WITHIN_DOMAIN, IMPLEMENTATION_FAILURE, THEOREM_REFUTATION_CANDIDATE, INCOMPLETE. Separately: obstruction class empty, all static-coordinate sufficient, or at least one moving-location-required pair. Universal unit law remains UNRESOLVED in every finite outcome.
Canonical witness ordering: vertex count,k,parent tuple,q,component representatives. Minimality only inside the frozen domain. GitHub-only scientific execution; Python3.11 and pinned inherited dependencies;45-minute per-job limit; no sampling,state cap,selective exclusions or silent domain changes. Preserve failed runs.

## Controls and closure
Reject omitted/duplicate/same-count substituted pair records, false SC/endpoint classification, invalid or wrong-endpoint paths, width violations, false successful coordinates, incomplete failed-coordinate reachability, false verdict/summary, wrong schema/domain and false stage-specific provenance/source bindings. Include explicit known four/eight-move example and honest failure controls.
Run all261 inherited tests plus fresh parent science byte reproduction. Upload complete new scientific certificates, source/input snapshots, logs, environment/checkout/workflow/trigger/run/attempt metadata and manifests. Fresh publication repeats all science/tests with byte-identical scientific outputs. Review entire branch, inspect downloaded artifact digest/CRC/hashes, commit durable evidence, ready/merge exact verified publication head, replay full science/tests/manifests on actual merge SHA with an artifact and durable receipt. Only then close numbered stage. Preserve PR85 as exploratory history.

