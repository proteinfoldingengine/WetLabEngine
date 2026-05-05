# SLICE_ALIGNMENT_AND_SHIFT_VERIFIER_SUMMARY.md

# Verifier Summary
## Shift proxy from aligned adjacent antichain slices

## Status
**Executed structural verifier. Shift remains proxy-level.**

Verifier file:

```text
slice_alignment_and_shift_verifier.py
```

Execution log:

```text
slice_alignment_and_shift_verifier_run.log
```

## Captured output

```text
Slice alignment and shift verifier
==================================================
Route:
adjacent antichain profiles -> matching -> Procrustes alignment -> shift vector proxy

PASS: 86.0
SOFT_FAIL: 0.0
HARD_FAIL: 14.0
n_slice_pairs_median: 9.0
match_count_median_median: 34.0
match_score_median_median: 0.8910400734116303
aligned_shift_norm_median_median: 1.6389851443624852
hidden_shift_corr_median: 0.07464960762180159
procrustes_residual_median_median: 1.8627013178170457
```

## Interpretation

The verifier replaces raw centroid drift with:
- causal-profile matching,
- graph embedding alignment,
- Procrustes residual control,
- matched displacement shift proxy.

This is structurally better than the prior centroid shift, but it is not yet a covariant ADM shift.

**End of summary.**
