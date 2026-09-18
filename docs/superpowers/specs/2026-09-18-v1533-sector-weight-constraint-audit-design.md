# UQCF-GEM v15.33 — Sector-Weight Naturality / Composition Constraint Gate

**Date:** 2026-09-18
**Base:** v15.32 certified head `ff4707b3a09bc7cd091e89986c8cc3dcaf758798`
**Inherited:** `MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS`
**Pillar 3:** OPEN

## Purpose

v15.32 leaves ten scalar sector weights `w_i`, or nine relative weights after common projective scale.
v15.33 asks whether any already-certified pre-time principle supplies additional equations on those nine ratios without consulting gravity or adding a new selector.

## Frozen inputs

Hash-pin and type-audit v15.32, v15.05, v15.06, v13.22, v13.23, v13.26 and v15.24. No inherited scientific file may be modified.

## Weight algebra

For the ten multiplicity-free sectors `S_i`, every equivariant linear endomorphism has

`T_w | S_i = w_i I`.

Hence addition, scalar multiplication and composition are coordinatewise:

`T_w + T_v = T_(w+v)`

`a T_w = T_(a w)`

`T_w T_v = T_(w*v)`.

## Gate A — automatic frozen constraints

Verify exactly that every weight vector satisfies:

1. linearity/source additivity;
2. source reversal `T_w(-z)=-T_w(z)`;
3. inherited G-covariance;
4. same-carrier composition closure;
5. availability of the identity at `w=(1,...,1)`;
6. common source rescaling as projective gauge.

These are family-closure properties. They do not select one family member.

## Gate B — type-blocked inherited principles

- v13.22 refinement naturality maps an already supplied source as `P -> P tensor I`; it does not select the source or a torus-sector weight vector.
- v13.23 leaves QRSL irreducible; no hidden refinement selector may be imported.
- v15.05 proves labeled monoidal composition preserves arbitrary already-chosen local response.
- v15.06 gives multiplicative recoverability scalars but no scalar-to-operator/source map.
- v15.24 no-signalling and product composition are conditional properties of supplied tensor-factor channels and are not a universal source law or a typed map to these torus sectors.
- v13.26 removes one common positive source scale but leaves relative projective ratios untouched.

Each candidate is classified as one of:

`AUTOMATIC_FOR_ALL_WEIGHTS`
`TYPE_BLOCKED_NO_CERTIFIED_MAP_TO_WEIGHT_SPACE`
`PROJECTIVE_GAUGE_ONLY`
`NEW_ASSUMPTION_CONTROL_ONLY`
`ACTUAL_WEIGHT_EQUATION`.

## Gate C — exact frozen constraint rank

Let `r` be the rank of all actual frozen weight equations after excluding the already-known common projective gauge. The surviving relative-weight dimension is `9-r`.

## Gate D — stronger-selector controls

These are controls only and must not be promoted to frozen ontology:

- Idempotence `T_w^2=T_w` gives `w_i in {0,1}` exactly: 1024 binary solutions, 1023 nonzero choices. It discretizes but does not uniquely select.
- Equal weights collapse to one projective class, but this is a supplied selector and must be tagged `NEW_ASSUMPTION_CONTROL_ONLY`.
- Positive weights form a positive cone and retain nine continuous projective degrees of freedom.

## Preregistered outcomes

`FROZEN_CONSTRAINTS_REDUCE_SECTOR_WEIGHTS` — at least one correctly typed frozen principle gives nonzero equation rank.

`FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE` — all frozen principles are automatic, gauge-only, or type-blocked, so equation rank is zero.

`WEIGHT_CONSTRAINT_AUDIT_UNRESOLVED` — typing cannot be adjudicated cleanly.

## Mechanical adjudication

`if unresolved typing -> WEIGHT_CONSTRAINT_AUDIT_UNRESOLVED`

`elif frozen_constraint_rank > 0 -> FROZEN_CONSTRAINTS_REDUCE_SECTOR_WEIGHTS`

`else -> FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE`.

## Required controls

1. ten-sector count and projective dimension inherited exactly from v15.32;
2. multiple exact rational witness vectors satisfying all automatic laws;
3. exact coordinatewise composition and reversal;
4. explicit zero equation contribution from every type-blocked candidate;
5. idempotence count 1024 total / 1023 nonzero;
6. equal-weight control isolated as new assumption;
7. positive-cone control retains projective dimension 9;
8. deterministic ledger and gravity firewall.

## Claim firewall

`new_source_semantics_axiom_added = false`
`new_sector_weight_selector_added = false`
`coupling_solver_reopened = false`
`gravity_observables_evaluated = false`
`uses_holonomy_selector = false`
`uses_newton_or_gr = false`
`uses_metric_selector = false`
`uses_pruning_as_selector = false`
`uses_entropy_as_selector = false`
`uses_physical_time = false`
`physical_gravity_derived = false`
`Pillar_3 = OPEN`

## Interpretation

A zero constraint rank does not mean arbitrary weights are physically correct. It means the certified ontology has not earned a principle distinguishing the nine relative sector-weight ratios.

The next lawful move would then require a genuinely new ontology-derived invariant mapping into the sector weights, or an explicitly declared constitutive/source-semantics axiom. Downstream gravity may test a locked law but may not choose it.

## Verification standard

Tests-first RED→GREEN, hash-pinned inputs, exact/rational algebra, explicit typed-constraint ledger, inherited v15.32 regression, deterministic ledger regeneration, and exact-head GitHub Actions success.
