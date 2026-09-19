# UQCF-GEM v15.36 — Positivity / Order-Preservation / Semigroup Constraint Gate

**Date:** 2026-09-19  
**Base:** v15.35 exact certified head `c549e093be355ca93fff5ac1c63d0c3a4452b6f7`  
**Inherited:** `CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED`  
**Pillar 3:** OPEN

## Purpose

v15.34-v15.35 established:

```text
End_G(Z) = Q[A]
```

and an exact ten-dimensional response algebra with no frozen hard-radius selector.

v15.36 asks whether already-earned positivity, order, recoverability, channel-composition, or semigroup ideas impose any equation on the remaining adjacency response function.

## Algebra

Over the real splitting field, the commutant is diagonal on ten inequivalent sectors:

```text
T_w | S_i = w_i I.
```

Composition is coordinatewise multiplication.

A continuous one-parameter semigroup with identity,

```text
T_0 = I
T_s T_t = T_(s+t)
```

has sector weights

```text
w_i(t) = exp(b_i t)
```

for arbitrary real rates `b_i`.

Hence every generator

```text
B = g(A)
```

in the ten-dimensional real commutant generates such a semigroup, and positivity of all sector multipliers is automatic.

The semigroup law therefore classifies evolution after a generator is supplied; it does not select the generator.

## Gate A — exact semigroup non-selection controls

Use exact rational discrete semigroups

```text
w_i(n) = q_i^n
```

with positive rational `q_i`.

Verify for several projectively inequivalent bases:

```text
w(m+n) = w(m) * w(n)
```

exactly over Q.

Record:

- witness semigroup count;
- projectively distinct generator/base count;
- exact composition error = zero;
- continuous-generator dimension = 10;
- projective relative-generator dimension = 9.

## Gate B — positivity control

Treat sectorwise nonnegativity only as a mathematical control:

```text
w_i >= 0.
```

Verify the positive cone has full affine dimension 10 and its positive projectivization has dimension 9.

This control is not automatically a physical order law on the cycle carrier.

## Gate C — contraction control

As a stronger control, consider semigroup generators with

```text
b_i <= 0.
```

so every sector multiplier satisfies `0 < exp(b_i t) <= 1` for `t>=0`.

The nonpositive generator cone has full dimension 10. Thus even positivity plus contractivity does not uniquely select a generator.

This is a control only.

## Gate D — frozen typing audit

Classify inherited principles.

### v15.05 composition

Frozen monoidal composition preserves arbitrary already-chosen response law.

Classification:

`COMPOSITION_CLOSURE_NONSELECTIVE`.

### v15.06 recoverability multiplicativity

Root fidelity is a multiplicative scalar and `-log F_root` additive, but no natural scalar-to-current-cycle-response map is certified.

Classification:

`RECOVERABILITY_SCALAR_TO_RESPONSE_FUNCTION_TYPE_BLOCKED`.

### v13.16 Markov/recoverability

Exact Markovity is explicitly not selected by the ontology. Approximate recoverability is conditional/existential.

Classification:

`MARKOV_SEMIGROUP_NOT_FROZEN_ON_CURRENT_CARRIER`.

### v15.24 CPTP / no-signalling / product composition

These are properties of supplied tensor-factor quantum channels. The cycle carrier `Z` is not certified as that operator algebra/channel space.

Classification:

`CPTP_ORDER_STRUCTURE_TYPE_BLOCKED`.

### physical order cone on Z

No frozen pointed cone, order unit, Choi structure, or probability simplex on the 50-D cycle carrier is certified.

Classification:

`NO_FROZEN_PHYSICAL_ORDER_CONE_ON_Z`.

## Gate E — constraint rank

Count only correctly typed frozen equations on the response function.

Each candidate receives:

- `NONSELECTIVE_FAMILY_CLOSURE`
- `TYPE_BLOCKED`
- `CONTROL_ONLY`
- `ACTUAL_FUNCTION_EQUATION`
- `UNRESOLVED`

Let `r` be the rank of actual frozen function equations.

Surviving projective function dimension:

```text
9 - r.
```

## Preregistered outcomes

### `ORDER_SEMIGROUP_AUDIT_UNRESOLVED`

Typing or exact controls fail.

### `FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_REDUCE_FUNCTION`

At least one correctly typed frozen principle gives nonzero equation rank.

### `FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_LEAVE_FUNCTION_UNSELECTED`

Semigroup closure is nonselective, positivity/contraction controls retain full dimension, and all stronger frozen order/channel claims are type-blocked.

## Required controls

1. ten inherited sectors;
2. at least five exact positive rational semigroup witnesses;
3. exact composition for several integer parameter pairs;
4. projective inequivalence of witnesses;
5. positive-cone affine dimension 10;
6. positive projective dimension 9;
7. nonpositive generator cone affine dimension 10;
8. frozen equation rank;
9. deterministic result ledger;
10. gravity/source-selector firewall.

## Claim firewall

```text
new_source_semantics_axiom_added = false
new_order_axiom_added = false
new_semigroup_axiom_added = false
response_generator_selected = false
adjacency_function_selected = false
coupling_solver_reopened = false
gravity_observables_evaluated = false
uses_holonomy_selector = false
uses_newton_or_gr = false
uses_metric_selector = false
uses_pruning_as_selector = false
uses_entropy_as_selector = false
uses_physical_time = false
physical_gravity_derived = false
Pillar_3 = OPEN
```

## Interpretation

If the frozen equation rank is zero, the result is not that arbitrary semigroups are physical.

It means the current certified ontology has still not supplied the constitutive rule selecting the generator `g(A)`.

The next lawful step must search for a genuinely typed invariant or declare a new pre-time response-function axiom before any gravity test is allowed to choose a function.

## Verification

Tests-first RED->GREEN, hash-pinned evidence, exact rational controls, inherited frontier regressions, deterministic ledger replay, exact-head Actions success.
