# UQCF-GEM v15.35 — Canonical Support-Radius / Locality Filtration Gate

## Adjudication

`CANONICAL_LOCALITY_FILTRATION_EXISTS_BUT_RADIUS_UNDERIVED`

v15.34 proved that every rational equivariant linear response on the 50-dimensional cycle carrier is a polynomial `f(A)` of the canonical nearest-neighbor adjacency.

v15.35 gives that algebra an exact finite-support basis.

## Exact orbit basis

The torus translation group has ten D4 displacement orbits, with radii:

```text
(0,0) r=0
(0,1) r=1
(0,2), (1,1) r=2
(0,3), (1,2) r=3
(1,3), (2,2) r=4
(2,3) r=5
(3,3) r=6
```

The ten orbit-convolution operators are linearly independent on `Z` and therefore form another exact basis of the same 10-dimensional commutant.

Every one reconstructs exactly as a rational polynomial in `A`.

A notable result is:

```text
identity orbit -> polynomial degree 0
nearest-neighbor orbit -> polynomial degree 1
all other eight finite-support orbit kernels -> polynomial degree 9
```

So short support is not the same thing as low polynomial degree.

## Exact support-radius filtration

```text
radius <= 0 : dimension 1   projective 0
radius <= 1 : dimension 2   projective 1
radius <= 2 : dimension 4   projective 3
radius <= 3 : dimension 6   projective 5
radius <= 4 : dimension 8   projective 7
radius <= 5 : dimension 9   projective 8
radius <= 6 : dimension 10  projective 9
```

By contrast the degree-`k` polynomial filtration has dimension `k+1`.

The first mismatch already occurs at radius/degree 2:

```text
support radius <= 2 : dimension 4
polynomial degree <= 2 : dimension 3
```

Therefore a future locality principle must be stated as a support statement, not silently replaced by a low-degree polynomial ansatz.

## Frozen locality audit

The current archive does not select a hard response radius.

- v13.15 explicitly gives a generic bounded-neighborhood QMAR **NO-GO**, even with a site-local source.
- v13.15 has exact separator locality only in a commuting-Markov sector whose required structure is explicitly not derived from the ontology.
- v13.18 gives approximate source-conditioned locality with error `O(||P|| sqrt(CMI))`; it is not exact compact support.
- site-local source covariance does not imply compactly supported response.

Hence:

```text
frozen hard-radius constraints = 0
selected hard radius = none
surviving response dimension = 10
surviving projective dimension = 9
```

The radius table is therefore a **classification of what a future locality axiom would imply**, not a locality axiom.

No source semantics, response function, radius, polynomial degree, or gravity criterion was selected. `Pillar_3 = OPEN`.

## Next required object

`TARGET_BLIND_TYPED_CONSTRAINT_ON_ADJACENCY_RESPONSE_FUNCTION_OR_EXPLICIT_PRETIME_RESPONSE_FUNCTION_AXIOM`

The next lawful audit may test other already-earned properties of `f(A)`—for example positivity/order preservation or a true semigroup law—only if those properties are correctly typed to this carrier. Gravity behavior may not choose the function.
