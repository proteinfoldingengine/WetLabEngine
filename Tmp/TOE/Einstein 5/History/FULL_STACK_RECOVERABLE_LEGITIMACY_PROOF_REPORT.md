# Full Stack Recoverable Legitimacy Python Proof

**Status:** executable proof-of-work  
**Version:** FULL_STACK_V1010  
**Seed:** 1010

## Core Result

```text
State is not history.
Geometry-like form is not provenance.
Visible equivalence is not legitimacy.
Omega-like equivalence is not legitimacy.
Recoverable legitimacy requires independent provenance.
```

## Theorem Candidate

```text
For a history space H = E × R where terminal visible observables S(H) and geometry-like fields Ω(H) depend only on event/order structure E, visible-state equivalence and geometry-like equivalence are insufficient to certify recoverable legitimacy when multiple provenance variants R share the same E. An independent provenance predicate P(H) is necessary. Genesis Pin is one sufficient and locally minimal implementation in the tested stack, but uniqueness is not proven.
```

## V1003 — Independent Counterfeit Geometry Stress

```json
{
  "histories_tested": 251,
  "counterfeits_tested": 250,
  "visible_only_accepted": 251,
  "geometry_only_certified": 251,
  "provenance_valid": 1,
  "full_certified": 1,
  "invalid_histories_with_geometry_accept": 250,
  "max_counterfeit_omega_similarity": 0.9999892771474855,
  "mean_counterfeit_omega_similarity": 0.9998806233939558,
  "invalid_full_certified": 0
}
```

## V1005 — Genesis Pin Minimality Ablation

```json
{
  "full_components_invalid_certified": 0,
  "single_component_ablation_slips": {
    "registry_matches": 0,
    "root_matches": 45,
    "quorum_valid": 42,
    "append_valid": 43,
    "non_circular": 0
  },
  "locally_minimal_against_generated_family": false
}
```

## V1006 — Formal Finite History Space

```json
{
  "event_sequences": 243,
  "total_histories": 1458,
  "S_classes": 12,
  "Omega_classes": 24,
  "SOmega_classes": 151,
  "ambiguous_SOmega_classes": 151,
  "invalid_SOmega_only_certified": 1215,
  "invalid_full_certified": 0
}
```

## V1007 — Generalized Finite-Family Sweep

```json
{
  "configs_tested": 20,
  "all_configs_have_ambiguous_SOmega_classes": true,
  "all_configs_have_invalid_SOmega_only_certified": true,
  "all_configs_have_zero_invalid_full_certified": true,
  "max_invalid_SOmega_only_certified": 390625
}
```

## V1009 — Necessity vs Specificity

```json
{
  "visible_geometry_only_false_accepts": 8,
  "sufficient_predicates": [
    "genesis_pin_full",
    "alternate_full_provenance"
  ],
  "conclusion": "Independent provenance is necessary; Genesis Pin is sufficient in the tested family but uniqueness is not proven."
}
```

## Claim Boundary

This script does **not** prove:

- physical spacetime,
- General Relativity,
- Einstein equations,
- actual ADM constraints,
- physical curvature,
- quantum gravity,
- production cryptographic security,
- uniqueness of Genesis Pin across all possible systems.

It does support the narrower map-class claim:

```text
When visible/geometry observables are functions of form/order and legitimacy is a function of provenance,
form-equivalence cannot certify source-legitimacy.
```

## Generated Artifacts

```text
v1003_counterfeit_stress_results.csv
v1005_ablation_results.csv
v1006_finite_history_space_results.csv
v1007_generalized_sweep_results.csv
v1009_predicate_comparison.csv
full_stack_summary.json
counterfeit_geometry_stress.png
genesis_pin_ablation.png
```
