# Shared leaf coverage forces the receiving index's record at a strict local endpoint

November 21, 2026 (America/Phoenix). The proof and exact replay were frozen at `1a6dd12f41726b96a9461049921d470de40e1707`. [Frozen derivation](P1_OWNER_ACTION.md) · [GitHub run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/44982566980)

## What the original event produces

Initially the same two indices both hold two terminal children of one parent. An inherited v16.26 deletion by the source index leaves the other index as the only holder of the deleted child. The receiver's own view is still the same on both source branches, but the same-union guard now permits it to delete only the other child at this parent. These are calls to the original event routine with fixed index and address arguments.

| Source deletion | Legal receiver deletion at this parent | Receiver child at the strict endpoint |
| --- | --- | --- |
| Child `(6,0)` | Child `(6,1)` | `(6,0)` with grade 2 |
| Child `(6,1)` | Child `(6,0)` | `(6,1)` with grade 2 |

The strict endpoint is the condition that two views are necessary to cover the parent's children, written $\tau_p=2$. In every deletion-only history reaching this endpoint, the same receiver action and child address are forced by coverage. The condition specifies a local cover number and leaves the realizing schedule and child address to the transition rule. The receiver's parent grade is 3 on both branches. The distinguishing retained quantity is the child address carrying grade 2. At the first event the local trigger is false in both histories. It is true in both at the forced receiver deletion.

The original code also accepts a second deletion by the source index that leaves both children with the receiver. Those two histories reach the same full state with $\tau_p=1$. A common receiver edit elsewhere also leaves its two marked children intact. These controls locate the remaining premise. The inherited rules constrain any refinement that reaches the strict endpoint. Physical attainment of that endpoint and access to the retained address remain open.

## What the archived geometry can distinguish

The same two event paths were replayed on a supplied 25-view geometry case with two equal graded children. The archived work evaluator saw the very same P1 projections of the verified event states. Both alternatives had identical full work tables at each matched phase.

| Phase | Minimum work | Nearest pairs | Work between source and receiver | Original square gate |
| --- | ---: | ---: | ---: | --- |
| Before the source deletion | 58 | 50 | 58 | Identifies 25 faces and rank two |
| After either source deletion | 54 | 3 | 62 | Degree test fails |
| After either forced receiver deletion | 54 | 6 | 66 | Degree test fails |

The prepared two-child branch changes the geometry, while the identity of the source deletion is preserved in the receiving index's own view at the strict endpoint. The geometry and scalar trigger sequence are identical across the alternatives. Global $h$ was 3 throughout. The periodic comparisons and placement of the two covering indices were supplied. The geometry replay carries forward the catalog constraint from the previous result. [Prior catalog result](P1_MEET_WORK_CATALOG_RESULT.md)

## Evidence

Eight original atomic outputs passed the historical verifier and were independently checked against the complete local deletion possibilities. The original transition denied six sole-owner deletions, and the verifier rejected a falsified trigger. The local and GitHub replays agree byte for byte, including all work tables and atomic records. Gemini 3.1 Pro accepted the scoped proof with native bridge status **OPEN**. The publication job independently reproduced the exact replay and reported the raw review and audit bytes. [Replay summary](p1_owner_action_evidence/replay.json) · [Gemini verdict](p1_owner_action_evidence/review_verdict.json) · [Audit](p1_owner_action_evidence/publication_audit.json) · [Artifact verification](p1_owner_action_evidence/readback.json)

The evidence directory preserves the original replay, review and publication archives, and the three original job logs. The replay archive includes the full work tables, original event records and pinned source bytes.
