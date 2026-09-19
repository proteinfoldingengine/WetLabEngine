# UQCF-GEM v15.40 — Global-Balance Specificity and Blind Operational Geometry

**Date:** 2026-09-19  
**Base:** v15.39 exact certified head `0f3e10602929dd0a148b195f32406efa52082070`  
**Status at design freeze:** preregistration only; no v15.40 geometry observable or control has been executed  
**Pillar 3:** OPEN

## 1. Purpose

v15.39 introduced an explicitly new higher-incidence source semantics and tested three explicitly
new response axioms. Only global balance completion survived the common finite canary:

```text
D y = kappa,
D = 4I - A,
y in im(B2).
```

Its exact remote support and noncommuting-axis precursor are scientifically relevant, but they may
be generic consequences of inverting a connected balance operator. v15.40 therefore asks the
next necessary question before any curvature, continuum, Newton, or Einstein-facing work:

> Does the frozen global-balance response define an operational face geometry that agrees with an
> independently queried incidence geometry, while matched covariant balance operators do not?

This is a specificity and internal-correspondence gate. It is allowed to downgrade the
interpretation of v15.39.

## 2. Frozen inherited content

The following are inputs and may not be modified after this design is committed:

1. the v15.39 source occurrence and lift
   `kappa = a sigma(f,e) B2 u_f`;
2. the canonical boundary sector `B_L = im(B2)`;
3. the v15.39 global-balance candidate on that sector;
4. the odd periodic sizes `L=5,7,9` and locked `L=11`;
5. exact rational arithmetic and the projective-scale firewall;
6. the v15.39 claim boundary: the source and response axioms are new assumptions, not consequences
   of the earlier frozen ontology.

Evidence pins:

```text
v15.39 certified head:
  0f3e10602929dd0a148b195f32406efa52082070
v15.39 source_axiom_canary.py blob:
  620a8a64ed93d8c30a6e04730ed5bfc0e6e1252a
v15.39 RESULTS.json blob:
  ac8eb10ed90360fee6dcc0f170f19fffd0d74116
representation_actions.py blob:
  7260147cd6ca47ec21634172b44b98de726904af
v15.39 exact-head Actions run:
  35454923008
```

No v15.39 candidate formula, observable, result, or ledger is rewritten.

## 3. Spaces and canonical source normalization

Let `F_L = Q^(L^2)` be the face-chain coordinate space and

```text
F_L^0 = {x in F_L : sum_f x_f = 0}.
```

For face `f`, define the centered unit source

```text
s_f = e_f - (1/L^2) 1.
```

On the periodic complex, `B2|_(F_L^0)` is an exact isomorphism onto `B_L`; v15.40 must
reverify this at every size. Thus the canonical face-potential coordinate `u_f in F_L^0` is
unique whenever

```text
y_f = B2 u_f.
```

For the frozen survivor,

```text
D_ax u_f = s_f,
D_ax = 4I - A_ax,
```

where `A_ax` is the v15.39 sum of the four primitive axial translations. The corresponding edge
response is `y_f=B2 u_f`.

The geometry audit uses the positively normalized centered source `s_f`. It must separately
verify that all four elementary source occurrences at face `f`, after the frozen incidence-sign
normalization, produce the same projective response ray. No absolute physical coupling is inferred.

## 4. Strict input separation

The gate has three components with nonoverlapping inputs.

### 4.1 Response-geometry constructor

The response-geometry constructor receives only:

- the labeled centered source vectors `s_f`;
- the labeled face-potential response vectors `u_f`;
- exact rational arithmetic.

It may not receive or query:

```text
B1, B2, A, D, translations, D4 matrices,
face coordinates (x,y), graph distances,
target adjacency, eigenspectra, or candidate labels.
```

It may not invert the response matrix or reconstruct `D` or `A`.

### 4.2 Incidence-target constructor

The incidence-target constructor receives only the signed support pattern of `B2`. It may not
receive or query:

```text
A, D, response vectors, response pairings,
translations, D4 matrices, face coordinates (x,y), or precomputed graph distances.
```

### 4.3 Adjudicator

Only the adjudicator may receive the frozen outputs of the two constructors. It compares exact
sets and booleans; it may not tune either construction after comparison.

The implementation must keep these interfaces separate and test them with hostile sentinels that
raise if a forbidden object is supplied or accessed.

## 5. Response-derived operational geometry

For two distinct faces `f,g`, define the exact source-response work

```text
R(f,g) = <s_f - s_g, u_f - u_g>,
```

using only the canonical face-chain/face-cochain evaluation pairing. This is not a fitted inner
product or a supplied edge metric. For the global-balance candidate it equals the effective
resistance expression

```text
(e_f-e_g)^T D_ax^(-1) (e_f-e_g),
```

but the response-geometry constructor is forbidden to use that formula or access `D_ax`.

The exact geometry protocol requires:

1. symmetry: `R(f,g)=R(g,f)`;
2. identity: `R(f,f)=0`;
3. strict separation: `R(f,g)>0` for `f != g`;
4. triangle inequality for every ordered triple;
5. invariance under the deterministic simultaneous relabeling in Section 8;
6. projective invariance of all verdicts under `u -> lambda u` for
   `lambda in {1, 7/3}`.

Let

```text
R_min = min_{f != g} R(f,g)
N_R   = {{f,g} : f != g and R(f,g)=R_min}.
```

Only equality, order, and ratios `R/R_min` may adjudicate. No floating tolerance or absolute
scale may appear.

## 6. Independently queried incidence geometry

Using only `B2), define the unordered face-neighbor relation

```text
N_B2 = {{f,g} : f != g and there exists edge e
                  with (B2)_(e,f) != 0 and (B2)_(e,g) != 0}.
```

The target constructor must verify that every face has exactly four such neighbors and that the
resulting graph is connected. It then computes exact unweighted all-pairs distances using only
`N_B2`.

The primary correspondence predicate is

```text
N_R = N_B2.
```

If it holds, graph distances reconstructed from `N_R` must equal the independently computed
`N_B2` distances. This second equality is a consistency check, not additional independent
evidence beyond neighbor recovery.

## 7. Frozen controls

Every control is passed through the identical response-geometry constructor. Control identity is
hidden from that constructor.

### 7.1 Historical local controls

1. **Direct inheritance:** `u_f=s_f`.
2. **One-incidence transport:** `u_f=A_ax s_f`.

These determine whether the new geometry predicate rejects the two v15.39 candidates already
classified as local. They are controls, not reopened response candidates.

### 7.2 Matched covariant global-balance controls

Define two alternative four-neighbor, translation-covariant, D4-invariant generator sets on every
odd torus:

```text
S_diag  = {(+1,+1), (+1,-1), (-1,+1), (-1,-1)}
S_step2 = {(+2,0), (-2,0), (0,+2), (0,-2)}  mod L.
```

Let

```text
A_c = sum_(t in S_c) T_t,
D_c = 4I - A_c,
D_c u_f^(c) = s_f  on F_L^0.
```

Each matched control must independently pass:

- exact connectedness of its generator graph;
- exact invertibility of `D_c|_(F_L^0)`;
- translation and D4 covariance;
- valence four;
- the complete metric protocol in Section 5;
- the same orientation, additivity, relabeling, scale, and holdout checks.

A control failure of structural admissibility invalidates the protocol; it cannot be counted as
evidence for canonical specificity.

The control generator sets and formulas are frozen here. No alternative control may be substituted
after seeing output.

## 8. Sizes, relabeling, and exhaustive sweeps

Use:

```text
controls: L=5,7,9
locked holdout: L=11
```

At every size:

1. reconstruct the complex and every operator independently;
2. evaluate every source face, not a sample;
3. evaluate all unordered face pairs for `R`;
4. evaluate every ordered triple for the triangle inequality;
5. verify all four elementary edge-occurrence orientations at a fixed face and their images under
   translation/D4 generators;
6. verify two-source additivity using amplitudes `2/3` and `-5/7`;
7. verify `lambda=1` and `lambda=7/3`;
8. repeat the full comparison after the deterministic non-geometric face relabeling

```text
pi(i) = (2i + 1) mod L^2.
```

Because `L^2` is odd, `pi` is a bijection. Relabel `B2` columns, sources, and response labels
consistently, then require the two constructor outputs and final verdict to transform equivariantly.

No random seed, sampling rule, or post-output case selection is permitted.

## 9. Construction firewall

Candidate and control construction must record:

```text
spectrum_queries = 0
spectral_edge_parameters = 0
geometry_fit_parameters = 0
candidate_specific_thresholds = 0
coordinate_queries_in_response_geometry = 0
B2_queries_in_response_geometry = 0
response_queries_in_incidence_target = 0
operator_inversions_in_response_geometry = 0
```

The exact solves used to generate `u_f` are allowed only in the response-generation layer. They
are not allowed in the response-geometry constructor.

Forbidden adjudicating inputs include:

- square-grid coordinates or drawings;
- torus displacement labels;
- continuum distance formulas;
- Newtonian or Einstein targets;
- full or partial eigenspectra;
- fitted monotone transformations of `R`;
- minimum-norm/Hodge selection outside the frozen global-balance axiom;
- pruning, entropy, outcome selection, or physical time.

## 10. Mechanical adjudication

First classify the protocol:

```text
RESPONSE_GEOMETRY_PROTOCOL_INVALID
```

if any evidence pin, input-separation sentinel, exact structural check, matched-control
admissibility check, relabeling check, scale check, or holdout rule fails.

Otherwise classify the canonical response:

```text
NO_RESPONSE_DERIVED_GEOMETRY
```

if its `R` fails any metric requirement or if `N_R != N_B2` at any required size.

If the canonical response passes, classify specificity:

```text
GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY
```

if any historical or matched control passes the complete metric protocol and also satisfies
`N_R=N_B2` at every required size.

Only return

```text
CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES
```

if all of the following hold:

- the canonical response passes the complete metric protocol;
- `N_R=N_B2` at `L=5,7,9,11`;
- both constructor outputs are equivariant under the frozen relabeling;
- both projective scales give identical verdicts;
- both matched global-balance controls are structurally admissible;
- each historical control is evaluated without requiring it to pass the metric protocol;
- no historical or matched control passes both the complete metric protocol and the canonical
  correspondence rule;
- the locked `L=11` result uses unchanged formulas and criteria;
- every construction-firewall counter remains zero.

No intermediate numerical score, correlation, accuracy percentage, or fitted cutoff may replace
these exact set-equality rules.

## 11. Interpretation firewall

A positive result would establish only:

> Conditional on the explicitly new v15.39 source and global-balance axioms, an operational
> geometry built from exact source-response work recovers the face adjacency independently queried
> from `B2`, while the preregistered covariant controls do not.

This would be a finite internal Level-1 correspondence candidate because an independently queried
geometry agrees with an exactly conserved response `B1 y=0`. It would not show that the response
axiom, the primitive translation operator, or the square complex was derived from the pre-v15.39
ontology.

The ledger must retain:

```text
new_source_semantics_axiom_inherited = true
new_global_balance_response_axiom_inherited = true
source_axiom_derived_from_frozen_ontology = false
response_axiom_derived_from_frozen_ontology = false
physical_metric_derived = false
spacetime_derived = false
physical_gravity_derived = false
continuum_limit_derived = false
einstein_equations_derived = false
uses_pruning = false
uses_entropy = false
uses_physical_time = false
scientific_breakthrough = false
Pillar_3 = OPEN
```

`GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY` would supersede the interpretation of v15.39 by showing
that its nonlocal signal lacks operator specificity. The v15.39 exact artifact remains immutable;
the downgrade is recorded monotonically in the v15.40 ledger.

## 12. Stop rules and next objects

- If the protocol is invalid, repair only the protocol defect without inspecting scientific
  output.
- If there is no response-derived geometry, stop this mechanism. Do not tune `R`, add a monotone
  transform, or change the response axiom.
- If the result is generic Green-operator geometry, record the downgrade and do not proceed to
  curvature correspondence for this mechanism.
- If canonical specificity survives, the next gate may test a formal connection/curvature object
  and a source-curvature correspondence. It may not fit Newton or GR.

Mechanical next-object ledger:

```text
RESPONSE_GEOMETRY_PROTOCOL_INVALID
  -> REPAIR_BLIND_GEOMETRY_PROTOCOL_BEFORE_ANY_ADJUDICATION

NO_RESPONSE_DERIVED_GEOMETRY
  -> CLOSE_GLOBAL_BALANCE_GEOMETRY_INTERPRETATION_WITHOUT_TUNING

GENERIC_GREEN_OPERATOR_GEOMETRY_ONLY
  -> DOWNGRADE_V1539_TO_GENERIC_INVERSE_OPERATOR_GLOBALITY

CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES
  -> PREREGISTER_FORMAL_CONNECTION_CURVATURE_AND_SOURCE_CORRESPONDENCE_GATE
```

## 13. Planned artifacts and verification

After this design is reviewed and an implementation plan is separately approved:

1. create an additive v15.40 demo directory;
2. add behavior-first RED tests before implementation;
3. implement separate response-geometry, incidence-target, and adjudication modules;
4. generate a canonical `docs/RESULTS.json`;
5. document theorem/computation/interpretation boundaries in a README;
6. run inherited v15.38 and v15.39 frontier regressions;
7. require exact byte-identical result replay;
8. require an exact-head GitHub Actions success;
9. leave the PR draft/open/unmerged.

To control Actions cost, exploratory calculations must not run in CI. The intended sequence is one
missing-implementation RED receipt, staged deterministic implementation checks only when an
interface is complete, and one final exact-head certification. All repository changes remain
additive relative to the certified v15.39 head.
