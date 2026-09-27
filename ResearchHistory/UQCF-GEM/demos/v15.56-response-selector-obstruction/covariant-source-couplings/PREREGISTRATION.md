# v15.79 preregistration — covariant source couplings

Frozen before gate.py exists or new scientific measurements are executed.
Parent 7f68c941f699ccbebec5b15834bfdb032807950f.
Branch research/v15.79-covariant-source-couplings.
Folder covariant-source-couplings. Historical files remain untouched.

## Frozen design and inputs

Implement DERIVATION.md exactly: single-source, state-independent real
bilinear equivariance, not a classification of CP source laws. All 63 raw
nonidentity source Paulis in lexicographic {0,1,2,3}^3 order, all 27 normalized
hidden Paulis in lexicographic {1,2,3}^3 order, and retained HS coordinates in
inherited M.ONE then M.PAIR order. Enumerate source supports by size then
lexicographic subset; retained supports likewise, restricted to sizes 1,2.
Canonical tensor coefficients are products of delta and epsilon, unscaled.

Freeze the inherited 12 states/candidate indices
[13,16,22,25,27,29,37,39,46,50,66,77] and v15.74 control_fixture(beta=0).
No reselection, random seed, fitting or finite differences. Source angle for
the unitary algebra check is pi/4. Generic rotation angles are X pi/7 and
Z pi/5 independently at each site, with all inputs and outputs transformed.
Use local Lie-algebra generator constraints for all four local combinations
(source scalar/vector, output scalar/vector; hidden always vector) to count
intertwiners independently. Use all three rotation generators per site.

At each state assemble Q and E coefficient maps of shape (63*27*9,18),
stack the 12 references to shape (183708,18), and separately measure the
zero-Bloch control. Observe each source/hidden basis input, not only a chosen
source direction. Report per-state and stacked singular spectra and ranks.
For every numerical rank use thresholds [1e-9,1e-10,1e-11] times that
matrix's largest singular value, unless the explicit zero-block reference
below is specified. No rank threshold is adjusted after measurement.

## Validity controls (failure overrides both verdicts as INVALID)

- Exact candidate indices; inherited M.domain valid for all 13 states.
- Source, hidden and output ordering/normalization agree with direct Pauli
  matrix moments within 1e-12; retained basis dimension 36, source 63,
  hidden 27. All recorded numeric values finite.
- Canonical tensor Gram matrix equals diagonal 27*2^k within 1e-12;
  off-diagonal zero. This checks tensor implementation, not completeness.
- Each constructed tensor satisfies all nine local generator constraints
  and six generic finite-rotation covariance identities to absolute
  Frobenius residual <=1e-11. Local Lie kernels satisfy their constraints
  <=1e-12 and agree with the corresponding analytic tensor projector
  <=1e-10 whenever that tensor exists.
- Direct complex matrix commutator/Jordan retained coefficients agree with
  the frozen predicted tensor sums to maximum absolute error <=1e-12 for
  every source and hidden basis pair. Tangents are Hermitian, trace zero;
  errors <=1e-12. Their retained complex moment imaginary part <=1e-12.
- All 63 finite U have unitarity residual <=1e-12; their retained hidden
  responses agree with sin(pi/4) times the commutator to max error <=1e-12.
  Identity-source commutator and Jordan retained responses <=1e-12.
- F_rho assembly agrees with an independent direct tangent evaluation for
  all 18 columns at each of 13 states using deterministic source weights
  (-1)^j/(j+1), j=0..62, and hidden weights (-1)^k/(k+1), k=0..26;
  maximum absolute Q/E disagreement <=1e-10. Sylvester residual <=1e-11.
- The inherited zero-Bloch control has one-body moments <=1e-12 and pair
  correlations .04 I within 1e-12. In its Q/E maps the six one-body-output
  columns have norm <=1e-12 times the complete map norm. Its Q/E ranks are
  12 at all three frozen thresholds, and the threshold-1e-10 right-kernel
  projector equals the coordinate projector onto those six columns within
  1e-9. This is an exceptional-state validation control.

Unexpected programming exceptions fail CI and are repaired without changing
this preregistration. They are not interpreted as scientific failures.

## Primary classification gate

The independent local Lie constraints give multiplicities 0,1,1,1 for
(source scalar/output scalar), (scalar/vector), (vector/scalar),
(vector/vector). Their products across the three sites give exactly 18
allowed source/target support pairs, with source-weight counts [3,9,6].
The assembled tensor basis has rank 18 at all three thresholds and splits
into nine one-cross and nine zero/two-cross tensors. A scalar source has
no allowed retained target.
YES: COVARIANT_SOURCE_COUPLING_CLASSIFICATION_CONFIRMED.
NO: COVARIANT_SOURCE_COUPLING_CLASSIFICATION_NOT_CONFIRMED.

## Separate ensemble observability gate

Both 12-state stacked Q and E coefficient maps have rank 18 at each frozen
threshold, hence coefficient nullity zero. Per-state ranks are diagnostics,
not additional required gates. A valid rank deficiency is retained as NO.
YES: COVARIANT_COUPLINGS_ENSEMBLE_NULL_EXCLUDED.
NO: COVARIANT_COUPLINGS_ENSEMBLE_NULL_NOT_EXCLUDED.
INVALID overrides both verdicts if any validity check fails.

## Publication and verification

Publish tests with gate.py absent, run Actions and inspect the expected RED.
Only then implement the frozen measurement; run GREEN, inspect exact job
logs and artifact JSON, verify execution SHA and checksums, then publish
RESULTS.md and the lossless result with exact run/job/artifact IDs. Tests
accept valid scientific NOs, so green CI alone is never called a YES.
No threshold/amplitude changes; no merge to main.
