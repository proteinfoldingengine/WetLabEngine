# UQCF-GEM v15.32 — Commutant / Canonical Sector Decomposition Gate

**Date:** 2026-09-18  
**Class:** theorem-first, gravity-blind representation gate  
**Base:** v15.31 exact certified head `d2b767c88a4bdb3d750d7bb696b29b4fbd34dca1`  
**Inherited result:** `FIBER_EXTENSION_CHANNELS_EXIST_BUT_NONUNIQUE`, with `dim End_G(Z)=10`  
**Pillar 3:** OPEN

## 1. Purpose

v15.31 proved that the same-q fiber/cycle representation

```text
Z = ker(B1),  dim Z = 50
```

admits a ten-dimensional equivariant endomorphism space under the exact 392-element pre-time automorphism group.

v15.32 asks a strictly upstream question:

> Is that ten-dimensional freedom an undifferentiated ambiguity, or does the already-earned topology and symmetry canonically decompose Z into invariant sectors so that the remaining freedom can be localized precisely?

The gate must not choose a sector or relative weight because it later resembles gravity.

## 2. Frozen objects

Reuse exactly:

- the 7 x 7 torus chain complex from v15.25-v15.31;
- `C1`, `B1`, `B2`;
- `Z = ker(B1)`;
- the exact automorphism group `G = Z_7^2 semidirect D4`, order 392;
- the v15.28/v15.31 exact representation machinery and source pins.

No inherited scientific file may be modified.

## 3. Gate A — canonical rational macro-sectors

Let `C2` be rational face-coefficient space on the 49 torus faces and let `P0` be averaging onto constants.

Define exact rational line-averaging projectors:

- `Px`: functions of x only;
- `Py`: functions of y only;
- `P+`: functions of x+y mod 7 only;
- `P-`: functions of x-y mod 7 only.

Define

```text
P_axis    = Px + Py - 2 P0
P_diag    = P+ + P- - 2 P0
P_generic = I - Px - Py - P+ - P- + 3 P0
```

The implementation must verify exactly over Q:

1. each projector is idempotent;
2. the three are pairwise orthogonal;
3. their sum is `I-P0`;
4. their ranks are 12, 12, 24;
5. each commutes with the frozen G action on oriented face chains;
6. `B2` is injective on each image;
7. their boundary images are pairwise disjoint G-invariant subspaces of Z.

Separately define the homological sector

```text
H = Z^(translations)
```

as the subspace fixed by the normal translation subgroup. Verify `dim H=2`, it has zero intersection with `im(B2)`, and

```text
Z = H direct_sum B_axis direct_sum B_diag direct_sum B_generic
```

with dimensions

```text
2 + 12 + 12 + 24 = 50.
```

No metric/Hodge decomposition may be used.

## 4. Gate B — exact sector character orthogonality

Compute exact characters for the four invariant sectors under all 392 group elements.

The exact Hom-dimension matrix is

```text
dim Hom_G(S_i,S_j)
 = |G|^-1 sum_g chi_i(g) chi_j(g).
```

Do not preregister the numerical matrix as a scientific assumption; compute it from the exact projectors/action.

Adjudicate:

- whether cross-sector Hom spaces vanish;
- each self-End dimension;
- whether their sum reproduces `dim End_G(Z)=10`.

A mismatch with v15.31 is a hard failure.

## 5. Gate C — splitting-field momentum orbit classification

Use only the finite character lattice `F_7^2`.

Enumerate exact nonzero momentum orbits under D4. For each orbit record:

- representative;
- orbit size;
- type: axis, diagonal, or generic;
- stabilizer size.

Then audit scalar multiplication by `F_7^*`, which is the exact Galois action on 7th-root Fourier labels.

Determine:

- number of D4 momentum orbits;
- number per type;
- orbit dimensions;
- Galois grouping of those orbits into rational macro-sectors.

This gate may use Fourier labels as a representation-classification device only. No physical wave/momentum interpretation is inferred.

## 6. Gate D — multiplicity / commutant structure

Combine Gates A-C to determine whether the ten-dimensional commutant represents:

1. true multiplicity mixing inside repeated equivalent irreducibles;
2. scalar freedom on inequivalent symmetry sectors;
3. or a mixture of both.

If the splitting-field decomposition is multiplicity-free, record that fact explicitly.

If there are ten inequivalent splitting-field sectors each appearing once, then the ten-dimensional commutant is diagonal by sector: the ambiguity is ten independent sector weights, not arbitrary mixing.

Do not call a sector physical or preferred.

## 7. Preregistered outcomes

### `SECTOR_DECOMPOSITION_UNRESOLVED`

Exact rational projector, character, or momentum-orbit checks fail or disagree.

### `NO_CANONICAL_SECTOR_REDUCTION`

No nontrivial canonical invariant decomposition of Z is supplied by the frozen topology/symmetry.

### `CANONICAL_MACRO_SECTORS_WITH_RESIDUAL_MULTIPLICITY`

Canonical macro-sectors exist, but equivalent irreducible multiplicities leave genuine matrix-valued mixing freedom.

### `MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS`

The frozen structure canonically decomposes the representation and removes mixing ambiguity, but more than one inequivalent sector remains and their relative scalar weights are not selected.

### `UNIQUE_CANONICAL_SOURCE_SECTOR`

Exactly one nontrivial sector/ray survives every exact symmetry/topology equivalence without a new physical selector.

This outcome must not be inferred merely because one sector is topological, low-dimensional, visually simple, or attractive downstream.

## 8. Mechanical precedence

```text
if exact decomposition checks fail:
    SECTOR_DECOMPOSITION_UNRESOLVED
elif no nontrivial canonical invariant decomposition exists:
    NO_CANONICAL_SECTOR_REDUCTION
elif any equivalent-irrep multiplicity exceeds one:
    CANONICAL_MACRO_SECTORS_WITH_RESIDUAL_MULTIPLICITY
elif more than one inequivalent multiplicity-free sector survives:
    MULTIPLICITY_FREE_SECTORS_BUT_WEIGHT_NONUNIQUENESS
elif exactly one nontrivial sector survives:
    UNIQUE_CANONICAL_SOURCE_SECTOR
else:
    fail closed as SECTOR_DECOMPOSITION_UNRESOLVED
```

## 9. Required controls

At minimum:

1. exact projector idempotence;
2. exact projector orthogonality;
3. exact projector completeness on face augmentation;
4. exact G-commutation for all 392 actions;
5. exact boundary-map injectivity and direct-sum rank;
6. exact translation-fixed homology rank;
7. exact character inner-product Hom matrix;
8. recovery of the v15.31 total commutant dimension 10;
9. exact D4 orbit enumeration on `F_7^2\{0}`;
10. exact `F_7^*`/Galois orbit grouping;
11. basis/relabeling invariance of the sector counts;
12. gravity firewall.

## 10. Claim firewall

Machine-readable flags must remain:

```text
new_source_semantics_axiom_added = false
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

## 11. Deterministic output contract

At least:

```text
version = v15.32
base_sha
status
group_order
dim_Z
rational_macro_sector_count
rational_macro_sector_dimensions
projector_checks_exact
sector_hom_dimension_matrix
sector_self_end_dimensions
cross_sector_hom_zero
recovered_total_commutant_dimension
nonzero_momentum_orbit_count
momentum_orbits_by_type
galois_groups_by_type
splitting_field_sector_count
multiplicity_free_over_splitting_field
residual_weight_dimension
mixing_freedom_dimension
scientific_breakthrough
signal_of_life
firewall flags
next_required_object
```

## 12. Interpretation discipline

A canonical decomposition is not a physical selection rule.

If the result is multiplicity-free but has multiple sectors, the theory has learned something real: symmetry forbids arbitrary sector mixing. But the relative coefficients of the surviving sectors remain constitutive information.

That information may be supplied only by:

- additional independently derived pre-time structure; or
- an explicitly approved new physical/source-semantics axiom.

It may not be chosen by Newton/GR agreement.

## 13. Verification standard

Scientific completion requires:

1. tests-first RED -> GREEN;
2. exact inherited source/blob pins;
3. exact rational projector and finite-group arithmetic;
4. deterministic ledger regeneration;
5. inherited v15.31 regression;
6. exact-head GitHub Actions success;
7. no post-certification scientific edits.

No result is claimed by this design document alone.
