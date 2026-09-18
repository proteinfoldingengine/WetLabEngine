# UQCF-GEM v15.33 — Sector-Weight Naturality / Composition Constraint Gate

## Adjudication

`FROZEN_CONSTRAINTS_LEAVE_ALL_9_RELATIVE_WEIGHTS_FREE`

v15.32 reduced the equivariant source-response ambiguity to ten inequivalent multiplicity-free sector weights, or nine relative weights after one common projective scale. v15.33 asks whether any already-certified pre-time principle reduces those nine ratios.

The exact frozen constraint rank is:

```text
0
```

and therefore the surviving projective sector-weight dimension remains:

```text
9
```

## What the frozen principles actually do

Five inherited properties are automatic for every ten-weight law:

- linearity / source additivity;
- source reversal oddness;
- G-covariance;
- same-carrier composition closure;
- availability of the identity map.

These certify a closed family. They do not select one member.

Five stronger-looking inherited principles are not typed as equations on the v15.32 sector-weight space:

- v13.22 refinement naturality;
- v13.23 QRSL;
- v15.05 labeled monoidal composition;
- v15.06 recoverability multiplicativity;
- v15.24 no-signalling / independent product composition.

Each therefore contributes zero sector-weight equations in this gate rather than being silently promoted into a new selector.

v13.26 contributes the already-known common positive source-scale gauge. It removes one overall scale and nothing further.

## Exact witness test

Five projectively distinct rational weight vectors were evaluated. Every one satisfies the automatic frozen constraints exactly.

Thus the automatic laws do not merely fail to prove uniqueness abstractly; explicit inequivalent weight laws survive them.

## Stronger-selector controls

Idempotence was tested only as a nonphysical control:

```text
T_w^2 = T_w  =>  w_i in {0,1}.
```

This gives exactly:

```text
1024 total idempotents
1023 nonzero idempotents
```

so even this stronger extra condition would discretize the ambiguity without uniquely selecting a law. Earlier v15.23 evidence also states that idempotence has not been derived as a new physical requirement.

An equal-weight condition would collapse the projective freedom to zero, but that is a supplied selector by definition and remains `NEW_ASSUMPTION_CONTROL_ONLY`.

Positivity leaves a nine-dimensional projective positive cone.

## Scientific consequence

The current ontology now localizes the missing source information very sharply:

```text
not arbitrary operator mixing
not representation multiplicity
not overall scale
but nine undetermined relative weights among ten inequivalent symmetry sectors
```

No currently certified pre-time principle supplies a typed relation that fixes any of those nine ratios.

This is an archive-relative branch boundary, not a theorem that no deeper principle can fix them.

## Claim boundary

v15.33 adds no source-semantics axiom, no sector-weight selector, no coupling law, and no gravity criterion. It does not use holonomy, Newton/GR, metric/Hodge, pruning, entropy, or physical time to choose weights.

`Pillar_3 = OPEN`.

## Next required object

`NEW_TYPED_PRETIME_INVARIANT_OR_EXPLICIT_SECTOR_WEIGHT_AXIOM`

A future continuation must either derive a new pre-time invariant with a certified map into the ten-sector weight algebra, or explicitly declare a new constitutive/source-semantics axiom. A downstream gravity test may evaluate a law only after that law is locked independently.
