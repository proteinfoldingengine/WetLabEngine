# v16.00 — frozen-input precision audit

**Verdict: FROZEN_INPUT_RANK_RESIDUAL_PERSISTS.** The audit is valid, but the preregistered readout-only recovery hypothesis fails for all eight comparisons. CI is GREEN because the tests correctly accept a valid negative scientific result. v15.99 remains historically **INVALID**.

All eight discrepancies survive independently evaluated 50- and 80-digit readouts of the same rounded retained tensors. Exact prescribed-frame transport controls recover the expected ranks. The discrepancy is therefore present in the frozen retained inputs; increasing precision only after those inputs have been formed is insufficient. This audit does not identify the particular upstream operation responsible.

## Provenance

Repository: proteinfoldingengine/WetLabEngine. Branch: research/v16.00-precision-readout-audit. No main merge.

| Item | Exact identity |
|---|---|
| Published v15.99 parent | 64a294845b36877d08c0ef90c87bdec1e1800e58 |
| Preregistration/tests | ab94d0ebc5ac1247cd30d385a6f67ede41e755a9 |
| Clean RED workflow head | 8f92f9272124f93a243a5aa39dac88cf85527116 |
| Tested scientific implementation | 7ed1b65c86700b6b4fd17bd366262c48cdae38d8 |
| Initial RED run / job / artifact | 36430646746 / 108955642285 / 10972964828 |
| Clean RED run / job / artifact | 36430853798 / 108956342728 / 10973735786 |
| GREEN run / job / artifact | 36431426627 / 108958306641 / 10974221343 |

[Clean RED](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36430853798), [GREEN execution and scientific NO](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36431426627), [measurement artifact](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36431426627/artifacts/10974221343).

The initial RED correctly hit the absent-implementation assertion, then the evidence-capture workflow attempted to parse an empty JSON file. A workflow-only guard fixed that secondary error before any scientific implementation. The clean RED failed solely for the expected absent implementation. The preregistration and tests were unchanged. All four frozen tests subsequently passed in 32.062 seconds.

| SHA-256 object | Digest |
|---|---|
| Initial RED archive | f9098c06e7830ac34abbc186b7d4f247dea6e396cea444b76b42f718b3c23dfe |
| Clean RED archive | e7173cb8fe7ff1b4e19f6af9af7bb412931838e8cb3a1c1e19457efcdecdbea1 |
| Measurement archive | b93d2d24334ce903524abd22c9d96dc2108c5a54b864ebb50bb126fdf3ac0018 |
| gate.py | 7eeead6262372ac6e57fc1a39d90775bd883227c017285997079c8fd70261fab |
| Raw result JSON | 7d2fcc55c51474f12ac596ca5321d6a8e22265560066d64ded61e945ffd0fd24 |
| RESULT.json.gz | ccebbb43faf27b7c5d8825e9b53571067ca40011c575618119f059550effa4a2 |

Downloaded archive digests, execution heads, frozen files, and every manifest checksum were verified. The exact job log explicitly reports all_valid=true, recovery_predicate=false and the negative verdict. All eight canonical retained-input hashes were also checked. Raw JSON is 5,935,776 bytes; deterministic gzip is 957,761 bytes. EVIDENCE.json, SUMMARY.json and the saved test logs contain the audit trail.

## Measurement and controls

The eight previously failing comparisons cover candidate 66 overlapping-source reverse/contrast responses at a=1,1/3,1/6, and candidate 77 disjoint-source forward/reverse responses at a=1/6. All 81 hidden directions and the original absolute rank thresholds 1e-9,1e-10,1e-11 remain fixed.

The NumPy calculation reproduces archived native matrices and transformed spectra with measured difference exactly 0 and identical rank lists. Complex state decoding and retained-array binary roundtrips are exact. The largest state imaginary entry is 0.011805506343391585, so retaining complex components is a substantive check.

At each precision the independent solver evaluates native rounded inputs, transformed rounded inputs, and exact-frame transported native inputs: 48 complete K/J readouts in total. It uses the inherited two-leading-singular-vector completion, retains the signed P=sym(R^T C), and independently solves the skew Sylvester equation in a three-dimensional axial basis. It does not project K/J, clip P, or force an input to exact rank two.

All skew positive controls recover rank 3, symmetric controls return zero, and rank-one input is rejected. Maximum arithmetic identity residual is 6.96092e-49. Maximum 50/80-digit matrix disagreement is 2.61204e-48, far below the frozen 1e-30 convergence bound. Exact-frame covariance residuals are at most 2.16805e-48 across both precisions, and 3.46433e-78 at 80 digits.

## Persistent spectra

Each row below still crosses only the original 1e-11 threshold. Native and exact-frame-control ranks agree at every threshold and both precisions. J ranks agree throughout. Values shown are from the 80-digit output; the 50-digit output gives the same rank lists.

| Candidate | a | Pair / response | Expected K rank | Frozen-input K rank at 1e-11 | Extra singular value |
|---|---|---|---|---|---|
| 66 | 1 | overlap / reverse | 1 | 2 | 1.35174e-11 |
| 66 | 1 | overlap / contrast | 1 | 2 | 1.34884e-11 |
| 66 | 1/3 | overlap / reverse | 1 | 2 | 1.09309e-11 |
| 66 | 1/3 | overlap / contrast | 1 | 2 | 1.09448e-11 |
| 66 | 1/6 | overlap / reverse | 1 | 2 | 1.57418e-11 |
| 66 | 1/6 | overlap / contrast | 1 | 2 | 1.57543e-11 |
| 77 | 1/6 | disjoint / forward | 2 | 3 | 1.89917e-11 |
| 77 | 1/6 | disjoint / reverse | 2 | 3 | 1.89900e-11 |

Frozen-input covariance residuals remain between 1.09537e-11 and 2.26344e-11. The small differences from v15.99's float64 spectra do not remove any threshold crossing.

Compared with exact prescribed transport of native inputs, the rounded transformed arrays differ by at most 2.55064e-16 in C, 2.66351e-16 in source-C and 2.82854e-15 in the full mixed derivative array. The per-case maximum third C singular value over the five readout edges ranges from 1.07064e-16 to 1.31715e-16; tiny negative eigenvalues of signed P are retained and reported. These are input defects at the rounding scale, not failed high-precision arithmetic identities.

## What this establishes

The hypothesis that higher precision in the polar/Sylvester/loop readout alone would remove the eight discrepancies is rejected. The same frozen inputs carry the residual through an independent, converged evaluator. Exact-frame controls show that the prescribed tensor covariance is recovered when the input relation itself is preserved to high precision.

This localizes the problem upstream of the readout boundary without isolating a particular matrix multiplication, channel evaluation, correlation extraction or transport operation. The control transports retained tensors; it is not an independent global quantum/source calculation. No full v15.99 re-certification is earned, and its INVALID verdict is unchanged. The identity-channel case a=1 still participates, so this is not evidence of an EB-induced physical obstruction.

The next justified experiment is an end-to-end precision/identity audit that forms the global states, source derivatives, intermediate channel and retained correlations at high precision before readout. It should freeze the same cases and thresholds, inspect intermediate identities, and preserve this negative result. That experiment has not been run here.

No fundamental time, fitted alignment, primitive geometry, physical source-law selection, or gravity derivation is introduced. Genesis Pin and ordered recoverability remain unchanged.

## Reproduction

Check out 7ed1b65c86700b6b4fd17bd366262c48cdae38d8, install the pinned workflow dependencies, set OPENBLAS_NUM_THREADS=1, and run python -m unittest -v test_gate followed by python gate.py in this directory. The script emits the complete audit JSON and exits 0 for this valid negative outcome. RESULT.json.gz includes binary-hex retained inputs, their hashes, full precision matrices, spectra, input diagnostics and per-case predicates.
