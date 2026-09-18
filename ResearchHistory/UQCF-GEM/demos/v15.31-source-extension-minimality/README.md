# UQCF-GEM v15.31 — Source-Extension Representation / Minimal-Axiom Gate

## Adjudication

`FIBER_EXTENSION_CHANNELS_EXIST_BUT_NONUNIQUE`

v15.31 asks what representation-theoretic structure a future source-semantics axiom would minimally have to supply after v15.30 found `NO_TYPED_COMMON_CARRIER`.

It does **not** add that axiom.

## Exact result

The inherited 7×7 pre-time torus has:

```text
|G| = 392
dim C1 = 98
dim Q  = 48
dim Z = dim ker(B1) = 50
dim Y_cyc = 50
```

v15.28 already certifies `Y_cyc` as the cycle-space target on the same chain complex. Therefore the fiber-sensitive linear channel space is

```text
Hom_G(Z, Y_cyc) = End_G(Z).
```

The exact cycle-character distribution over the 392 automorphisms is:

```text
chi_Z =  50 :   1 element
chi_Z =  -6 :  28 elements
chi_Z =  -2 :  49 elements
chi_Z =   0 :  98 elements
chi_Z =   1 : 216 elements
```

Hence

```text
dim Hom_G(Z,Y_cyc)
 = (1/392) sum_g chi_Z(g) chi_Y(g)
 = (2500 + 1008 + 196 + 216) / 392
 = 3920 / 392
 = 10.
```

This is exact integer/rational character arithmetic. Restricted-cycle traces are independently spot-checked against the inherited signed-permutation action.

## Source-extension consequence

A minimal linear source extension would have the form

```text
0 -> K -> S -> Q -> 0.
```

Because the inherited symmetry group is finite and the working rational/real category has characteristic zero, Maschke semisimplicity applies: finite-dimensional linear extensions split equivariantly,

```text
S ~= Q direct_sum K
```

as representations.

That is an existence statement, not a canonical semantic identification. It does not say what physical provenance populates `K`, and it does not canonically select a splitting.

More importantly, the same-q fiber information has a **10-dimensional** equivariant linear response space into the already-certified cycle target. Symmetry therefore does not reduce the new source semantics to one projective channel.

The gate stops immediately on that exact nonuniqueness. A full irreducible decomposition cannot change the primary adjudication and is intentionally not used as busywork.

## What this means

v15.30 showed that the frozen ontology does not already contain the missing typed provenance/source bridge.

v15.31 now shows that simply saying "add a covariant fiber-sensitive linear source degree of freedom" is still far from enough. Even after the carrier is forced to respect the full inherited pre-time symmetry, ten independent linear intertwiner directions survive.

So the next physical theory input must do more than create a carrier. It must independently explain why one ray/member of this 10-dimensional space is physically privileged, or supply additional derived pre-time structure that reduces the space before any gravity observable is examined.

## Integral boundary

The rational/real semisimplicity result is not silently promoted to an integral-lattice theorem. No typed physical integral source extension currently exists in the archive, so v15.31 records the integral category as:

`NOT_ADJUDICATED_WITHOUT_TYPED_INTEGRAL_SOURCE_AXIOM`.

If an integral microscopic source law is later proposed, it requires its own exact gate.

## Claim boundary

v15.31 does not:

- add a physical source-semantics axiom;
- identify provenance with the cycle kernel;
- choose any member of the 10-dimensional channel space;
- reopen the v15.28 physical coupling solver;
- evaluate holonomy, Newton, Einstein, ADM, or any gravity canary;
- use metric/Hodge, entropy, pruning, recoverability, or physical time as a selector;
- derive physical gravity;
- close Pillar 3.

`Pillar_3 = OPEN`.

## Next required object

`INDEPENDENT_SOURCE_SEMANTICS_OR_DERIVED_STRUCTURE_REDUCING_THE_10_DIMENSIONAL_EQUIVARIANT_FIBER_CHANNEL_SPACE`

That object must be motivated before downstream gravity behavior is exposed.
