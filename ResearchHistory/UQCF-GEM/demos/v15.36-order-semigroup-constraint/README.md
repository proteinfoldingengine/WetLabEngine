# UQCF-GEM v15.36 — Positivity / Order / Semigroup Constraint Gate

## Adjudication

`FROZEN_ORDER_SEMIGROUP_CONSTRAINTS_LEAVE_FUNCTION_UNSELECTED`

v15.34-v15.35 reduced the equivariant response problem to one arbitrary function of the canonical adjacency:

```text
T = f(A)
```

with nine projective relative degrees of freedom.

v15.36 tests whether composition-semigroup, positivity, contractivity, recoverability or quantum-channel structure reduces that freedom.

## Semigroup theorem

On the ten multiplicity-free real sectors, composition is coordinatewise.

A continuous one-parameter semigroup satisfying

```text
T_0 = I
T_s T_t = T_(s+t)
```

has sector multipliers

```text
w_i(t) = exp(b_i t).
```

Thus

```text
T_t = exp[t g(A)]
```

for an arbitrary generator `g(A)` in the same ten-dimensional commutant.

Therefore:

```text
generator dimension = 10
projective relative generator dimension = 9
```

The semigroup law does not select the generator.

Five projectively distinct positive rational discrete semigroups were checked exactly and satisfy composition with zero arithmetic error.

## Positivity and contraction controls

Sectorwise nonnegative response weights form a full-dimensional cone:

```text
affine dimension = 10
positive projective dimension = 9
```

Likewise the cone of nonpositive semigroup generators—giving sector contractions for positive parameter—has affine dimension 10.

So even if these stronger mathematical controls were granted, they would not select a unique response generator.

They are not promoted to physical laws.

## Frozen typing audit

- v15.05 composition: nonselective family closure.
- v15.06 recoverability multiplicativity: scalar-to-response-function map missing.
- v13.16 Markov/recoverability: exact Markovity is not selected; the recovery structure lives on quantum state/channel data.
- v15.24 CPTP/no-signalling/product composition: typed to supplied quantum channel algebras, not the cycle carrier.
- no frozen pointed physical order cone, order unit, Choi structure or probability simplex is certified on Z.

Therefore:

```text
frozen actual function equations = 0
frozen function constraint rank = 0
surviving projective function dimension = 9
```

## Consequence

The frontier remains

```text
T = f(A)
A is canonical
f is not selected
```

and this remains true even after granting semigroup closure as a mathematical control.

No order axiom, semigroup axiom, source law, response generator, gravity observable, metric/Hodge rule, pruning, entropy or physical time was inserted.

`Pillar_3 = OPEN`.

## Next required object

`NEW_TYPED_PRETIME_RESPONSE_PRINCIPLE_OR_EXPLICIT_RESPONSE_FUNCTION_AXIOM`
