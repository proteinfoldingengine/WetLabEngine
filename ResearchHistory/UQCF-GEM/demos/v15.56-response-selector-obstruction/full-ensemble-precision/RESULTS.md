# v16.02 — Full-ensemble precision results

Status: completed; both preregistered scientific predicates confirmed.

## Authoritative execution

- Tested commit: `ccc65c5569e904be3c98ec61e3d231f8e693eb92`.
- [GitHub Actions run 36440529651](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36440529651), job `108989510349`, attempt 1.
- Completed 2026-09-28 at 15:24 UTC (08:24 America/Phoenix).
- All five tests passed; test execution took 1271.526 seconds.
- [Complete raw results, source snapshot, logs and checksums](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36440529651/artifacts/10978763246).
- Artifact ID: `10978763246`; size: 26,065,099 bytes. GitHub reports expiration 2026-12-27; this committed report and EVIDENCE.json persist independently of that artifact retention window.

## Measured result

The downloaded result.json reports:

```json
{
  "version": "16.02",
  "all_valid": true,
  "verdict": "FULL_ENSEMBLE_EB_RESPONSE_SCALING_CONFIRMED",
  "erasure_verdict": "FULL_ENSEMBLE_ERASURE_POLAR_UNDEFINED_CONFIRMED",
  "scaling_predicate": true,
  "erasure_predicate": true
}
```

The frozen ensemble contains all 12 candidate states and 81 probe columns, evaluated at 50 and 80 decimal digits. All 192 rows were recorded: 144 positive-attenuation rows and 48 complete-erasure rows. Rank covariance and cross-precision rank/domain agreement passed at both precisions.

Response covariance residuals were approximately 5.0121e-48 (50 digits) and 2.6970e-78 (80 digits), below the frozen 1e-35 bound. Cross-precision response convergence was approximately 5.2570e-48, below 1e-30. The legacy physicality replay recorded 344,604 checks and passed; all legacy non-rank controls passed. Its historical rank-covariance failure and INVALID verdict remain recorded, rather than being retrospectively changed.

This closes the full-ensemble numerical precision certification under the frozen source and preparation laws. Complete erasure has undefined polar response, not an assigned rank-zero response. No universal source-law selection, surviving reference entanglement, fully classical process, or gravity derivation is established. Time is pruning / ordered recoverability update.

## Evidence verification

On 2026-09-28 the final job log and downloaded ZIP were inspected. The ZIP SHA256 matched GitHub's artifact digest; all six SHA256SUMS entries matched the extracted bytes. execution_head.txt matched the tested commit. Git blob hashes for PREREGISTRATION.md, SOURCE_MANIFEST.json, gate.py and test_gate.py matched the published branch source. The decompressed legacy result hash matched the value recorded in result.json. The measured JSON's row counts and verdicts were inspected directly.

ZIP SHA256: `6fbcd695d037956e980f9a4fcd6a1f64c97120a2e5aee5208e140479950c0e7e`.

result.json SHA256: `6b0e8e5a143df5c7ece910e1b3d9fe7204d916ea2cdce7f181ccc1f12ebe9eb9`.

The earlier run 36440369786 at e058fcd15ac8b27ab77b879036daa6c7974ddc56 is superseded, as documented in REVIEW.md. This publication adds documentation only and does not change the tested implementation or merge to main.
