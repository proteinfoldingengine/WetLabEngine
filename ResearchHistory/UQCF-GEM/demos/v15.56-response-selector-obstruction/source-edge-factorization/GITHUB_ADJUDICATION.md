# GitHub adjudication — source-edge factorization gate COMPLETE

Date: 2026-09-26. This completion record supersedes any earlier pending GitHub status in the local-execution handoff. It closes the bounded factorization/export/validity task, not a gravity or source-law-universality claim.

## Verified execution and artifacts

- Implementation head: `9b78f689449a2bfe9dc332cad3542700e059f2ab`.
- Branch: `research/v15.56-source-edge-factorization`, forked from `ec33024e0343193f6a5d0c7ed62d8512701dd541`.
- GitHub run: [36271450389](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36271450389).
- Job: `108486070671`, completed **SUCCESS**, including cleanup.
- New fail-closed tests: **20/20 passed** (10.170 s on GitHub).
- Existing complete UQCF v15.56 demo suite: **301/301 passed** (346.361 s on GitHub). Unrelated protein-engine tests are outside this scope.
- Full measurement: **11 fixtures x 243 hidden/source tensor columns**; all control checks passed.
- Measurement and separate saved-artifact verification both returned `FACTORIZATION_VERIFIED_243_9_3`, `verified: true`.
- Python 3.11.16; NumPy 2.3.5; single-threaded BLAS environment.

Source snapshot artifact: **10915941206**, SHA-256 `b30882ac8b76f0bd4327f5aae7ea5cc837c0100d56e9c13f4f7baee356d0e7bf`.

Full evidence artifact: [10916290893](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36271450389/artifacts/10916290893), SHA-256 `ca7870c1884e7b5b1c436e8052a5d3c085204e95015f469df17f4690f05494f9`.

Evidence includes 11 NPZ files, full report.json, test logs, measurement and verification logs, preregistration, and exact checkout SHA. Report JSON SHA-256: `615e98c8d7ad309e0e8d1d91013d8ca4f86e1604c6742f6824d114075cea27e5`. GitHub currently records artifact expiry as 2026-12-25; the source and adjudication are committed independently of artifact retention.

Both artifact ZIP digests were verified after download. The exact GitHub source snapshot was then used to verify all saved GitHub NPZ files and recompute their diagnostic summaries locally, successfully. The source snapshot also matches the locally tested implementation, preregistration, tests, and all seven hash-pinned historical source modules byte-for-byte.

## GitHub numerical results

All 11 fixtures have rank E=9, rank K=3, rank Pi E=3 and rank (I-Pi)E=6. The main effective ranks are stable at the preregistered relative cuts 1e-9, 1e-10 and 1e-11.

| Diagnostic | GitHub result |
| --- | ---: |
| Maximum full-matrix factorization relative error | 9.045539936388003e-16 |
| Maximum non-skew residual / parent Frobenius norm | 3.185771657058189e-16 |
| Effective non-skew rank under parent scaling | 0 at all 33 edges |
| Maximum error across 33 dense finite-difference probes | 9.603220020881997e-8 |
| Minimum sigma_9(E)/sigma_1(E) | 0.5292203972728345 |
| Maximum sigma_4(K)/sigma_1(K) | 4.2225211841533633e-16 |
| Minimum loop-visible squared-norm fraction | 0.2910935688853428 |
| Maximum loop-visible squared-norm fraction | 0.3477852479702824 |

The finite-difference error uses the frozen denominator max(1,||K_analytic||_F); the threshold is 1e-5. Three predetermined dense probes per state are checked at two step sizes. This is not a finite-difference verification of all individual basis columns.

The fresh raw-data measurement confirms the earlier interpretation of non-skew rank eight as self-relative roundoff inflation. No historical result was erased, and no source or tolerance was retuned. The nine edge directions are well separated from the numerical rank cutoff on this fixed ensemble; no general theorem about arbitrary states or singular strata follows from that observation.

## Local / GitHub agreement

Maximum relative Frobenius discrepancy between independently executed local and GitHub raw matrices:

| Raw map | Maximum relative discrepancy |
| --- | ---: |
| E | 1.076585938133122e-14 |
| L | 1.6958936828758677e-16 |
| K | 9.369946572150812e-15 |
| Pi E | 9.374554748750901e-15 |
| (I-Pi) E | 1.1384778748333545e-14 |

Small numerical diagnostics are not expected to agree decimal-for-decimal. Both executions independently pass the frozen acceptance criteria. Local numerical values remain separately labeled in LOCAL_RESULT_SUMMARY.json rather than being overwritten with GitHub values.

## Interpretation and next boundary

The operational decomposition is now measured and reproducible: 243 tensorized input directions feed nine independent edge-response coordinates, of which three combinations are visible to the loop and six cancel. The loop's rank-three cap remains ordinary SO(3) product geometry. The varying 29.1%-34.8% visible squared-norm fraction is information about the state/source map E; it is not a physical energy fraction, probability, emergent spatial dimension, or gravity detection.

The next discriminator is source-law specificity: compare the selected exponential tilt with a marginally closed local-unitary null control, and separately test a conditioning-selected symmetry-breaking state ensemble. Neither comparison has been run here. The conditional retained-marginal-closure null theorem and proposed next task are in README.md.

Review was self-review, not an independent code review. The README records one unused helper edge case (explicit zero parent scale with nonzero residual); it does not affect any measured parent map. All changes are additive on the child research branch; no historical scientific source was modified and no merge into main was performed.
