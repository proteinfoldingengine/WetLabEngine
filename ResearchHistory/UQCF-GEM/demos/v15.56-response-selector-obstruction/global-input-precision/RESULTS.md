# v16.01 — Global input precision audit

Verdict: **GLOBAL_INPUT_PRECISION_RECOVERY_CONFIRMED**. All validity controls passed. All eight frozen comparisons recovered at both 50 and 80 decimal digits, at the unchanged absolute rank thresholds 1e-9, 1e-10 and 1e-11.

The full 256-dimensional global Pauli calculation was rebuilt at each precision. Source channels, transformed probes and transformed preparation were independently constructed. Prescribed covariance predictions were used only for comparison. Original binary density entries and attenuation values were preserved, including their complex parts; no clipping, renormalization, rank projection or post-result threshold adjustment was introduced.

## Scientific result

| Frozen comparisons | Count | Native and transformed K rank | Native and transformed J rank |
|---|---:|---:|---:|
| Candidate 66, overlap reverse/contrast, a = 1, archived 1/3, archived 1/6 | 6 | 1 | 1 |
| Candidate 77, disjoint forward/reverse, archived a = 1/6 | 2 | 2 | 2 |

Each rank holds at all three thresholds and both precisions across the original 81 hidden columns.

| Maximum absolute Frobenius residual | 50 digits | 80 digits |
|---|---:|---:|
| Global stage covariance | 8.408293e-50 | 6.065338e-80 |
| Retained tensor covariance | 2.683207e-50 | 1.177531e-80 |
| K/J response covariance | 1.704779e-48 | 2.020564e-78 |
| Readout arithmetic identities | 7.371733e-49 | 2.116155e-79 |

Maximum 50/80 convergence discrepancy was 8.522478e-50 for global stage coefficients and 2.238591e-48 for retained/readout arrays. Native input difference from archived binary retained arrays was at most 3.212941e-16 (gate 1e-12); native response difference from the v16.00 frozen native 80-digit readout was at most 1.265358e-13 (gate 1e-9).

Both precisions passed complex state reconstruction, local channel/unitarity/trace identities, prescribed frame identities, global witnesses and hidden/one-body nulls. Readout controls retained skew rank 3, symmetric null and rank-one rejection. Original density physicality passed (minimum eigenvalue 0.02489397439321258); binary state round trips were exact.

## What this establishes

v16.00 showed that increasing precision only after the retained arrays had been rounded left all eight strict-threshold K discrepancies. v16.01 shows that rebuilding the entire global calculation at high precision removes them. Together these tests support an upstream numerical origin for those eight discrepancies, rather than a physical failure of covariance under the specified source/preparation law.

This audit does not isolate a single upstream operation. It does not recertify all 144 v15.99 rows, change its historical INVALID verdict, or change v16.00's FROZEN_INPUT_RANK_RESIDUAL_PERSISTS verdict. No new physical source-law selection, universal composition theorem, or gravity derivation follows. Time remains pruning / ordered recoverability update; geometry remains extracted from retained relations.

The next research step would be a separately preregistered full-ensemble certification using the validated global precision path, preserving the original finite-channel, erasure, scaling, covariance and domain gates. It has not been run here.

## Reproducibility and exact provenance

- Parent documentation head: `be25cd28806bea11de0b57da1a342b03c57cf28a`.
- Preregistration/test head: `7a89d1d9781ef2ffbe705044c73304c2497a5620`.
- Scientific implementation and tested head: `633e5016456a953be77c159680d8073ce4c4bf84`.
- Branch: `research/v16.01-global-input-precision`. No merge to main.
- [Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36435920620): job `108973692026`, artifact `10975965417`; absent implementation assertion verified. ZIP SHA-256 `6a17af65b510a045229ce8752ec3148c0a4753125c4663c56ab394e6443707b5`.
- [GREEN measurement run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36436733683): job `108976481377`, [artifact `10975264654`](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36436733683/artifacts/10975264654). ZIP SHA-256 `ed194e86f0d80f971e30e8f060ef8678b768ee0cec900bebd664c2f5bc135407`.
- Four tests passed in 121.154 seconds. The standalone measurement independently emitted the same scientific verdict; the exact job log was read, not inferred from workflow status.
- `gate.py` SHA-256: `1f5de072b35561768f054b8cb59200e5814f7cff66a22bfa0fc42e2facc52c80`.
- Raw `result.json` SHA-256: `8308d457346e42755697228c4877db2b28eeedb93f6f3c9a16d551aa4449b7ba` (11,492,280 bytes).
- Deterministic `RESULT.json.gz` SHA-256: `fb34a2a3ae5197983d41e66fd44505b59c500f063d1e80cf6417059537f075ff` (1,881,757 bytes); Git blob `d52e33b60235a04a3cb4bef4353b65cddb2594ae`.

Both downloaded archive digests, execution heads, preregistration/derivation/test source bytes, measurement implementation bytes and every SHA256SUMS entry were verified. Each manifest entry matched the exact measurement job log. Independent code review found no blocking defects; it did not execute measurements.

Run from this folder with Python 3.11, numpy 2.3.5, sympy 1.13.3, mpmath 1.3.0 and OPENBLAS_NUM_THREADS=1:

```bash
python -m unittest -v test_gate
python gate.py > result.json
```

`SUMMARY.json` contains per-case ranks and precision metrics; `RESULT.json.gz` includes native/transformed retained inputs and response arrays. `EVIDENCE.json`, `SHA256SUMS`, `RED_TEST_LOG.txt`, and `TEST_LOG.txt` preserve machine-readable provenance and tests. The publication commit is identifiable as the commit adding this report; the tested scientific head above is distinct from that documentation commit.
