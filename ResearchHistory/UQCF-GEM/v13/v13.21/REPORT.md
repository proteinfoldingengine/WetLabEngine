# UQCF-GEM v13.21 — Recoverability Atlas Telemetry / Blind Refinement Protocol Gate

**Date:** 2026-09-12

## Adjudication

**RATS PROTOCOL: FROZEN / HASHED**

**RATS EXECUTION: BLOCKED — GENUINE NESTED QUANTUM REFINEMENT FAMILY MISSING**

No refinement telemetry was generated.

Protocol SHA-256:

`b46bec9868fd8c71a2789801d4d9eca733e187608b8f364b99721cfafd24227b`

v13.20 derived continuum thresholds, so the next trustworthy move is to freeze the experiment before seeing any exponent. The current v13 architecture does not yet contain a target-independent rule that produces ancestry-linked quantum states `rho_h` across nested resolutions. Inventing that law inside the scoring gate would contaminate the test.

## Frozen nested-family contract

The experiment requires at least four dyadically nested levels:

`h_r = h_0 / 2^r`.

Every level must represent the same physical relational configuration, with:
- a declared fine-to-coarse ancestry map;
- the same ancestry-tracked target edge;
- a frozen separator partition `A|B|C`;
- a source continuation fixed independently of all RATS scores;
- reproducible raw state/marginal data and hashes.

Independent random states at each `h` are forbidden.

## Canonical recovery

The primary recovery is the faithful-state Petz map:

`R_B->BC(X) = rho_BC^(1/2) rho_B^(-1/2) X rho_B^(-1/2) rho_BC^(1/2)`.

The recovered state is:

`rho_rec_ABC = (id_A tensor R_B->BC)(rho_AB)`.

No rotated-Petz, variational, or best-of recovery search is allowed in the primary score.

If a required marginal is not faithful, that level is a conditioning failure rather than an invitation to tune a pseudoinverse threshold.

## Frozen telemetry

Every refinement level records:

1. `I(h) = I(A:C|B)`;
2. `gamma(h)`, the smaller true/recovered target polar singular floor;
3. `mu(h)`, the relevant true/recovered faithfulness floor;
4. `epsilon(h) = ||O - O_rec||_F`;
5. `eta(h) = ||dot O - dot O_rec||_F`;
6. `Lambda(h) = max(||dot O||_F, ||dot O_rec||_F)`;
7. `p(h) = ||P_h||_op`.

The same source `P_h` is applied to the true and recovered states.

## Frozen information-theoretic score

Adjacent exponents are scored conservatively.

Let:
- `alpha_min` be the minimum adjacent CMI exponent;
- `beta_max` the maximum adjacent polar-gap closing exponent;
- `sigma_min` the minimum source-norm exponent;
- `lambda_min` the minimum true-edge-jet exponent.

The v13.20 conditions remain unchanged.

Value-level boundedness requires:

`alpha_min >= 2 beta_max + 2`.

Jet locality requires both:

`alpha_min >= 4 beta_max + 2 - 2 sigma_min`

and

`alpha_min >= 2 beta_max + 4 - 2 lambda_min`.

Strict inequalities are recorded only as finite-family compatibility with vanishing error, not as proof of an asymptotic law.

## Independent direct-error score

The measured edge errors are scored directly as a second path.

If:

`epsilon(h) ~ h^(p_epsilon)`

and

`eta(h) ~ h^(p_eta)`,

then bounded macroscopic composition requires:

`p_epsilon >= 1`

for value geometry,

`p_eta >= 1`

for the local jet term, and

`p_epsilon + lambda_min >= 2`

for the context/holonomy-jet term.

This is an independent cross-check that bypasses looseness in the analytic recoverability constants.

## Numerical governance

Primary jets use the analytic/Frechet QMAR differential.

A finite-difference fallback is allowed only if its step schedule and Richardson consistency check are frozen before telemetry exists.

No step can be adjusted after seeing a desired exponent.

Likewise:
- numerical floor hits do not become infinite exponents;
- exact zero must be algebraically certified;
- separator width cannot change after seeing CMI;
- the source cannot be renormalized after seeing the score.

## Architecture audit

The current v13 branch contains exact/locality theorems, finite-dimensional quantum controls, and synthetic refinement power-law checks.

But the repository audit found no existing implementation of:
- a genuine ancestry-linked `rho_h` family;
- a pre-existing quantum coarse-graining/restriction map;
- a frozen physical source continuation across that quantum family.

The older ADM-7 refinement branch does not fill this gap. It supplies a matched current/carrier continuation, not the quantum-state telemetry required here, and its frozen continuation failed its own ACR continuum gate.

Therefore the correct result is:

**DO NOT GENERATE RATS DATA YET.**

## Scientific meaning

This prevents a subtle circularity.

v13.20 tells us what exponent would make the recoverability atlas work. Choosing how to refine the quantum state after seeing those exponents would make a passing result scientifically weak.

So the frozen order is:

`derive quantum refinement law -> freeze implementation/hash -> generate nested states -> run already-frozen RATS scorer`.

The continuum question remains open, but it is now experimentally well posed.

## Status

- RATS protocol: **FROZEN / HASHED**
- canonical recovery: **FROZEN**
- six telemetry streams: **FROZEN**
- v13.20 thresholds: **UNCHANGED**
- direct-error cross-check: **FROZEN**
- genuine nested quantum refinement family: **MISSING**
- RATS execution: **BLOCKED**
- continuum recoverability atlas: **NOT CERTIFIED**
- Pillar 3: **OPEN**

No scientific breakthrough is declared.

This is a **trust-preserving protocol freeze and execution-boundary result**.

## Next — v13.22

### Quantum Refinement Naturality / Nested-State Law Gate

The next missing object is not another scorer.

We need a target-blind law `rho_h <-> rho_(h/2)` already justified by the pre-time ontology.

It must:
1. provide explicit ancestry;
2. preserve the declared physical source geometry;
3. commute appropriately with retained-observable restriction;
4. respect positivity and normalization;
5. compose consistently across two refinement steps;
6. contain no RATS/CMI/continuum target in its derivation.

Only after that law is derived or recovered should the sealed v13.21 protocol be executed.
