# Sprint I — Spectral chain benchmark note

## Purpose
Benchmark the operator-derived spectral chain under three structural truncations:

1. shell-only
2. shell + microstate return, no cross coupling
3. full shell + microstate + cross coupling

The chain being tested is:

L_coh(gamma) -> P(tau; gamma) -> D_spec(tau; gamma) -> sigma(gamma) -> F(gamma)

## Benchmark grid
gamma = [0.18, 0.22, 0.26671093, 0.3, 0.36]
tau = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

## Calibration note
The affine sigma-map is calibrated on the FULL operator only:
- sigma(gamma*) = 1 - gamma*
- sigma(0.36) = 0.75

This is explicit and local. It is not claimed as a unique fundamental normalization.

## What to look for
- whether the full mode preserves the crossing structure near gamma*
- whether shell-only and full modes separate clearly in D_spec, spectral gap, and F(gamma)
- whether D_spec and the spectral gap have stable monotone trends as gamma varies
