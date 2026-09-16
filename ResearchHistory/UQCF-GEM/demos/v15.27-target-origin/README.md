# v15.27 — Pre-Time Source→Cycle-Response Target Origin Gate

**Status:** `PRETIME_CYCLE_TARGET_ORIGIN_AUDIT_STOP`  
**Selector verdict:** `PRETIME_CYCLE_TARGET_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY`

v15.25 killed bare compatibility as a gravity-before-time canary. v15.26 then showed that a metric-free topological response operator can resolve all 50 cycle degrees **once a response target is supplied**. v15.27 asks whether the frozen ontology itself supplies that target.

It does not. The result is a scoped branch-stop theorem, not a universal no-go against deeper physics.

## 1. Exact factorization obstruction

The frozen source law is

```text
B1 j + q = 0.
```

v15.26 uses a response operator `R=[B2^T;H]` with full cycle rank:

```text
rank(R Z)=50=dim ker(B1).
```

Suppose the physical response target were inherited from the source quotient alone for every admissible current:

```text
R j = F(B1 j).
```

For any closed cycle `z in ker(B1)`, `j` and `j+z` have the same source. Therefore the factorization would require `Rz=0` for every cycle, equivalently `R` would factor through `B1`. But the executed `RZ` has rank 50 and smallest singular value about `0.8677674782`.

Hence the actual response coordinates of arbitrary admissible currents **do not factor through q**. Any map `q -> y` is an additional section/constitutive law, not inherited cycle data.

A direct same-q witness changes the response by about `1.118033989` while leaving the source unchanged to numerical precision.

## 2. Microscopic inheritance fails the quotient

A tempting rule is to inherit the target from the microscopic incidence representative `delta_b`:

```text
y_micro = -R delta_b.
```

But `delta_b` and `delta_b+B2 f` produce exactly the same source because `B1 B2=0`. Their inherited targets differ by about `4.472135955`. So microscopic inheritance depends on which representative of the same source class was chosen.

Verdict: `OBSTRUCTED_NOT_QUOTIENT_COVARIANT`.

## 3. Hodge/minimum action remains conditional

Changing the positive edge inner product changes the minimum-action current and therefore its response target. In the frozen control:

- current difference: about `0.108465704`;
- response-target difference: about `0.216053292`.

No edge metric has been derived. v13.01 and the archived Gate-A controls already stopped this route from being promoted by convenience.

Verdict: `CONDITIONAL_ON_UNDERIVED_EDGE_INNER_PRODUCT`.

## 4. Zero target is lawful but not derived

`y=0` defines a mathematically valid section because the v15.26 response rank is full. It is not implied by compatibility or topology, and it differs from the Hodge representative by current norm about `0.8571428571`.

Verdict: `LAWFUL_EXTRA_CONDITION_NOT_DERIVED`.

## 5. Topology + source-linearity + covariance still leave a family

To test whether symmetry alone closes the gap, define a metric-free vertex-to-face averaging map `A` from the existing torus incidence structure and a closed cycle

```text
z(q)=B2 A q,
B1 z(q)=0.
```

Then for any real scalar `alpha`,

```text
y_alpha(q)=alpha R z(q)
```

is source-linear, depends only on q, is quotient-covariant, and is covariant under simultaneous relabeling of vertices/edges/faces. The gate freezes `alpha=-1,0,+1` before adjudication.

All three laws satisfy the source equation and the rank gate, yet they give distinct targets and currents. Fresh local values:

- topology cycle norm: `0.8660254038`;
- target spread: `3.3166247904`;
- current spread: `1.7320508076`;
- relabeling error: about `5.17e-15`.

Thus topology, linearity and relabeling covariance are insufficient to choose the target.

Verdict: `LAWFUL_BUT_NONUNIQUE`.

## 6. Homology basis is coordinate, not physics

Replacing the two period rows by an invertible linear combination changes their target coordinates but reconstructs the same current. The reconstruction error is about `2.4e-15`, while the numerical period coordinates change by about `0.8571`. A preferred basis cannot be treated as new physics.

## 7. Candidate adjudication

```text
SOURCE_QUOTIENT_INHERITANCE      OBSTRUCTED_R_DOES_NOT_FACTOR_THROUGH_B1
MICROSCOPIC_DEFECT_INHERITANCE   OBSTRUCTED_NOT_QUOTIENT_COVARIANT
HODGE_MINIMUM_ACTION              CONDITIONAL_ON_UNDERIVED_EDGE_INNER_PRODUCT
ZERO_CYCLE_TARGET                 LAWFUL_EXTRA_CONDITION_NOT_DERIVED
TOPOLOGY_LINEAR_COVARIANT_FAMILY LAWFUL_BUT_NONUNIQUE
```

Historical boundaries remain:

- metric origin: `CONDITIONAL_NOT_DERIVED`;
- response rank: `CONDITIONAL_ON_TARGET`;
- source→geometry pairing: `REQUIRES_NEW_AXIOM_OR_CALIBRATION`.

No stopped branch is reopened by renaming it.

## 8. Scientific verdict

```text
cycle target derived:       NO
signal of life:             NO
gravity canary certified:   NO
```

The exact scoped verdict is

```text
PRETIME_CYCLE_TARGET_IRREDUCIBLE_RELATIVE_TO_FROZEN_ONTOLOGY
```

The next allowed object is therefore:

```text
EXPLICIT_PRETIME_SOURCE_TO_HIGHER_INCIDENCE_COUPLING_AXIOM_OR_NEW_DERIVED_STRUCTURE
```

That does **not** mean an arbitrary axiom should be added. Any restart must have independent quantum/information-theoretic motivation and preregistered consequences before consulting gravity-like behavior.

## Claim boundary

No holonomy strength, Newtonian law, inverse-square behavior, Einstein residual, pruning, entropy or physical time is used as a selector. No actual outcome, physical metric, source calibration, gravitational field or GR equation is derived. Pre-time reversible change remains allowed. Pillar 3 remains OPEN.

Local TDD recorded 21 missing-model failures and six missing-presentation failures before implementation. All 27 new checks then passed locally and the 24-second H.264 movie fully decoded. Exact-head GitHub Actions independently reruns the selected research stack and publishes only after release-asset size/SHA-256 verification. Self-review only; no independent peer review or empirical validation.
