# UQCF-GEM v15.35 — Canonical Support-Radius / Locality Filtration Gate

**Date:** 2026-09-19  
**Class:** theorem-first, gravity-blind locality audit  
**Base:** v15.34 exact certified head `e24b94fb1a0ca4c8eda33379f5a4ab3f4c360487`  
**Inherited result:** `FULL_COMMUTANT_GENERATED_BY_CANONICAL_ADJACENCY_FUNCTION_UNSELECTED`  
**Pillar 3:** OPEN

## 1. Purpose

v15.34 proved

```text
End_G(Z) = Q[A]
```

for the canonical nearest-neighbor translation adjacency `A` on the 50-dimensional cycle carrier.

v15.35 asks two deliberately separate questions:

1. What exact finite-support / support-radius filtration does this algebra carry?
2. Does any already-certified pre-time locality theorem select one support radius for the physical response law?

The first is algebra. The second is physics/ontology.

A positive answer to (1) must not be promoted into a positive answer to (2).

## 2. Frozen inputs

Hash-pin:

- v15.28 exact 7x7 torus representation machinery;
- v15.34 canonical adjacency result;
- v13.15 Relational Locality / Sparse Source Closure;
- v13.18 Source-Conditioned Recoverability / QMAR Jet Locality;
- v15.03 graph-site source-lift design / locality claim boundary.

No inherited scientific file may be modified.

## 3. Canonical displacement-orbit kernels

The translation subgroup is `Z_7^2`.

For displacement

```text
d=(dx,dy)
```

define its torus graph radius

```text
r(d)=min(dx,7-dx)+min(dy,7-dy)
```

using representatives modulo 7.

D4 acts on displacement labels. The ten exact D4 orbits are preregistered by canonical representatives:

```text
(0,0)  radius 0, size 1
(0,1)  radius 1, size 4
(0,2)  radius 2, size 4
(0,3)  radius 3, size 4
(1,1)  radius 2, size 4
(1,2)  radius 3, size 8
(1,3)  radius 4, size 8
(2,2)  radius 4, size 4
(2,3)  radius 5, size 8
(3,3)  radius 6, size 4
```

For each orbit `O`, define the exact orbit convolution

```text
E_O = sum_{d in O} T_d
```

on oriented edge chains and restrict it to `Z`.

Gate A must verify:

1. there are exactly ten displacement orbits;
2. the orbit sizes sum to 49;
3. every `E_O` preserves `Z`;
4. every `E_O` commutes with the full frozen group;
5. the ten restricted `E_O` are linearly independent;
6. therefore they form a second exact basis of `End_G(Z)`.

## 4. Gate B — exact polynomial reconstruction

For each orbit operator solve exactly for the unique coefficients

```text
E_O|_Z = c_0 I + c_1 A + ... + c_9 A^9.
```

This is possible iff the v15.34 theorem is correct.

Required checks:

- exact rational solution for all ten orbit kernels;
- exact replay equality on `Z`;
- coefficient uniqueness;
- rank 10 of the coefficient matrix;
- no floating fitting.

This produces a direct change of basis between:

```text
spectral/polynomial basis {I,A,...,A^9}
```

and

```text
finite-support orbit basis {E_O}.
```

## 5. Gate C — support-radius filtration

Define

```text
L_R = span{ E_O : radius(O) <= R }.
```

For the 7x7 torus the preregistered exact dimensions are:

```text
R=0 -> dim 1
R=1 -> dim 2
R=2 -> dim 4
R=3 -> dim 6
R=4 -> dim 8
R=5 -> dim 9
R=6 -> dim 10
```

The corresponding nonzero projective freedom dimensions are:

```text
0, 1, 3, 5, 7, 8, 9.
```

Gate C must verify these dimensions from exact support constraints, not merely count the preregistered table.

## 6. Gate D — locality is not polynomial-degree truncation

Because `I,A,...,A^9` are independent, the polynomial degree-`k` subspace has dimension `k+1` for `0<=k<=9`.

Support-radius locality is a different filtration.

For example:

```text
dim{deg f <= 2} = 3
dim L_2 = 4.
```

Therefore:

```text
hard radius <= R
!=
polynomial degree <= R
```

on this finite torus.

The implementation must record the two filtrations separately and reject any attempt to infer low polynomial degree from hard support locality without an additional theorem.

## 7. Gate E — frozen locality law audit

The archive is adjudicated by typing, not by suggestive wording.

### v13.15 generic locality

v13.15 explicitly proves:

```text
generic bounded-neighborhood QMAR: NO-GO
```

even on a treewidth-1 path.

Therefore graph sparsity/site locality alone cannot be imported as a universal hard response-radius cutoff.

Classify:

`GENERIC_HARD_RADIUS_NOT_DERIVED`.

### v13.15 commuting-Markov positive sector

Exact separator closure exists only under:

- commuting graphical state;
- Markov factorization;
- compatible source.

v13.15 explicitly records that this structure is not derived from the ontology.

No current certified map identifies the v15.34 cycle-response algebra with that conditional sector.

Classify:

`CONDITIONAL_LOCALITY_NOT_TYPED_TO_CURRENT_WEIGHT_ALGEBRA`.

### v13.18 recoverability / CMI locality

v13.18 gives approximate error bounds

```text
O(||P|| sqrt(CMI))
```

on conditioned strata.

That is not an exact statement that response matrix elements vanish outside some graph radius.

Classify:

`APPROXIMATE_ERROR_LOCALITY_NOT_HARD_SUPPORT_CUTOFF`.

### v15.03 site-local source covariance

A local source input does not imply a local response kernel; v13.15 gives the explicit generic counterexample.

Classify:

`SOURCE_LOCALITY_DOES_NOT_ENTAIL_RESPONSE_RADIUS`.

## 8. Frozen radius adjudication

Let a hard-radius law count only if the frozen archive supplies a correctly typed exact statement:

```text
physical response T belongs to L_R
```

for a specific `R<6`.

Anything conditional, approximate, on another carrier, or merely source-local contributes zero hard-radius constraints.

Record:

```text
frozen_hard_radius_selected = null or integer
frozen_hard_radius_constraint_count
surviving_response_dimension
surviving_projective_response_dimension
```

## 9. Stronger-selector controls

These demonstrate what a supplied hard-locality axiom would do, without adopting one.

For each `R=0,...,6`, record:

- response-space dimension;
- projective dimension;
- number of displacement orbits retained.

In particular:

```text
R=0 -> one-dimensional scalar/identity class
R=1 -> two-dimensional response family
R=6 -> full ten-dimensional commutant
```

Every `R<6` is labeled:

`NEW_HARD_RADIUS_ASSUMPTION_CONTROL_ONLY`

unless independently earned.

## 10. Preregistered outcomes

### `SUPPORT_RADIUS_FILTRATION_UNRESOLVED`

Exact orbit-basis, polynomial-reconstruction, or support checks fail.

### `FROZEN_LOCALITY_SELECTS_HARD_RADIUS`

A previously certified, correctly typed exact law selects a specific `R<6`.

### `CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED`

The exact support filtration exists, but no frozen law selects one radius. The full nine projective function degrees remain physically unselected.

## 11. Mechanical adjudication

```text
if exact filtration fails:
    SUPPORT_RADIUS_FILTRATION_UNRESOLVED
elif frozen exact typed radius exists:
    FROZEN_LOCALITY_SELECTS_HARD_RADIUS
else:
    CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED
```

## 12. Claim firewall

```text
new_source_semantics_axiom_added = false
new_locality_axiom_added = false
hard_radius_selected = false
polynomial_degree_selected = false
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

## 13. Interpretation discipline

A canonical locality filtration is meaningful structure. It tells us exactly how much constitutive freedom would survive a supplied finite-support principle.

But the archive currently contains a generic bounded-neighborhood no-go and only conditional/approximate positive locality theorems.

Therefore no hard radius may be chosen simply because local physics is aesthetically attractive.

## 14. Next-step mapping

If no frozen radius is selected, the next lawful question is not “which radius fits gravity?”

It is:

> Is there any other already-earned target-blind property of `f(A)`—positivity/order preservation, semigroup/composition law, recoverability monotonicity, or a derived refinement relation—that supplies a nonzero constraint?

Only correctly typed properties may be tested.

If all such properties remain absent or type-blocked, the branch reaches an explicit constitutive object:

`PRETIME_RESPONSE_FUNCTION_AXIOM`.

## 15. Verification standard

Scientific completion requires:

1. tests-first RED -> GREEN;
2. exact orbit enumeration;
3. exact rational basis transformation;
4. exact support-radius filtration;
5. hash-pinned locality evidence;
6. inherited v15.34 regression;
7. deterministic ledger replay;
8. exact-head GitHub Actions success;
9. no post-certification scientific edits.

No result is claimed by this design document alone.
