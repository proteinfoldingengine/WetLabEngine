# UQCF-GEM v15.41 — Formal Connection, Curvature, and Source Correspondence

**Date:** 2026-09-19
**Base:** v15.40 exact certified head `84aa1c81fd86ac4d7a06015482f98572f3afc05f`
**Status at design freeze:** preregistration only; no v15.41 connection, curvature, or source-correspondence observable has been executed
**Pillar 3:** OPEN

## 1. Purpose

v15.40 established, at `L=5,7,9,11`, that the exact source-response work metric of the frozen
global-balance response recovers the independently queried `B2` face-neighbor relation. Four
preregistered controls fail the same all-size metric-and-correspondence rule. Its certified result is

```text
CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES
```

That result does not provide a connection, curvature, a source-curvature law, spacetime, or gravity.
v15.41 asks the next narrower question:

> Does the frozen v15.40 operational geometry determine, up to explicitly enumerated local gauge,
> a formal discrete metric connection; and, only if it does, does the connection's exact linearized
> curvature response correspond to the independently frozen centered source carrier?

The first admissible result is a non-identifiability result. No frame, orientation, discrete Hodge
map, curvature contraction, or tie-breaker may be selected after output is inspected.

## 2. Historical boundary

Earlier Retained-Atlas work already contains a conditional metric-affine/polar connection and a
retained curvature-current stationarity law. In particular, the historical chain

```text
retained charts -> Gamma_R -> holonomy/W3 -> J_R -> curvature-current stationarity
```

is evidence about a different, already assumed connection container. It is not a derivation of a
connection from the v15.40 response geometry.

Therefore:

- historical connection, holonomy, current, and stationarity artifacts are forbidden inputs to every
  v15.41 adjudicating constructor;
- they may be evaluated only after the v15.41 verdict is frozen;
- any such evaluation is labeled `NON_ADJUDICATING_HISTORICAL_CROSS_CHECK`;
- agreement cannot upgrade the v15.41 verdict and disagreement cannot be repaired by changing the
  v15.41 constructor.

Pillar 2's historical status is not reopened. Pillar 3 remains `OPEN` for every v15.41 outcome.

## 3. Frozen inherited content

The following v15.40 objects are immutable inputs:

1. the centered sources `s_f=e_f-(1/L^2)1`;
2. the exact face-potential responses `u_f` for each preregistered family;
3. the exact work matrix

   ```text
   R(f,g) = <s_f-s_g, u_f-u_g>;
   ```

4. the response-derived minimum-neighbor relation `N_R`;
5. the independently constructed `B2` neighbor relation `N_B2`;
6. sizes `L=5,7,9` and locked holdout `L=11`;
7. exact rational arithmetic, common projective scales `1` and `7/3`, and the deterministic
   relabeling `pi(i)=(2i+1) mod L^2`;
8. the five v15.40 families and all v15.40 metric/admissibility results.

Evidence pins:

```text
v15.40 certified head:
  84aa1c81fd86ac4d7a06015482f98572f3afc05f
v15.40 result:
  CANONICAL_INCIDENCE_GEOMETRY_SPECIFICITY_SURVIVES
v15.40 exact-head Actions run:
  35468963309
v15.40 exact-head Actions job:
  105966319336
v15.40 pull request:
  51
```

Implementation must pin the exact blobs for the v15.40 design, generator, geometry constructor,
target constructor, gate, tests, and certified result before executing scientific code.

## 4. Three-layer input separation

### 4.1 Operational connection constructor

The constructor receives only:

- labels;
- exact work matrix `R`;
- response-derived neighbors `N_R`;
- one exact response field `u_f` only when computing the source-indexed linear perturbation;
- exact combinatorial structures reconstructed from `N_R` itself.

It may not receive or query:

```text
B1, B2, face coordinates, torus displacements,
the generating operator A, the defect D, eigenspectra,
candidate/control identity, historical Gamma_R or W3,
Newton/Einstein targets, or a supplied orientation.
```

### 4.2 Source-target constructor

The target constructor receives only the centered source family and signed support of `B2`. It may
construct `N_B2` and source carrier relations. It may not receive `R`, `N_R`, response fields,
connection data, curvature data, coordinates, candidate identity, or historical geometry.

### 4.3 Adjudicator

Only the adjudicator receives frozen outputs from both sides. It performs exact equality,
dimension, orbit, rank, and support tests. It cannot alter a constructor or normalize a failed
comparison after seeing output.

Hostile sentinels must make each forbidden access fail immediately.

## 5. Response-only tangent carrier

For each label `x`, let

```text
Star_R(x) = {y : {x,y} in N_R}.
```

The connection protocol is admissible only if every star has four elements, `N_R` is connected,
and every edge lies in exactly two chordless four-cycles reconstructed solely from `N_R`.

For `y,z in Star_R(x)`, use exact work values to partition the four directions into opposite pairs:
`y` and `z` are opposite when `R(y,z)` is maximal among pairs in the star. The protocol requires a
unique partition into two opposite pairs and equal minimum radial work. Failure returns
`CONNECTION_NOT_IDENTIFIABLE`; it is not a protocol error.

Define the formal two-dimensional tangent carrier `T_x` by assigning the four directions to

```text
{+e_1, -e_1, +e_2, -e_2}
```

with squared scale `R_min`. Ordering the two axes and choosing their signs are not data. The eight
choices form the local `D4` gauge group. Every reported object must be invariant under independent
local frame changes or be reported only by its gauge orbit.

No square-grid coordinate is used in this construction.

## 6. Baseline connection identifiability

For a directed response edge `x->y`, chordless four-cycles determine the two transverse direction
pairs, while the unique work-maximizing continuation at `y` determines the forward direction.
An admissible transport is an exact isometry

```text
P_xy : T_x -> T_y
```

that:

1. sends the direction `x->y` to its unique forward continuation at `y`;
2. sends the reverse direction consistently under `P_yx=P_xy^-1`;
3. preserves the unordered pair of the two chordless four-cycles incident to `{x,y}`;
4. preserves the exact tangent metric;
5. is equivariant under every automorphism of the weighted metric `R`;
6. is equivariant under the frozen non-geometric relabeling.

All finite admissible transports must be enumerated. A connection is a globally compatible choice
on every directed edge. Two choices are equivalent only when related by an explicitly enumerated
vertexwise `D4` gauge transformation.

The constructor returns `CONNECTION_NOT_IDENTIFIABLE` if there are zero admissible gauge orbits or
more than one admissible gauge orbit. It may proceed only when there is exactly one orbit. Choosing
an orientation, lexicographic frame, coordinate direction, minimum-norm matrix, or preferred
representative is forbidden.

## 7. Baseline curvature

For each based, oriented chordless four-cycle `C=(x_0,x_1,x_2,x_3,x_0)`, compute exact holonomy

```text
H_C = P_(x_3 x_0) P_(x_2 x_3) P_(x_1 x_2) P_(x_0 x_1).
```

Only the conjugacy class of `H_C` under local gauge is observable. Reversing cycle orientation must
replace `H_C` by its inverse and leave the curvature classification unchanged.

The following are recorded without physical interpretation:

- identity versus nonidentity holonomy;
- exact conjugacy class;
- orbit multiplicities under weighted-metric automorphisms;
- relabeling and projective-scale covariance.

This is formal discrete connection curvature. It is not Riemann curvature of a derived spacetime.

## 8. Source-indexed isotropic metric perturbation

The response field `u_f` is a scalar on labels. At each `x`, the local `D4` action on `T_x` admits
an invariant subspace of symmetric bilinear forms. The implementation must compute this invariant
subspace exactly rather than assume its dimension.

Proceed only if

```text
dim Sym^2(T_x^*)^D4 = 1
```

at every label and the one-dimensional spaces glue equivariantly. The unique projective isotropic
lift is then

```text
h_f(x) = u_f(x) g_x,
```

where `g_x` is the baseline tangent metric. The common scale is deliberately unfixed. Centering of
`u_f` removes additive constant gauge.

If the invariant lift is zero-dimensional, multidimensional, or fails to glue, return
`CONNECTION_NOT_IDENTIFIABLE`. No anisotropic response-to-metric rule may be inserted.

## 9. Linearized metric-compatible torsion-free connection

For every source label `f`, solve exact discrete metric-compatibility and torsion-closure equations
for the first-order transport perturbations

```text
delta P_xy[f]
```

induced by `h_f`. The equations are imposed on all directed edges and all chordless four-cycles,
with reverse-edge, automorphism, relabeling, and local-frame covariance. Pure vertex-frame changes
form the explicitly computed infinitesimal gauge subspace.

The equation system and gauge quotient must be assembled without `B2`, coordinates, `D`, historical
connection data, or source-target output. The implementation must publish its exact ranks and null
dimensions at every size.

Proceed only if each source has exactly one solution modulo gauge and the solution map is linear:

```text
delta P[a u_f + b u_g] = a delta P[u_f] + b delta P[u_g]
```

for the frozen exact amplitudes `a=2/3` and `b=-5/7`. Otherwise return
`CONNECTION_NOT_IDENTIFIABLE`.

This section is an identifiability test, not permission to select a discrete Levi-Civita convention.

## 10. Linearized curvature and carrier contraction

Differentiate the holonomy product mechanically to obtain `delta H_C[f]` for every source and
chordless four-cycle. It is forbidden to define curvature directly as a graph Laplacian of `u_f`;
any Laplacian identity must emerge as an independently checked theorem of the constructed
connection.

Curvature lives on response-derived four-cycles while sources live on labels. Let `I_R` be the exact
cycle-label incidence relation reconstructed only from `N_R`. Enumerate all linear contractions
from gauge-invariant linearized curvature data to the centered label carrier that are:

- invariant under reversal of auxiliary cycle orientation;
- equivariant under every weighted-metric automorphism;
- equivariant under relabeling;
- local to `I_R`;
- common to every candidate and control;
- free of fitted coefficients except an overall projective scale.

After quotienting overall scale, exactly one admissible contraction must remain. Zero or multiple
inequivalent contractions returns

```text
CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE
```

The surviving contraction, if any, produces an exact centered curvature response `K_f` on labels.
No componentwise rescaling, sign choice per source, fitted monotone map, tolerance, or source-specific
normalization is allowed. One global sign is orientation gauge and one common nonzero scale is
projective gauge.

## 11. Independent source correspondence

The source-side constructor freezes the centered target family `{s_f}` and `N_B2` before receiving
any connection output. The complete correspondence predicate for a family is:

1. its response work passes the inherited v15.40 metric protocol;
2. `N_R=N_B2` at every required size;
3. the baseline connection has exactly one gauge orbit;
4. the isotropic lift and linearized connection are unique modulo gauge;
5. the curvature carrier contraction is unique projectively;
6. there exists one common nonzero rational `alpha_L`, independent of `f`, such that

   ```text
   K_f = alpha_L s_f
   ```

   for every source `f`;
7. the same rule survives relabeling, source superposition, and common projective response scaling;
8. the locked `L=11` result uses the unchanged construction.

`alpha_L` is reported, not fitted per source. Equality is exact. Cross-size equality of `alpha_L`
is not required because the formal cell normalization changes with size; any physical continuum
interpretation is forbidden.

## 12. Controls

The v15.40 controls are reused without modification:

```text
DIRECT_INHERITANCE
ONE_INCIDENCE_TRANSPORT
MATCHED_DIAGONAL_BALANCE
MATCHED_STEP2_BALANCE
```

Every control receives the identical connection, curvature, and contraction code with identity
hidden. A control that fails the inherited metric prerequisites is recorded as inapplicable at the
first failed stage, not silently repaired.

In addition, the canonical response receives two frozen negative controls:

1. **scrambled response/source pairing:** apply the deterministic non-geometric permutation to
   response-field columns but not source columns after both constructors are frozen;
2. **cycle-incidence scramble:** apply the same permutation to curvature-cycle labels but not to
   the independent source carrier.

Both must fail exact source correspondence while the correctly simultaneous relabeling must pass.
These are adjudicator controls; they may not alter connection construction.

## 13. Construction firewall

Every run records zero for:

```text
coordinate_queries = 0
B2_queries_in_connection_constructor = 0
historical_connection_queries = 0
supplied_orientation_queries = 0
spectrum_queries = 0
floating_tolerances = 0
fitted_connection_parameters = 0
fitted_curvature_parameters = 0
source_specific_normalizations = 0
post_output_tie_breakers = 0
newton_or_einstein_targets = 0
```

All group orbits, ranks, linear systems, holonomies, and equalities use exact arithmetic. Algebraic
extensions, if required by an exact isometry calculation, must be represented symbolically and
verified by exact minimal-polynomial identities; floating approximations cannot adjudicate.

## 14. Mechanical outcomes

Return

```text
PROTOCOL_INVALID
```

if an evidence pin, input firewall, exact-arithmetic rule, structural control admissibility check,
relabeling rule, scale rule, or holdout rule fails.

Otherwise the first applicable scientific outcome is:

```text
CONNECTION_NOT_IDENTIFIABLE
```

if the tangent carrier, baseline connection, isotropic lift, or linearized connection is not unique
up to the frozen gauge rules.

If connection and curvature exist but the response-to-source carrier map is not unique, return:

```text
CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE
```

If all objects are identifiable but the canonical family fails `K_f=alpha_L s_f` at any required
size, return:

```text
CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE
```

If the canonical family passes but any preregistered control also passes the complete metric,
incidence, connection, and source-correspondence rule at every size, return:

```text
GENERIC_CONNECTION_CURVATURE_RESPONSE
```

Only return

```text
CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES
```

if the canonical family passes every clause in Section 11, all controls are evaluated under the
same code, neither negative scramble passes, no other family passes the complete all-size rule, and
every firewall counter remains zero.

## 15. Interpretation firewall

A positive result would establish only:

> Conditional on the explicitly new v15.39 source and global-balance response axioms, the finite
> v15.40 operational metric admits a unique formal connection in the preregistered response-only
> class, and its unique formal linearized curvature contraction is projectively proportional to the
> independently frozen centered source family at `L=5,7,9,11` while the controls fail.

It would not establish a physical affine connection, spacetime curvature, stress-energy, Newtonian
gravity, Einstein dynamics, a continuum limit, or scientific breakthrough. The discrete tangent,
isotropic lift, torsion equations, and contraction class introduced here are formal candidate
structures and must remain listed as new assumptions/restrictions.

The ledger must include:

```text
v1539_source_axiom_inherited = true
v1539_global_balance_response_axiom_inherited = true
v1540_operational_metric_inherited = true
formal_tangent_carrier_new = true
formal_connection_class_new = true
formal_isotropic_lift_class_new = true
formal_curvature_contraction_class_new = true
historical_connection_used_for_adjudication = false
physical_connection_derived = false
physical_curvature_derived = false
stress_energy_derived = false
spacetime_derived = false
continuum_limit_derived = false
einstein_equations_derived = false
scientific_breakthrough = false
Pillar_3 = OPEN
```

## 16. Stop rules and next objects

```text
PROTOCOL_INVALID
  -> REPAIR_ONLY_THE_PROTOCOL_DEFECT_BEFORE_ADJUDICATION

CONNECTION_NOT_IDENTIFIABLE
  -> RECORD_MISSING_CONNECTION_SELECTOR_WITHOUT_CHOOSING_A_FRAME_OR_DISCRETIZATION

CURVATURE_SOURCE_MAP_NOT_IDENTIFIABLE
  -> RECORD_MISSING_CURVATURE_TO_SOURCE_CARRIER_MAP_WITHOUT_FITTING_ONE

CONNECTION_IDENTIFIABLE_NO_CURVATURE_SOURCE_CORRESPONDENCE
  -> CLOSE_THIS_OPERATIONAL_CONNECTION_ROUTE_WITHOUT_TUNING

GENERIC_CONNECTION_CURVATURE_RESPONSE
  -> DOWNGRADE_TO_GENERIC_FORMAL_DISCRETE_RESPONSE

CANONICAL_OPERATIONAL_CURVATURE_SOURCE_SPECIFICITY_SURVIVES
  -> PREREGISTER_GENERAL_SIZE_AND_REFINEMENT_COMPATIBILITY_GATE
```

No v15.41 outcome authorizes Newton fitting, GR fitting, or merging the historical retained
connection into the adjudicating construction.

## 17. Planned artifacts and verification

After this design is reviewed and a separate implementation plan is approved:

1. create an additive v15.41 demo directory;
2. add behavior-first RED tests before implementation;
3. implement separate operational-connection, source-target, and adjudicator modules;
4. publish exact orbit counts, ranks, gauge dimensions, and stage outcomes;
5. generate a canonical `docs/RESULTS.json` with lossless encodings;
6. document theorem/computation/interpretation boundaries in a README;
7. run inherited v15.39 and v15.40 frontier regressions;
8. require byte-identical result replay;
9. require one final exact-head GitHub Actions success;
10. leave the pull request draft/open/unmerged.

Exploratory calculations are excluded from CI. Repository changes remain additive relative to the
certified v15.40 head.
