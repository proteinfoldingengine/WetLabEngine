# v16.15F — Graded obstruction descent

## Earned criterion
v16.14F proved that a response-information obstruction T on K_j descends to the canonical grade G_j=K_j/K_{j-1} iff T(K_{j-1})=0.

## Frozen test
Use only the four existing exact prefix-tree pruning fixtures. Build an ordered pruning chain from each fine tree by retaining the archived final coarse subtree and adding removed leaves back in canonical lineage-address order, producing nested prefix-closed carriers from fine to final coarse. No geometry or response coarse map is introduced.

For each stage j, form P_0j and K_j=ker(P_0j). Let O_j=(Q_0 G_0)|K_j be the already-defined intrinsic full-fine response obstruction, where Q_0 removes only the constant response gauge on the initial connected tree.

Test exactly whether O_j vanishes on K_{j-1}. Since K_{j-1}⊂K_j, this is the descent condition for O_j to factor through G_j.

Also compute rank(O_j|K_j) and rank(O_j|K_{j-1}) exactly. No numerical threshold.

Outcomes:
- GRADED_OBSTRUCTION_DESCENT_CERTIFIED
- OBSTRUCTION_RETAINS_PRIOR_GRADE_HISTORY
- MIXED_GRADED_DESCENT
- INVALID

This tests the earned full-fine intrinsic obstruction. It does not assert that retained-boundary response fails; the exact boundary theorem remains intact.
