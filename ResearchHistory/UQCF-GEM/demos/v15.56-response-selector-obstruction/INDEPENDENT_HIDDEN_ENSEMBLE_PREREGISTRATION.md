# Independent Hidden-Completion Ensemble / Scaling Gate — Preregistration

Parent single-fixture held-out result: d5f9616e85d21f701258993b298d313ead7c1028. This gate tests replication and law-like scaling, not rediscovery.

## Ensemble frozen before evaluation
Use the same Stage-A constructor and oriented-edge conventions. Enumerate the existing fixed grid in lexicographic order:
m in [0.10,0.15,0.20], d in [0.08,0.12,0.16], a in [0.04,0.08,0.12].
A base state enters the ensemble iff, without hidden completion:
- min eigenvalue >= 0.03;
- oriented cyclic pair difference <= 1e-12;
- minimum pair singular value >= 0.02;
- loop holonomy angle >= 0.20.
No response value may enter membership.

Freeze ALL qualifying states, not a selected subset.

## Hidden amplitudes
For each member evaluate eta = 0.001, 0.002, 0.003 only when hidden-state min eigenvalue >= 0.01.
No amplitude is chosen from response.

## Matched inputs
At every evaluated eta require proper one/two-body difference <=1e-12, initial polar difference <=1e-10, initial holonomy difference <=1e-10.

## Endpoints
D(m,d,a,eta)=||dot H_hidden-dot H_base|| under the same Pz source.

Primary replication criterion:
- at least 6 admissible base fixtures;
- every admissible evaluated fixture has D(eta=0.003)>1e-6 where eta=.003 is positive;
- median D(.003)>1e-3.

Scaling criterion, per fixture with all three eta values:
Fit through-origin slope using the three predeclared eta values only.
Require relative RMS residual <= 0.05 and positive slope.
Ensemble scaling passes if >=90% of eligible fixtures pass.

Controls on every fixture: eta=0 null, identity-source null <=1e-7, source x2 linearity residual <=1e-5. Hidden sign is evaluated as an antisymmetry control at eta=.003 with residual <=1e-5.

Verdicts:
ROBUST_LINEAR_HIDDEN_GEOMETRY_RESPONSE: replication + scaling + all matched-input/control gates pass.
ROBUST_NONLINEAR_HIDDEN_GEOMETRY_RESPONSE: replication and controls pass but scaling criterion fails.
ENSEMBLE_NULL: all gates/controls pass but replication threshold fails.
INVALID_ENSEMBLE: membership, matched-input, or control gate fails.

No parameters are fitted to improve these verdicts.

## Claim boundary
A robust verdict is a finite-model response law inside the BKM/polar/QMAR architecture. It is not a derivation of physical gravity, Genesis source selection, spacetime, Einstein equations, or an absolute coupling.
