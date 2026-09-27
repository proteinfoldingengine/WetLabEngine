# v15.71 Memory-enriched null law and Jacobian integrability

Frozen before measurement, 2026-09-26 America/Los_Angeles.
Parent: `0d90d48da6c121ae2e808930a9c5d10198abe437`.
Branch: `research/v15.71-memory-enriched-null`.

## Question

Can the historical hidden derivative be realized by one smooth state-dependent source field with explicitly retained scalar memory, rather than unrelated reference-centered fields? Separately, can the historical *entire* rank-one Jacobian assignment be integrated unchanged?

The distinction is essential. For unit full-support source label h, define m_h(rho)=Tr(h rho) and X_h(rho)=m_h(rho)Y(rho), where Y is exactly the historical minimum-norm lift with pair correlation targets O_e/sqrt(3). On regular polar strata this is a single field, without a moving reference state. Its hidden derivative is Y, but its visible derivative includes m_h DY. It does not silently integrate the entire old rank-one Jacobian.

Regional inputs are now explicitly (rho_R,m_h), or (rho_R,m_h,m_k) for two sources. The memory is transported unchanged under restriction and under this candidate's updates. It is an added global source observable, not information recovered from a marginal, and its physical/native origin is not established. The original marginal-only naturality gate remains obstructed.

## Frozen data and operations

- Reuse unchanged v15.58 selector (seed 20260928), exact indices [13,16,22,25,27,29,37,39,46,50,66,77].
- All 27 unit exact-weight-three Pauli h, ordered lexicographically as in v15.70; k is the next cyclic label.
- Three visible bases per state: rho and rho +/- 1e-4 v0, v0=XXI/sqrt(8).
- At each base and h use sigma=base+eta(h+k), eta=1e-4. This gives 972 cases and 2916 edge restriction comparisons. Source amplitudes s=1e-3, u=-3e-4 label ordered updates, not fundamental time.
- Global candidate Y is the closed-form weight-two lift. Independently compare it with the unchanged v15.64 least-squares lift at each of the 36 visible bases.
- Regional y_e is computed independently from the two-qubit marginal's own connected correlations and polar factor: y_e=sum_ab O_ab sigma_a tensor sigma_b/(4sqrt(3)). Never pass the global Y or global O to that regional computation.
- Compare enriched regional update with restriction of the global update. Test both endpoint overlaps, memory preservation, trace and positivity. Removing memory (setting it to zero) is a positive obstruction control, not a rescue of v15.70.
- Recompute Y and X at each updated state. Compare sequential h then k, reversed order, sum of source increments, and same-source s then u versus s+u. Test Y constancy along these paths and unchanged finite rotations. No base/reference reset occurs.
- At every case use centered hidden derivative epsilon=5e-6 to compare DX_h[h] with Y(sigma).
- At every original base, use all 27 unit weight-two Pauli v. Compute DY[v] analytically with the polar Sylvester derivative; verify by centered differences at epsilons [1e-5,5e-6]. Normalized error is ||FD-analytic||/max(1,||analytic||). These are verification steps, not fit parameters.
- Use h=XXX/sqrt(8), sigma=rho+eta h for the visible Jacobian completion probe: DX_h[v]=eta DY[v], checked at both derivative epsilons using error denominator max(eta,||eta DY[v]||). Record the nonzero visible correction omitted by the old rank-one assignment.
- The old full-Jacobian integrability curl is C(v,h)=D_v N[h]-D_h N[v]=DY[v], N_rho[z]=Y(rho)Tr(hz). Assemble all 27 columns in the 63-dimensional Pauli tangent basis. Record ranks at relative tolerances [1e-9,1e-10,1e-11], singular values and norms. The predicted rank is nine; it is a measured secondary result, never imposed as validity.

## Frozen validity and controls

Python 3.11, numpy 2.3.5, OPENBLAS_NUM_THREADS=1; no added random seeds.

Require all numeric diagnostics finite and exact counts. Density trace/Hermiticity <=1e-12; density eigenvalue >=-1e-12 throughout all finite/derivative probes. Base polar factors and finite-update polar factors must remain on positive regular stratum; minimum edge singular >=.015 (a fixed domain floor below the inherited .020 selector). Closed-form versus historical Y relative error <=1e-10. Source memories must be nonzero with |m_h-eta| and |m_k-eta| <=1e-12 for primary probes. Hidden-free original bases have all 27 memories <=1e-12. Analytical DY must match its two centered-difference checks <=1e-5; malformed data or failed numerical verification is INVALID, not a scientific NO.

Controls: exact diagonal positive-polar Sylvester derivative and complex regional partial trace in unit tests; an independently lifted O K target, K=(E01-E10)/sqrt(2), must produce skew norm >1; deleting memory gives regional vector-field discrepancy >1e-6; a constant-Y Jacobian has exactly zero analytic curl. Adjudication tests exercise CONFIRMED, NOT_CONFIRMED/OBSTRUCTED, and INVALID branches, including nonfinite output handling inherited from v15.70.

## Frozen scientific gates

Primary MEMORY_ENRICHED_NULL_CONFIRMED if every valid case has:

- enriched restriction state residual <=1e-11;
- edge-to-endpoint source overlap residual <=1e-12;
- memory change <=1e-12;
- sequential/reversed/combined/same-source additive residuals <=1e-11;
- recomputed Y relative change <=1e-9;
- finite polar rotation change <=1e-10;
- hidden derivative relative error <=1e-9;
- visible completion derivative verification error <=1e-5.

Otherwise MEMORY_ENRICHED_NULL_NOT_CONFIRMED. Any validity/control failure -> INVALID. Valid negative verdicts exit zero; INVALID exits 2. Report all individual errors and failures.

Secondary FROZEN_FULL_JACOBIAN_OBSTRUCTED if any valid curl column norm >1e-8; otherwise FROZEN_FULL_JACOBIAN_NOT_OBSTRUCTED_ON_PROBES. Report all rank sweeps. The latter would be a finite probe result, not a general integrability theorem. No changed thresholds after observing outcomes.

## TDD / publication

Publish this preregistration, DERIVATION.md, tests and dedicated workflow with implementation absent. Inspect exact RED. Then implement only this measurement, run GREEN, inspect logs and download/check artifact. Preserve full JSON, checksums, run/commit/artifact IDs and RESULTS.md on the additive branch. Never merge to main or rewrite v15.64-v15.70 verdicts.

## Boundaries

This is a constructed existence test, not physical selection. Y uses the retained observable to construct a counterexample. The memory is additional information; covariance does not supply its native origin. Local/global refers to a regular open domain of state space, not positivity for arbitrary source strength. No tensor-product naturality, unique law, Einstein/gravity derivation, or minimal universal memory dimension is claimed.
