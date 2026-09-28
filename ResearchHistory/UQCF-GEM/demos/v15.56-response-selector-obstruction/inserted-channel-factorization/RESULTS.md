# v16.04 — Inserted-channel factorization: completed

**FACTORIZATION_CONFIRMED**. All 12 candidates passed the frozen validity controls. The independent Pauli-weight construction reproduces the archived v16.03 cubic matrices in both frames and at both precisions.

## What was learned

The audit confirms the mechanism derived in [DERIVATION.md](DERIVATION.md):

T = T_D - T_A,

T_X = D²F(C0)[DC(z0)[Q [L_X,M_a] rho], B_a].

The global commutator is constructed independently by explicit Pauli-index replacement and factors a^weight(input)-a^weight(output). The connected differential is independently indexed and includes both one-body-product derivatives. The polar Hessian evaluator is inherited from v16.03; this is an independent audit of its input mechanism, not a second independent polar solver.

The decomposition reveals an asymmetry: in all 48 EB configurations, T_A is resolved-active with ranks 3/3/3, while T_D is numerically null with ranks 0/0/0. The total T has ranks 3/3/3 and agrees with -T_A at the frozen tolerance. The native 80-digit cancellation ratio range is ['1.0', '1.0']; here the ratio is ||T_D-T_A||/(||T_D||+||T_A||), not a fitted statistic.

| Middle channel | Coefficient | Active | Numerical null | Unresolved |
| --- | --- | ---: | ---: | ---: |
| identity | T_D | 0 | 24 | 0 |
| identity | T_A | 0 | 24 | 0 |
| identity | T | 0 | 24 | 0 |
| EB | T_D | 0 | 48 | 0 |
| EB | T_A | 48 | 0 | 0 |
| EB | T | 48 | 0 | 0 |

Counts above use native 80-digit configurations; ranks and classifications agree in transformed frames and at 50 digits. Both preparations are included. Identity-middle cases are null for both source contributions and their difference.

This does not yet identify where the D direction is lost. The archived connected-direction norms include all six pair edges, whereas the loop Hessian uses only the five declared geometry edges. A nonzero six-edge norm therefore does not establish a nonzero input to the five-edge Hessian. Distinguishing edge omission from a Hessian kernel is the next mechanistic question; this report does not claim it has been resolved.

## Coverage and checks

The run covers all 12 frozen states, all 81 hidden probes, the plane and isotropic preparations, and archived binary attenuation values 1, 1/3 and 1/6. It evaluates 72 configurations per precision in two frames at 50/80 digits: 288 frame-specific configurations, each with T_D, T_A and T matrices. No source, state, preparation, alignment, threshold or fit was changed. This is a coefficient audit; the finite-lambda sweep remains the v16.03 result.

| Maximum residual | Value |
| --- | ---: |
| Parent cubic discrepancy, 50 digits | 1.653358e-48 |
| Parent cubic discrepancy, 80 digits | 1.331120e-78 |
| Direct-protocol cubic discrepancy, 80 digits | 5.043935e-79 |
| Response covariance, 80 digits | 7.821884e-78 |
| Retained-direction covariance, 80 digits | 1.332693e-82 |
| Cross-precision discrepancy | 1.280578e-47 |
| Affine-readout null, 80 digits | 4.047971e-79 |

Within-precision controls use absolute Frobenius tolerance 1e-35; cross-precision comparisons use 1e-30. Every source-lift, commutator, connected differential, global/retained covariance, hidden-null, affine-readout, arithmetic-identity and coefficient-reconstruction check passed. The identity-middle and weight-preserving-block residuals are zero in the archived outputs. All evaluated origin geometries passed the unchanged spectral-domain checks. Complete erasure remains undefined polar geometry and is excluded, never assigned zero.

## First-principles scope

The result explains the observed coefficient within ordinary associative channel composition, the inserted attenuation operation and the nonlinear readout. The numerical agreement supports the specified mechanism; it does not select the source/preparation laws, establish universal coupling or derive gravity. Geometry remains extracted from retained relations; time remains pruning / ordered recoverability update. Historical INVALID results remain unchanged.

A useful next step is an exact support audit of the D direction: project its connected derivative onto the five readout edges before evaluating the Hessian. If that projection vanishes, the asymmetry is explained at the retained-edge stage. If it survives, inspect the Hessian contraction with the common hidden tangent. These alternatives must not be conflated.

## Reproduction and evidence

- Frozen protocol: [PREREGISTRATION.md](PREREGISTRATION.md), commit 1273637d90bfc71b90f22f377c877f08ec8b96dc.
- Expected RED: [run 36479322504](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36479322504), controls job 109120785455. Exact logs show six absent-implementation failures; measurement was skipped.
- Tested implementation: 1b14035ab727b1f07a40c01498f91ad7fd0f3aac.
- GREEN: [run 36480147334](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334). Six new controls, nine parent tests and all 12 candidate jobs passed.
- Independent implementation review closed a prepared/connected-direction control gap before measurement. Independent reporting review closed INVALID-exit and rank/classification-validation gaps. Five reporting regression tests passed locally after their expected failures.
- All 12 ZIP digests, execution heads and all 60 SHA256SUMS entries were verified. The complete JSON matrices and controls were parsed and aggregated. Exact job logs, SHA256SUMS files and all twelve byte-identical raw gzip results are archived in this directory.
- [SUMMARY.json](SUMMARY.json) gives aggregate counts, residuals and per-configuration decomposition; [EVIDENCE.json](EVIDENCE.json) records artifact hashes and job identities. [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) pins inherited code and parent results.

With the workflow's pinned dependencies installed, from this directory:

```bash
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate test_summary
OPENBLAS_NUM_THREADS=1 python gate.py --candidate 13
# Repeat for 16,22,25,27,29,37,39,46,50,66,77.
python summarize.py . --output SUMMARY.json
```

The reporter deliberately checks the archived execution head. A new reproduction commit has a different head and must be documented as a new run, not relabeled as this measurement.

| Candidate | Permanent repository copy | Original artifact |
| --- | --- | --- |
| 13 | [Raw result](result-13.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996427226) |
| 16 | [Raw result](result-16.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10995778180) |
| 22 | [Raw result](result-22.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996762068) |
| 25 | [Raw result](result-25.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10995953131) |
| 27 | [Raw result](result-27.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996742102) |
| 29 | [Raw result](result-29.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10997061921) |
| 37 | [Raw result](result-37.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996212550) |
| 39 | [Raw result](result-39.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996797563) |
| 46 | [Raw result](result-46.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10995898940) |
| 50 | [Raw result](result-50.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996063797) |
| 66 | [Raw result](result-66.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996308033) |
| 77 | [Raw result](result-77.json.gz) | [Actions artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36480147334/artifacts/10996453079) |

Publication is additive on research/v16.04-inserted-channel-factorization; no merge to main.
