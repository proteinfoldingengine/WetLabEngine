# 16.14 — Closed-network signed response: final report

**Status: COMPLETE. Verdict: CLOSED_NETWORK_NORMAL_RESPONSE.** This is a positive result for the frozen first-order simple-cycle family, not a derivation of physical geometry or gravity.

## What was learned

A continuous connected-correlation response can carry signed information into an intrinsic closed-network scalar. Every one of the 48 nonidentity order pairs has a nonzero total derivative contrast and a separately nonzero sixth-edge normal contribution in all four cycles containing edge23. All three cycles omitting that edge have zero order contrast. The full contrasts and normal contrasts are exactly odd in source coherence lambda, hence vanish at lambda=0 and reverse sign when lambda reverses. The 24 identity-middle pairs are exactly null on every cycle.

This includes all 24 nonidentity plane-arm pairs, whose sixth-edge baseline is exactly rank one. The network normal signal therefore does not require the tiny second singular direction used by the local rank-two determinant witness in 16.13. It uses the neighboring edges as an intrinsic reference. The frozen rank-two cases retain their inherited spectral qualification; no universal robustness claim follows.

## Complete cycle results

Each row reports nonzero order contrasts among 48 nonidentity pairs (24 plane, 24 isotropic).

| Cycle | Total | Normal contribution |
|---|---:|---:|
| 012 | 0 | 0 |
| 013 | 0 | 0 |
| 023 | 48 | 48 |
| 123 | 48 | 48 |
| 0123 | 48 | 48 |
| 0132 | 48 | 48 |
| 0213 | 0 | 0 |

There are 192 nonzero and 312 zero pair-cycle contrasts when the 168 identity-middle records are included. Across all individual paths, 576 of 1008 normal path-cycle derivatives are nonzero.

The other-five-edge order-contrast contribution is exactly zero in all 504 records. The sixth-edge tangent contribution is nonzero in the same 192 active contrasts. Normal and tangent terms oppose each other in 92 of those records; the total has the opposite sign to the normal term in 64. Thus the total cannot be interpreted as a pure normal response, even though the normal signal independently survives. None of the 192 active totals cancels exactly.

## Magnitudes and spectral interpretation

Absolute coefficients of lambda in the nonzero order contrasts:

| Quantity | Minimum | Maximum |
|---|---:|---:|
| Full cycle derivative | 1.56136755e-16 | 4.90923271e-9 |
| Normal contribution | 3.38274007e-17 | 3.44532479e-9 |
| Sixth-edge tangent contribution | 3.83387732e-16 | 6.55076709e-9 |
| Plane-arm normal contribution | 4.59013464e-16 | 3.44532479e-9 |
| Isotropic-arm normal contribution | 3.38274007e-17 | 1.74455359e-10 |

These are dimensionless model coefficients, not measured physical force scales. No success threshold selected them: exact rational nonzero decides the algebraic classification. The full loop derivative is polynomial, with no gap division or polar extension. The decomposition using support projectors is still conditioned on the exact baseline rank. The projected Cauchy bound is checked numerically and independently as an exact squared inequality for every path-cycle.

## Derivation and reproducibility

Read [DERIVATION.md](DERIVATION.md) for frame covariance, moving-frame cancellation, the gradient/reference contraction and rank-boundary limits. Read [PREREGISTRATION.md](PREREGISTRATION.md) for the frozen protocol and [REVIEW.md](REVIEW.md) for the independent code review and premeasurement bound correction.

- Parent publication: `18d49baad706b44abd57b1e2e1289c92b9bb2614` (complete 16.13).
- Preregistered RED commit: `bf07ca7a3812a9840a54473f1c5b043b94774469`; [expected-failure run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36503053115).
- Scientific execution head: `abb057ad4044377b4f41e7b2a08a53b3e007b14d`.
- [Successful run 36503365312](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36503365312), job `109199125907`, artifact `11006320955`.
- Six new tests and five parent tests passed. Exact counts: 144 six-edge paths, 1008 path-cycle records, 504 order contrasts. Numerical counts: 12096 rows, 80/120 digits, two independent local-frame choices, lambda=-1,0,1.
- Artifact ZIP digest, execution head and every scientific SHA256 verified before interpretation. Independent [publication verifier](verify_publication.py) reconstructed all 1008 reference contractions and exact bounds and all 504 order contrasts; [check results](PUBLICATION_CHECK.json) also certify complete numerical keys.

Maximum numeric residuals:

| Control | Maximum residual |
|---|---:|
| exact_numeric | 9.65167048e-86 |
| frame | 9.65167048e-86 |
| moving_frame | 1.93033410e-85 |
| bound | 3.01614703e-87 |
| precision | 9.77030866e-86 |

All within the preregistered 1e-35 control / 1e-30 cross-precision tolerances. The tiny positive numerical bound residual is rounding; all 1008 exact squared inequalities passed.

## Full committed evidence

[gate.py](gate.py), [tests](test_gate.py), [source manifest](SOURCE_MANIFEST.json), [full raw results, losslessly compressed](result.json.xz), [scientific checksums](SHA256SUMS), [compressed checksum](SHA256SUMS-xz), [artifact provenance](EVIDENCE.json), [test log](test.log), [parent tests](parent-test.log), [audit log](audit.log), [full successful job log](job.log), [expected RED job log](red-job.log).

Raw JSON is 14,509,911 bytes; its lossless XZ representation is 974,748 bytes. It contains every exact rational matrix, gradient, decomposition, pair contrast and numerical row; no subset replaces the full data. Reproduce with the pinned dependencies in `.github/workflows/uqcf-closed-network-response.yml`, run `python -m unittest -v` then `python gate.py` in this folder. Decode the archived raw file with Python lzma or xz to verify SHA256SUMS; the raw file is not duplicated in Git.

## Interpretation boundary and next gate

16.14 establishes an intrinsic network normal contribution within a specified CPTP model. It does not establish additional information beyond every local amplitude, source emergence, preferred geometry, transport, curvature or gravity. 16.15 will independently classify the projected reference map and compare the full order responses with the preregistered local scalar family. Time is pruning / ordered recoverability update; s denotes source-channel strength.
