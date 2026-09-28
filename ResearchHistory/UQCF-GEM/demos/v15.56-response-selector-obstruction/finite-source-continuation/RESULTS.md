# v16.03 — Finite-source cubic order response: completed

**DISJOINT_CUBIC_RESPONSE_DETECTED** and **FINITE_GRID_OVERLAP_RESPONSE_CONFIRMED**. All 12 candidate jobs passed all frozen validity controls. All 48 entanglement-breaking cubic cases are resolved-active; none are numerical-null or unresolved. There were no polar-domain exits in the fixed grid.

## What was learned

Two disjoint source channels commute when composed directly. When the specified attenuation channel is placed between them, their finite protocols can nevertheless carry order-dependent hidden-information response in loop invariants. The source-origin quadratic contrast is zero, but the analytically differentiated cubic coefficient is nonzero in every tested EB case.

The measured coefficient is T = D²F(C0)[Vf−Vr,B], in the expansion ΔJphysical(λ)=λ³T+O(λ⁴). T was obtained by differentiating the polar/Sylvester equations, not by fitting an exponent. The independent directional finite-difference check passed. This is a coefficient of the hidden-input response, not the raw difference between baseline loop invariants.

| Intermediate attenuation | Preparation | Cases | Cubic T ranks at 1e-9 / 1e-10 / 1e-11 |
|---|---|---:|---|
| 1 (identity control) | Planar | 12 | 0 / 0 / 0 |
| 1 (identity control) | Isotropic | 12 | 0 / 0 / 0 |
| Archived binary 1/3 | Planar | 12 | 3 / 3 / 3 |
| Archived binary 1/3 | Isotropic | 12 | 3 / 3 / 3 |
| Archived binary 1/6 | Planar | 12 | 3 / 3 / 3 |
| Archived binary 1/6 | Isotropic | 12 | 3 / 3 / 3 |

These ranks agree in native/transformed frames and at 50/80 digits. The identity-middle-channel disjoint contrast remains null. Complete erasure remains an undefined polar readout, not an assigned zero response.

## Finite protocols and controls

All 12 frozen states and all 81 weight-four probes were used. There are 144 origin configurations and 720 finite configurations per precision, evaluated for both source orders and both frames. The fixed mixture parameters were λ=1/16,1/32,1/64,1/128,1/256. All 360 overlapping-source finite configurations retain nonzero normalized invariant contrast. No step was shortened or excluded to obtain a pass.

The result JSON preserves all finite centers' correlation matrices, edge singular values and references, normalized and physical response matrices, cubic matrices, singular spectra, ranks and remainder data. The five finite-step remainders are descriptive measurements; this result does not claim a fitted exponent or a uniform Taylor remainder bound.

| Maximum validation residual | Value |
|---|---:|
| Invariant-response covariance, 50 digits | 1.25057e-47 |
| Invariant-response covariance, 80 digits | 8.11692e-78 |
| 50/80-digit response discrepancy | 1.27654e-47 |
| Independent mixed-derivative check (normalized) | 6.78871e-12 |
| Mixed-derivative symmetry, 50 digits | 2.13822e-50 |
| Identity-middle-channel order null, 80 digits | 1.13411e-78 |

Covariance uses the frozen 1e-35 bound; cross-precision comparison uses 1e-30; the independent directional check uses 1e-5. Every source/preparation, physicality, hidden-null, rank/domain-agreement and finite-value control passed. The numerical rank tests and singular-value domain checks were retained unchanged. Historical INVALID verdicts remain unchanged.

## First-principles interpretation

The experiment demonstrates order-sensitive access to initially pair-invisible global information under the specified physical source and preparation laws, including an intermediate entanglement-breaking cut. It closes the finite-source gap identified after 16.02.

This does not make the disjoint sources themselves noncommuting. The inserted channel changes the full protocol, and the geometric readout is evaluated at different finite centers. CPTP composition remains associative. The source-to-world law and correlation-to-geometry extraction are still specified inputs; this is not a universal coupling, a derivation of gravity, or evidence selecting those inputs from global compatibility alone. Time remains pruning / ordered recoverability update.

A useful next research question is whether the coefficient factors entirely through the inserted-channel commutators and the chosen readout's Hessian. Resolving that would separate a consequence of the specified operations from evidence for a more intrinsic source law. No 16.04 measurement has been run here.

## Reproducibility and publication

- Preregistration head: `150d9fe908d9480d54e0ec820ed2e1c9aa036473`.
- Expected RED: [run 36449687457](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36449687457), controls job 109020926196. Five explicit absent-implementation failures were inspected; measurement was skipped.
- Tested implementation: `850dc3538f04ce9efcb3e974fa04992bcb1cb150`.
- GREEN measurement: [run 36450083481](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481). Seven regression tests and all 12 candidate jobs passed.
- The two reporting tests additionally reject incomplete/duplicate ensembles and preserve INVALID overrides; nine local tests passed in total.
- All 12 downloaded ZIP digests, execution heads and all 60 SHA256SUMS entries were verified, and the complete JSON was inspected and aggregated. EVIDENCE.json records artifact IDs, raw hashes and exact job identities; full job logs are included.
- Full raw results are available through the twelve Actions artifacts below; permanent repository copies are being finalized. The `result-<candidate>.json.gz` files are byte-identical downloaded compressed scientific results. SUMMARY.json is generated by summarize.py and includes every 80-digit configuration. Publication is additive on `research/v16.03-finite-source-continuation`; no merge to main.

From this directory, with the pinned workflow dependencies installed:

```bash
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py --candidate 13
# Repeat for 16,22,25,27,29,37,39,46,50,66,77.
python summarize.py . --output SUMMARY.json
python -m unittest -v test_summary
```

Candidate jobs return success for valid scientific negative outcomes too; a green CI label alone is not the scientific verdict. The explicit JSON predicates above are the observed result.

## Complete raw result artifacts

| Candidate | Complete artifact |
| --- | --- |
| 13 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10982763221) |
| 16 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10984071808) |
| 22 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10983527304) |
| 25 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10983058663) |
| 27 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10984116578) |
| 29 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10982808100) |
| 37 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10983798197) |
| 39 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10984007890) |
| 46 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10983224074) |
| 50 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10982689709) |
| 66 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10984200394) |
| 77 | [Download](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36450083481/artifacts/10982909554) |
