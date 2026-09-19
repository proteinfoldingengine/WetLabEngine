# UQCF-GEM v15.38 — Pre-Time Response-Function Axiom Admissibility / Falsifiability Gate

**Date:** 2026-09-18
**Base:** v15.37 exact certified head `2d7950d7c151a386654e044af6d092bf68317c59`
**Inherited frontier:** `T=f(A)`, canonical `A`, response function irreducible relative to audited frozen ontology
**Pillar 3:** OPEN

## Purpose

v15.37 stops the search for a hidden frozen selector. v15.38 does not choose f(A). It defines the hard admissibility contract any NEW pre-time response principle must pass before downstream gravity tests are allowed.

## Candidate type

A candidate must define one family-level rule `T_L=f(A_L)` on the canonical nearest-neighbor adjacency of independently rebuilt odd-L periodic pre-time complexes.

The rule must be frozen before any holonomy, inverse-square, Newton, ADM/GR, cosmology or observer-fit score is evaluated.

## Hard admissibility requirements

### A. Correct carrier typing
Act directly through the certified cycle carrier and canonical A_L. No arbitrary embedding, reshaping, PCA/SVD alignment, random isometry, unearned Hodge metric or new intertwiner.

### B. Exact covariance
Verify exact relabeling/translation/D4 covariance on L=5,7,9.

### C. Family naturality across finite size
One formula must apply unchanged across L=5,7,9. Reject an L=7 sector lookup, coefficients obtained by interpolating the ten L=7 sectors, or any law whose form changes with L.

### D. Spectral-edge exclusion
An admissible candidate may not be chosen or parameterized from an extremal eigenvalue, smallest spectral gap, near-degenerate edge, extremal sector ID, or resonance observed only after inspecting the finite spectrum. A future theorem-defined spectral law is not categorically banned, but its form and parameters must be fixed independently of the tested instance.

### E. Target independence
Candidate definition may not use remote holonomy, long-range appearance, inverse-square quality, Newtonian fit, GR/ADM residual, cosmological fit, or any downstream geometry score.

### F. No hidden metric/minimum-action selector
No minimum norm, Hodge pseudoinverse, smoothness, radiality, minimum action, or edge weights not already canonically derived.

### G. Pre-time compatibility
No pruning, entropy, physical duration, clock time, ADM lapse/shift, or actual-outcome selection as an upstream response selector.

### H. Projective-scale discipline
Absolute normalization remains underived. Candidate laws are compared up to positive overall scale unless a separately certified calibration law is supplied.

### I. Falsifiability declaration
Before downstream testing, freeze the formula/parameters, carrier/domain, size-family domain, at least one structural falsifier independent of gravity, and at least one prospective downstream test not used to construct the law.

### J. Null/exact controls
Zero input maps to zero; cycle carrier is preserved; covariance is exact; rule is deterministic; no hidden data-dependent parameter fitting.

## Accepted control candidates — new-axiom controls only

F1: `f(x)=x`
F2: `f(x)=1+x^2`
F3: `f(x)=x-x^3/16`

These are not adopted physical laws. For L=5,7,9 verify the same exact coefficient vector, carrier preservation, covariance, zero spectrum queries, zero spectral-edge tuning, and pairwise projective inequivalence on L=7.

## Rejection controls

1. `L7_SECTOR_LOOKUP` — reject for finite-size/family-naturality failure.
2. `SPECTRAL_EDGE_TUNED` — reject for spectral-edge tuning.
3. `GR_FITTED_POLYNOMIAL` — reject for downstream target circularity.
4. `MINIMUM_NORM_HODGE_RESPONSE` — reject for hidden metric/minimum-norm selector.
5. `PRUNING_OR_TIME_RATE_RESPONSE` — reject for pre-time ontology violation.

Each bad control must fail for its preregistered primary reason.

## Exact multi-size structural audit

For each accepted polynomial law and L in {5,7,9}, independently rebuild the torus chain complex, exact cycle basis Z_L=ker(B1_L), canonical A_L, and f(A_L). Verify:

- cycle dimension = L^2+1;
- A_L preserves Z_L;
- f(A_L) preserves Z_L;
- primitive-translation sum is D4 invariant;
- exact commutation with a generating set of translations and D4;
- the polynomial coefficients are identical at all sizes.

No downstream observable is computed.

## Spectral-edge robustness

Accepted controls must be constructed without diagonalizing A_L or inspecting its gaps. Record `accepted_candidate_spectrum_queries=0` and `accepted_candidate_spectral_edge_parameters=0`. The bad spectral-edge control is rejected from declared construction provenance.

## Admissibility versus selection

Passing this gate means only that a candidate is clean enough for later falsification. If two or more projectively inequivalent target-blind controls pass, set `admissibility_contract_is_nonselective=true` and `response_function_selected=false`.

## Preregistered outcomes

`AXIOM_ADMISSIBILITY_AUDIT_UNRESOLVED` — a hard requirement cannot be checked or the exact multi-size audit fails.

`AXIOM_ADMISSIBILITY_CONTRACT_OVERRESTRICTIVE` — fewer than two target-blind controls survive.

`PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE` — at least two distinct target-blind controls pass and all bad controls fail for their intended reasons, with no physical response law selected.

## Mechanical adjudication

`if unresolved_check_count > 0 -> AXIOM_ADMISSIBILITY_AUDIT_UNRESOLVED`
`elif admissible_target_blind_control_count < 2 -> AXIOM_ADMISSIBILITY_CONTRACT_OVERRESTRICTIVE`
`else -> PRETIME_RESPONSE_AXIOM_ADMISSIBILITY_CONTRACT_CERTIFIED_NONSELECTIVE`

## Claim firewall

`new_response_function_axiom_adopted = false`
`response_function_selected = false`
`candidate_tested_against_gravity = false`
`gravity_observables_evaluated = false`
`new_metric_axiom_added = false`
`new_time_axiom_added = false`
`uses_holonomy_selector = false`
`uses_newton_or_gr_selector = false`
`uses_pruning_as_selector = false`
`uses_entropy_as_selector = false`
`uses_physical_time = false`
`physical_gravity_derived = false`
`Pillar_3 = OPEN`

## Next lawful move

After certification, formulate a small preregistered set of independently motivated NEW response principles that pass this contract, then expose them to one common adversarial canary suite. Success against gravity may test a locked law but cannot retroactively make it derived from the frozen ontology.

## Verification

Tests-first RED→GREEN; hash-pinned v15.25/v15.26/v15.37 evidence; exact multi-size rational algebra; deterministic candidate manifest; bad-control sensitivity; inherited v15.36/v15.37 regressions; byte-identical result replay; exact-head GitHub Actions success.
