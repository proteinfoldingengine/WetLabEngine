# 16.19 — Full-response information-kernel result

**Verdict: LOCAL_SCALARS_COMPLETE_ON_REALIZED_RESPONSE.**

The exact realized first-order response span was classified before any geometric interpretation. For each of the 72 frozen candidate/middle/preparation groups, the two archived coefficient responses (constant and coherence) span a two-dimensional exact subspace of the full six-edge matrix-response space. The independently reconstructed differential of the 24 frozen local invariants has rank two on that span in every group.

Therefore:

- groups: 72;
- total realized response-span dimension: 144;
- total local differential rank: 144;
- groups with nontrivial local-scalar kernel: 0;
- total kernel dimension: 0.

So the chosen local scalar differential loses **no realized first-order response direction** in this frozen physical-path family. This is stronger than 16.16's order-contrast rank result. It does not prove completeness for arbitrary perturbations outside the realized source span, higher-order response, other source families, or all possible local invariants.

No metric, connection, area, curvature, embedding or gravity interpretation follows from this result. In particular, there is no first-order information deficit here that can legitimately be promoted into a new relational/geometric carrier.

## Methodology

Preregistered RED run **36509824862** failed all three new tests because the implementation was absent. The first implementation run **36509900690** was invalid before adjudication because the workflow omitted an inherited NumPy dependency; no scientific result was taken from it. Only that pinned dependency was corrected. GREEN run **36509972888** then passed all three tests and the exact 72-group audit at commit **628e5ca649f2cb6f6ec8ba9ee0ed9c489cdf882d**.

The parent v16.15 publication is byte-bound by SHA256 `3b3f5e075ef129640f135b76780544ea268bd22bbc2efb17cd4d3b3dbebe2b81`. Local derivatives were reconstructed independently from baseline matrices and full derivative matrices using exact rational formulas rather than taking the archived scalar outputs as the primary calculation.

Time remains pruning / ordered recoverability update. Pillar 2 and Pillar 3 remain open.
