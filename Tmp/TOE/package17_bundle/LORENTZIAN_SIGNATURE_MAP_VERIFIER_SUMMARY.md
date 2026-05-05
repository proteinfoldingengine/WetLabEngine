# LORENTZIAN_SIGNATURE_MAP_VERIFIER_SUMMARY.md

# Verifier Summary
## Lorentzian signature reconstruction

## Status
**Executed structural verifier. Not a causal-set or GR proof.**

Verifier file:

```text
lorentzian_signature_map_verifier.py
```

Execution log:

```text
lorentzian_signature_map_verifier_run.log
```

## Captured output

```text
Lorentzian signature map verifier
==================================================
Candidate tested:
time-oriented coordinates + positive lapse/geometry scales + adjacency
-> signed interval relation
-> local symmetric metric estimate
-> signature check: one negative, three positive

Sweep results:
PASS: 94.0
SOFT_FAIL: 0.0
HARD_FAIL: 6.0
valid_fraction_median: 1.0
signature_fraction_median: 1.0
cond_median: 1.5625773434744308
metric_variation_median: 0.5218283833020964
valid_fraction_min: 1.0
```

## Interpretation

The verifier tests whether signed interval data with a time-oriented coordinate can support a local metric fit with signature:

\[
(-,+,+,+).
\]

It confirms structural viability for the local Lorentzian-signature reconstruction in sampled regimes.

It does not prove:
- microscopic origin of time,
- causal-set emergence,
- coordinate independence,
- curvature convergence,
- or Einstein-Hilbert emergence.

**End of summary.**
