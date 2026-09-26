# Independent Hidden-Completion Geometry Gate — Preregistration

Baseline: ed37bf640472f1206f6ff66f01315e3e17702df6

## Purpose
Test whether hidden higher-order completion generically changes polar-connection / loop-holonomy response under the same supplied radial ETL/PGRL source while all initial one- and two-body data, and therefore initial BKM/polar geometry, are held fixed.

This is a new fixture, not a fit or numerical reconstruction of v13.09.

## Frozen before outcome computation
- Three qubits; cyclic order 0->1->2->0.
- Source Pz=(Z0+Z1+Z2)/sqrt(3).
- Hidden shape G_hidden=sum_cyclic (X_i Y_j-Y_i X_j) Z_k; positive amplitude sign.
- Base must be faithful, cyclic, common axial U(1), equal one-body marginals, cyclic-identical pair connected correlations, Dx=Dy, nonsingular pair polar factors, and nonidentity loop holonomy.
- Base parameter selection may use only those admissibility conditions and numerical conditioning margins. It may NOT use hidden response or archived 0.272393... / 0.192611... targets.
- After base freeze, choose largest eta in {0.001,0.002,0.003} keeping hidden state minimum eigenvalue >=0.01. Response may not enter eta selection.
- Before response: one/two-body differences <=1e-12; initial BKM difference <=1e-10; polar difference <=1e-10; holonomy difference <=1e-10.
- Primary held-out endpoint: central derivative at s=0 of loop holonomy matrix under normalized exp(log rho+s Pz), base versus hidden.
- Controls: eta=0; identity source; hidden-sign reversal; cyclic covariance; source scaling; symmetric finite-source consistency.
- Verdict SIGNAL if all gates pass and holonomy-jet difference >1e-6; NULL if gates pass and <=1e-6; INVALID_FIXTURE otherwise.
- Parameters fit to response: zero.

## Claim boundary
A SIGNAL establishes an independently constructed finite-model hidden-completion -> connection-response effect inside the defined BKM/polar/QMAR architecture. It does not derive Genesis source selection, physical gravity, spacetime, Einstein equations, or absolute coupling.
