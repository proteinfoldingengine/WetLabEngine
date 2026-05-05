# ADM_CAUSAL_SLICE_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## ADM-like action proxy from causal slices

## Status
**Executed structural verifier. Not Einstein-Hilbert proof.**

Verifier file:

```text
adm_causal_slice_action_verifier.py
```

Execution log:

```text
adm_causal_slice_action_verifier_run.log
```

## Captured output

```text
ADM causal slice action verifier
==================================================
Route:
h_ab sequence -> K_ab proxy + R3 proxy -> ADM-like action sum
This is not full ADM/EH convergence.

PASS: 95.0
SOFT_FAIL: 0.0
HARD_FAIL: 5.0
n_slices_median: 9.0
action_proxy_median: 1536.5295729464574
action_abs_proxy_median: 1713.2725166548257
median_volume_median: 622.8593153687095
median_K_norm_median: 0.16377724219581252
median_R3_proxy_median: 0.4512541438778868
finite_fraction_median: 1.0
```

## Interpretation

The verifier assembles:

\[
S_{\mathrm{proxy}}
=
\sum_k
\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{proxy}}
+
K_{ab}K^{ab}
-
K^2
\right).
\]

It checks finiteness and stability of the ADM-like causal-slice action ingredients.

This is not full ADM, not variationally derived, and not Einstein-Hilbert convergence.

**End of summary.**
