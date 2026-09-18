# UQCF-GEM v15.32 — Commutant / Canonical Sector Decomposition Gate

## Adjudication

`MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS`

v15.31 found a ten-dimensional equivariant same-q fiber channel space. v15.32 resolves what those ten dimensions are.

## Exact rational macro-decomposition

Without a metric or Hodge selector, the 50-dimensional cycle representation splits canonically as

```text
Z = H ⊕ B_axis ⊕ B_diagonal ⊕ B_generic
```

with exact dimensions

```text
2 + 12 + 12 + 24 = 50.
```

- `H` is the two-dimensional cycle subspace fixed by all 49 translations.
- The other three sectors are boundary images of exact rational face-line projectors.
- The projectors are idempotent, pairwise orthogonal, complete on face augmentation, commute with all 392 automorphisms, and remain injective under `B2`.

The exact sector Hom matrix is diagonal:

```text
              H  axis  diagonal  generic
H             1    0      0        0
axis          0    3      0        0
diagonal      0    0      3        0
generic       0    0      0        3
```

so the total commutant dimension is again

```text
1 + 3 + 3 + 3 = 10.
```

No equivariant linear map mixes one rational macro-sector into another.

## Splitting-field structure

The nonzero character lattice `F_7^2 \ {0}` has exactly nine D4 orbits:

- three axis orbits, each dimension 4;
- three diagonal orbits, each dimension 4;
- three generic orbits, each dimension 8.

Scalar multiplication by `F_7^*` groups the three orbits of each type into one rational/Galois family. Together with the two-dimensional homology sector this gives ten splitting-field irreducible sectors:

```text
2,
4,4,4,
4,4,4,
8,8,8
```

and each occurs once.

Therefore the v15.31 ten-dimensional ambiguity is **not matrix mixing among repeated copies**. It is ten independent scalar sector weights. Up to one overall projective scale, nine relative weights remain unfixed.

## Scientific consequence

The frozen symmetry/topology has done more than v15.31 alone showed:

- arbitrary equivariant mixing is forbidden;
- four rational macro-sectors are canonical;
- the splitting-field representation is multiplicity-free.

But the theory still does not select one sector or fix the relative weights among the ten inequivalent sectors.

The next required object is:

`INDEPENDENT_PRETIME_PRINCIPLE_FIXING_RELATIVE_WEIGHTS_OR_RELATIONS_AMONG_THE_10_MULTIPLICITY_FREE_SECTORS`

That principle must be derived independently or introduced explicitly as a new axiom before downstream gravity behavior is consulted.

## Claim boundary

No source-semantics axiom was added. The physical coupling solver was not reopened. No gravity canary, holonomy/Newton/GR score, metric/Hodge selector, entropy, pruning, or physical time was used. `Pillar_3 = OPEN`.
