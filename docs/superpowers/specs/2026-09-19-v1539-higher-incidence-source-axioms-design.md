# UQCF-GEM v15.39 — Higher-Incidence Source Semantics and Response-Axiom Canary

**Date:** 2026-09-19  
**Base:** v15.38 exact certified head `825b47b276c6a17df35e6620f6de6630a1d729e2`  
**Status at design freeze:** preregistration only; no candidate has been executed against the canary  
**Pillar 3:** OPEN

## 1. Purpose

v15.37 established that the frozen ontology does not select the remaining response function in
`T=f(A)`. v15.38 certified a nonselective admissibility contract for explicitly new response
principles.

v15.39 is the first gate allowed to introduce new physics content. It must not pretend that
choosing `f(A)` alone resolves the earlier source-typing obstruction. The gate therefore
preregisters:

1. one explicit higher-incidence source-semantics axiom that supplies a typed same-`q`
   fiber source;
2. three competing response axioms;
3. one common adversarial canary applied without candidate-specific tuning.

Every new item below is labeled **NEW ASSUMPTION**. No item is claimed to follow from the
v15.38 frozen ontology.

## 2. Frozen chain-complex setting

For each odd periodic size `L`, use the inherited square relational 2-complex

```text
C2 --B2--> C1 --B1--> C0
```

with exact `B1 B2 = 0`.

Let

```text
Z_L = ker(B1)
B_L = im(B2)
H_L = Z_L / B_L
```

and use the canonical splitting already identified at `L=7`,

```text
Z_L = H_L direct_sum B_L,
```

subject to fresh exact verification at `L=5,7,9,11`.

The canonical adjacency is

```text
A_L = T_(+x) + T_(-x) + T_(+y) + T_(-y).
```

The primitive translation valence is exactly `d=4`. Define the canonical defect operator

```text
D_L = 4 I - A_L.
```

No square-grid drawing is asserted to be physical space. It remains a finite relational canary
arena.

## 3. Common source-semantics axiom — NEW ASSUMPTION

### 3.1 Elementary source occurrence

An elementary source occurrence is a tuple

```text
s = (f, e, a)
```

where `f` is an oriented face, `e` is one oriented edge occurrence in the boundary of `f`,
and `a` is a rational amplitude.

Let `u_e` and `u_f` denote the corresponding basis chains and let

```text
sigma(f,e) = (B2)_(e,f) in {+1,-1}.
```

Use edge-chain amplitude convention

```text
delta_s = a u_e
q_s     = B1 delta_s.
```

The new higher-incidence fiber source is

```text
kappa_s = a sigma(f,e) B2 u_f.
```

Thus

```text
kappa_s in B_L subset Z_L
B1 kappa_s = 0.
```

The incidence sign makes the lift transform with the oriented occurrence rather than with an
arbitrary display convention.

### 3.2 Physical meaning and concession

This axiom declares that the parent-face occurrence is part of source identity. Two microscopic
sources with the same coarse `q` can therefore be physically distinct when their
higher-incidence provenance differs.

Consequently, the old statement “a complete face boundary is a `q=0` null” remains true only
for the coarse carrier `q`. It is **not** assumed to be a null in the enlarged source carrier.
This is the central new-ontology concession and must appear in the result ledger. The chain
identity `B1 B2=0` is unchanged.

The gate does not claim that frozen Genesis provenance derived this lift. It is an explicit,
falsifiable source-semantics proposal.

### 3.3 Composition

For a finite formal sum of occurrences, define

```text
delta = sum_s delta_s
q     = B1 delta
kappa = sum_s kappa_s.
```

This gives exact source additivity and sign reversal. No nonlinear composition rule, outcome
selection, pruning order, entropy, or physical time is introduced.

## 4. Three competing response axioms — NEW ASSUMPTIONS

Each candidate maps the common fiber source `kappa in B_L` to a response ray
`[y] subset B_L`. Absolute source-response normalization remains underived.

### C0 — Direct provenance inheritance

```text
y = kappa.
```

Motivation: the higher-incidence source content is inherited without propagation. This is the
minimal typed response and the strongest local comparator.

### C1 — One-incidence transport

```text
y = A_L kappa.
```

Motivation: the response is the sum over exactly one primitive incidence-neighbor action. This
is the minimal nontrivial transport rule and contains no radius or coefficient fitted from a
downstream target.

### C2 — Global balance completion

Require `y in B_L` and

```text
D_L y = kappa,
D_L = 4 I - A_L.
```

The candidate is admissible only if `D_L|_(B_L)` is exactly invertible. If so,

```text
y = (D_L|_(B_L))^(-1) kappa.
```

Motivation: away from the source, the response obeys exact incidence balance with the four
primitive translations. The rule is an algebraic inverse on the canonical boundary sector,
not a minimum-norm solution, Hodge pseudoinverse, fitted Green function, spectral-edge
interpolation, or metric optimization.

The inverse is not to be silently called derived. It is the strongest of the three explicit
new axioms and is allowed to fail if the exact boundary-sector inverse does not exist.

## 5. Projective scale discipline

For diagnostic reconstruction, use

```text
j_lambda = -delta + lambda y,   lambda != 0.
```

Then

```text
B1 j_lambda + q = 0
```

exactly for every `lambda`, because `y in Z_L`.

The implementation may set `lambda=1` as a canonical ledger representative, but no physical
coupling magnitude is inferred. Canary predicates must be invariant under nonzero rational
rescaling of `y`.

## 6. Preregistration firewall

The source axiom, candidate formulas, canary observables, sizes, nulls, and adjudication rules
in this document are frozen before any candidate response is evaluated.

Candidate construction must record:

```text
spectrum_queries = 0
spectral_edge_parameters = 0
gravity_fit_parameters = 0
candidate_specific_thresholds = 0
```

No candidate may be modified after seeing far-shell support, holonomy, Newton/GR, or
finite-size behavior. A failed candidate is recorded as failed.

## 7. Common adversarial canary

Apply exactly the same suite to C0, C1, and C2.

### 7.1 Sizes

Use independently reconstructed odd periodic systems

```text
L = 5, 7, 9
```

and a locked holdout

```text
L = 11.
```

The candidate formulas and source-lift rule are unchanged at every size.

### 7.2 Exact structural checks

For every size and candidate:

1. verify `B1 B2=0`;
2. verify `Z_L = H_L direct_sum B_L` with the expected dimensions;
3. verify `A_L B_L subset B_L`;
4. verify `kappa in B_L` and `B1 kappa=0`;
5. verify the candidate produces a unique nonzero response ray for every elementary source
   orientation;
6. verify `B1 j_lambda + q=0` exactly;
7. verify translation, D4, and source-orientation covariance using a generating set;
8. verify exact additivity and sign reversal;
9. verify the same formula and construction provenance at every size.

C2 additionally requires exact injectivity and surjectivity of `D_L|_(B_L)`.

### 7.3 Exact global-support observable

Let `f_0` be the source face and use torus face distance. Define the maximally remote shell

```text
R_L = {f : dist(f,f_0) is maximal}.
```

Define

```text
S_remote(y) = sum of y_e^2 over oriented edges incident to faces in R_L.
```

This is evaluated in exact rational arithmetic. The response reaches the far shell iff

```text
S_remote(y) > 0.
```

No floating threshold is permitted.

### 7.4 Exact noncommuting-holonomy precursor

For each face, pair perpendicular horizontal and vertical boundary edges. Define the exact
quadratic commutator precursor

```text
C_f(y) = sum_(perpendicular pairs h,v in boundary(f)) (y_h y_v)^2.
```

and the remote aggregate

```text
C_remote(y) = sum_(f in R_L) C_f(y).
```

`C_remote(y)>0` is the exact algebraic condition for a nonzero second-order
noncommuting-axis group-commutator term somewhere on the far shell. The commuting-axis control
has Lie bracket zero identically.

This precursor is used instead of a fitted floating holonomy threshold. Any later SU(2)
visualization is presentation-only and cannot affect adjudication.

### 7.5 Orientation, translation, and composition sweeps

At each size:

- evaluate all four edge-occurrence slots of one source face;
- translate the source to preregistered distinct faces;
- reverse the source amplitude;
- compose two separated sources with unequal rational amplitudes;
- verify exact covariance, odd response scaling, linear superposition, and quadratic
  commutator-precursor scaling.

### 7.6 Hostile controls

1. **Zero source:** `a=0` gives `q=kappa=y=0`.
2. **Coarse-only erasure:** discarding `kappa` gives no cycle response, exposing dependence on
   the new source axiom.
3. **Bare local cancellation:** `j=-delta` remains an exact compatibility solution but is not
   a solution of an adopted nonzero response axiom; this distinguishes conservation from the
   new constitutive content.
4. **Commuting transport axes:** exact commutator precursor is zero.
5. **C0/C1 locality controls:** these candidates are not excused from the far-shell tests.
6. **Holdout size:** `L=11` cannot alter formulas or introduce a parameter.
7. **Spectral-edge audit:** no eigenspectrum may be queried during candidate construction.

## 8. Candidate and gate adjudication

A candidate is `STRUCTURALLY_REJECTED` if any typing, covariance, composition, scale, or
multi-size admissibility check fails.

A structurally admissible candidate is `STRUCTURAL_ONLY_LOCAL` if either
`S_remote=0` or `C_remote=0` at any required size/orientation.

A candidate is `PRETIME_GLOBAL_ORGANIZATION_SURVIVES` only if:

- all structural checks pass;
- `S_remote>0` exactly for every required size and source orientation;
- `C_remote>0` exactly for every required size and source orientation;
- the commuting control is exactly zero;
- the `L=11` holdout passes unchanged;
- no forbidden construction query or parameter is used.

Overall mechanical outcomes:

```text
SOURCE_AXIOM_PROTOCOL_INVALID
NO_ADMISSIBLE_RESPONSE_CANDIDATE
ADMISSIBLE_CANDIDATES_NO_GLOBAL_SIGNAL
AXIOM_DEPENDENT_PRETIME_GLOBAL_ORGANIZATION_SIGNAL
```

The last outcome requires at least one candidate with
`PRETIME_GLOBAL_ORGANIZATION_SURVIVES`.

## 9. Interpretation firewall

Even the strongest positive outcome means only:

> Given the explicitly new higher-incidence source semantics and the frozen response axiom,
> the finite pre-time canary forces a covariant remote cycle response with a noncommuting
> holonomy precursor.

It does not mean the axiom was derived from the earlier ontology.

The ledger must retain:

```text
new_source_semantics_axiom_added = true
new_response_axiom_candidates_tested = true
source_axiom_derived_from_frozen_ontology = false
absolute_response_scale_derived = false
physical_gravity_derived = false
einstein_equations_derived = false
continuum_limit_derived = false
uses_pruning = false
uses_entropy = false
uses_physical_time = false
Pillar_3 = OPEN
```

A positive result is an **axiom-dependent pre-time signal**, not a Level-2 or Level-3 gravity
claim. Discrete Green/balance operators are prior mathematical structure; novelty, if any, lies
only in the exact typed integration and falsification result, not in inventing a graph
Laplacian.

## 10. Tests and deterministic artifacts

After this design is reviewed:

1. write the implementation plan;
2. add tests before the gate module and record the intended RED failure;
3. implement exact rational source lifts, candidate maps, and canary observables;
4. generate a deterministic `docs/RESULTS.json`;
5. add a README with theorem/computation/interpretation boundaries;
6. run inherited v15.37 and v15.38 regressions;
7. require byte-identical result replay;
8. require an exact-head GitHub Actions success before certification.

All v15.39 changes must be additive relative to the v15.38 certified head.
