# v15.70 Strict marginal descent and fixed-base composition

Date: 2026-09-26. Parent: 5d079ca4bef6d51a38111f2312af87aa03e753c7.
Branch: research/v15.70-atlas-descent-composition.

## Question and mathematical scope

Does the existing v15.64/v15.69 source field descend to retained marginal data? Does fixed-base composition itself force a skew response?

Inspecting the actual code matters: Y(rho) is independent of the labeled hidden direction h; the source field is X_{rho,h}(sigma)=Y(rho) Tr[h(sigma-rho)]/Tr[h^2]. The variable differentiated by DX is sigma, with rho and h held fixed. We must not interpret the normalization in h as a linear assignment on source labels.

For a differentiable marginal-autonomous field, R X_G(sigma)=X_R(R sigma), differentiation gives R DX_G[h]=DX_R[R h]=0 whenever R h=0. This excludes symmetric AND skew hidden leakage. It is stronger than overlap compatibility and cannot selectively force rotational response. A finite fiber witness avoids assuming a regional formula or arbitrarily defining Y_R(rho_R,0).

The minimum-norm lift has only weight-two Pauli coefficients: its one-body coefficients are constrained to zero and its unconstrained weight-three coefficients vanish by minimum norm. For every weight-three h_a, N_a=|Y><h_a| has N_a N_b=0. Thus at fixed rho, affine updates compose additively and commute. Combined source data means the sum of linear operators, not a renormalized sum of labels. This is a theorem prediction, not a measured verdict.

## Frozen measurement

- Reuse all 12 states selected by the unchanged asymmetric-heldout-ensemble selector, seed 20260928; required indices [13,16,22,25,27,29,37,39,46,50,66,77]. No new random frames or selection.
- Reuse v15.64 target_Y and the historical simultaneous target O_e I/sqrt(3).
- Edges (0,1),(1,2),(2,0), retaining their order. Restriction is literal partial trace, independently checked on complex product operators and Bell states.
- All 27 HS-normalized exact-weight-three Pauli labels. Source amplitudes s=1e-3, u=-3e-4 and hidden amplitude eta=1e-4. These are ordered source parameters, never fundamental time.
- 324 state/hidden probes, 972 edge descent witnesses. Compare sigma_plus/minus=rho +/- eta h; equal marginal inputs must have equal outputs for any marginal-only regional update. Measure output gap and compare it with 2 eta s RY.
- Analytic derivative obstruction norm ||RY||; expected value 1/2 per edge from the unit-norm correlation target. Report this prediction independently of verdict.
- Overlap consistency: each edge lift restricts to zero on either endpoint; nested restriction equals direct restriction. Distinguish this compatibility from source-law descent.
- Fixed-base composition: compute all 729 pairwise products/commutators of N_a on the full 63-dimensional real Hermitian tangent space for each state. Report maximum product and commutator norms; also finite sequential, reversed, combined-operator and same-source additive updates on sigma=rho+eta(h_XXX+h_YYY). No base point is reset between operations.
- Compute connected-correlation changes and polar-skew residuals directly; no small-step mixed polar finite differences. Verify the composed path remains on the positive polar stratum. Report finite rotation change without dividing by small steps.
- Save every state-level diagnostic and every hidden/edge descent witness in result.json; record execution SHA and preregistration/test/implementation hashes in evidence artifact.

## Frozen validity checks and controls

Float64, Python 3.11, numpy 2.3.5, one OpenBLAS thread. All diagnostics finite; correct state identities and counts required.

Validity thresholds: state trace/Hermiticity 1e-12; input/output eigenvalue >= -1e-12; base-state eigenvalue >= .025-1e-12; base edge singular >= .020-1e-12 and positive polar eigenvalue >0; lift relative residual <=1e-10; target reconstruction <=1e-10; partial-trace/overlap/hidden-input equality residual <=1e-12. Finite output gap must agree with 2 eta s RY to relative 1e-8. Polar-skew null relative residual <=1e-10, nonzero target norm >1e-6. None are retuned after results.

Null control: identity update preserves each equal-input marginal pair, <=1e-12. Positive sensitivity control: replace one symmetric correlation target by O K with K=(E01-E10)/sqrt(2), globally lift by the same constraints; skew norm >1 and reconstruction <=1e-10. Composition sensitivity control: N=|Y><h| and M=|h><Y|/||Y||^2 must have commutator norm >1 (not claimed admissible null sources). Missing or failing controls, malformed data, nonfinite metrics, or exceptions -> INVALID.

## Frozen verdict logic

Primary verdict is strict marginal descent, not universal atlas naturality:

- ATLAS_NATURAL_NULL_OBSTRUCTED if any valid derivative witness ||RY|| >1e-10.
- ATLAS_NATURAL_NULL_CONFIRMED if all valid derivative witnesses <=1e-10. This is only confirmation on the frozen probes; never a universal existence proof.
- INVALID if a validity/control condition fails.

Orthogonal composition report: FIXED_BASE_NULL_COMPOSITION_CONFIRMED if all products and commutators <=1e-12, finite sequential/reversed/combined/additive residuals <=1e-12, finite rotation change <=1e-10 and composed positive-polar minimum >0. Otherwise FIXED_BASE_NULL_COMPOSITION_NOT_CONFIRMED. Failure of this scientific composition gate must be reported, not silently mapped to a pass.

GREEN CI means code/tests/evidence completed. Either valid primary scientific outcome exits zero. INVALID exits 2. Tests validate computations and both adjudication branches, not force the desired experimental verdict.

## TDD and interpretation limits

Publish this document, DERIVATION.md, tests and dedicated workflow with implementation absent; inspect Actions RED for that specific absence. Implement only afterward, inspect GREEN logs and download artifact. Preserve v15.64-v15.69 historical verdicts. No merge to main.

No claim about a globally integrable base-point-independent field, arbitrary rebasing, tensor-product composition, enriched regional source memory, global positivity for arbitrary amplitudes, physical source selection, or gravity. In particular strict marginal autonomy would also eliminate the nonzero exponential/filter hidden responses; it is not an earned physical axiom. The next structural question would need explicitly retained source/extension data, not an unacknowledged weakening of this gate.
