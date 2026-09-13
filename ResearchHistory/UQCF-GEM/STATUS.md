# UQCF-GEM Current Status

**As of:** 2026-09-13  
**Latest completed gate:** v15.04 — Equivariant Source-Law Classification / Spectral Freedom Gate  
**v15.04 adjudication:** `COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM`  
**Secondary:** `COVARIANCE_FIXES_EIGENSPACES_NOT_SPECTRAL_RESPONSE_VALUES`; `DIRECTION_ONLY_NOT_RESPONSE_LAW`; `NO_UNIQUE_A_OF_R`; `V15_03_NUMERICS_ARE_ILLUSTRATIONS_OF_V15_04_THEOREM`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`  
**Reproducibility policy:** scientific tolerances are enforced independently; frozen floating telemetry uses a tight mixed archive-binding tolerance rather than bitwise/absolute `1e-15` identity.

## Current scientific picture

The upstream source/admissibility problem is now localized more sharply than “missing representation.”

```text
Genesis / frozen provenance
    -> retained source-origin / source-current structure
    -> gauge-trivial provenance cannot select a noncentral C^25 source (v14.04)
    -> richer provenance carriers exist, but no frozen natural support intertwiner is certified (v14.04)

compatibility parent/support
    -> exact parent H_Q = C^125
    -> exact support isometry L : C^25 -> C^125
    -> exact projective/covariant compression A -> L^dagger A L
    -> frozen provenance supplies no source class/tangent on that parent (v15.01)

shared-label candidate
    -> retained source graph has five nodes
    -> compatibility factors have five internal labels
    -> all 120 node<->label identifications remain inequivalent under earned gauge
    -> NO_CERTIFIED_SHARED_LABEL_CARRIER (v15.02)

graph-site candidate
    -> graph-indexed quantum models exist in the archive
    -> exact retained five-node graph -> five quantum subsystems is NOT certified
    -> state-independent scalar/current lift + independent local gauge -> center -> PGRL-null
    -> supplied quantum-state context permits noncentral covariant lifts
    -> five nontrivial quantum sites cannot literally equal C^125
    -> no natural graph-site -> compatibility-parent map is certified
    -> NO_CERTIFIED_GRAPH_SITE_FACTORIZATION (v15.03)

state-dependent local source law
    -> require only F(U rho U^dagger)=U F(rho) U^dagger
    -> stabilizer theorem forces F(rho) to be spectral in rho
    -> qubit traceless law is exactly a(r)(rho-I/2)
    -> covariance fixes eigenspaces/direction but leaves a(r) free
    -> existing source extensivity/linearity, null-source behavior,
       positive projective scaling, and local-frame covariance all preserve that freedom
    -> COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM (v15.04)

supplied positive projective support source [P]
    -> exact PGRL tangent
    -> canonical hidden projection
    -> hidden-tangent radial first contact X*(P)
    -> objective-independent local dual ray [g(P)]
    -> PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY remains certified conditional (v14.03)

retained/downstream source-geometry bridge
    -> projective coupled-source ray [Sigma] survives
    -> absolute source->geometry coupling remains NOT DERIVED
    -> v13.28 REQUIRES_NEW_AXIOM remains in force
```

The unresolved upstream package therefore contains at least three distinct missing pieces:

1. an earned retained-node-to-quantum-site carrier identification;
2. an earned natural map from that carrier into the existing `C^125 -> C^25` compatibility stack; and
3. if quantum-state context is used, an upstream principle selecting the spectral response law `a(r)` rather than choosing it from downstream performance.

## Latest result — v15.04

### A. Exact local-unitary equivariance theorem

Let `F(rho)` be Hermitian and satisfy

```text
F(U rho U^dagger) = U F(rho) U^dagger
```

for every local unitary `U`.

For every unitary in the stabilizer of `rho`, equivariance forces the same unitary to stabilize `F(rho)`. Writing

```text
rho = sum_alpha lambda_alpha Pi_alpha,
```

the stabilizer contains the full unitary group on every eigenspace. Its commutant is scalar on each eigenspace, so

```text
F(rho) = sum_alpha mu_alpha(spec rho) Pi_alpha.
```

Hence

```text
[F(rho), rho] = 0
LOCAL_UNITARY_EQUIVARIANCE_IMPLIES_SPECTRAL_SOURCE_LAW
COVARIANCE_FIXES_EIGENSPACES_NOT_SPECTRAL_RESPONSE_VALUES
```

For degenerate spectra, the full stabilizer statement is stronger than the commutator alone: `F(rho)` must be scalar across each degenerate eigenspace.

The converse also holds for every well-defined real permutation-equivariant spectral assignment that treats equal eigenvalues equally. No differentiability, entropy, pruning, dynamics, or time primitive is needed for this classification.

### B. Exact qubit classification

For

```text
rho = 1/2 (I + r_vec . sigma),   r = |r_vec| < 1,
```

any conjugation-equivariant local map has the form

```text
F(rho) = c(r) I + a(r) (rho - I/2).
```

After traceless/projective centering,

```text
F_traceless(rho) = a(r) (rho - I/2).
```

Therefore

```text
QUBIT_EQUIVARIANT_TRACELESS_MAP_IS_RADIAL
DIRECTION_ONLY_NOT_RESPONSE_LAW
```

The unresolved local freedom is one scalar response function `a(r)`.

### C. v15.03 linear/square collapse is exact

For every qubit density matrix,

```text
rho^2 - Tr(rho^2) I / 2 = rho - I/2.
```

The executed maximum identity error was

```text
7.850462293418876e-17
```

so the v15.03 near-zero linear/square projective residuals are now illustrations of an exact identity, not evidence for an empirical coincidence.

### D. Logarithmic law gives an exact nonconstant response

For faithful qubits,

```text
log(rho) - Tr(log(rho)) I / 2
  = artanh(r) rhat.sigma
  = [2 artanh(r)/r] (rho-I/2).
```

Thus

```text
a_log(r) = 2 artanh(r)/r.
```

The executed maximum formula error was

```text
1.2412670766236366e-16
```

and `a_log(r)` is nonconstant and strictly increasing on `0<r<1`.

### E. Exact projective-ray split criterion

For the supplied graph-site carrier,

```text
P_a(s,rho) = sum_i s_i iota_i[a(r_i)(rho_i-I/2)].
```

Distinct embedded single-site traceless terms are Hilbert-Schmidt orthogonal. Therefore two such sources define the same positive projective ray exactly when their response coefficients on all nonzero source-support sites differ by one common positive factor.

For the frozen source `(-1,0,0,+1,0)`, only sites `0` and `3` contribute.

```text
Control A support radii = [0.15, 0.63]
a_log(A support)        = [2.015205812486224, 2.353702044702441]
linear vs log residual  = 0.032643436536906496

Control B support radii = [0.52, 0.47]
a_log(B support)        = [2.2166913652661258, 2.1705120706949246]
linear vs log residual  = 0.010460821683241906
```

Because the radii differ and `a_log` is not constant, the linear and logarithmic global projective source rays are exactly distinct.

A third witness `a(r)=1+r^2` also gives different rays:

```text
A: linear vs (1+r^2) = 0.061186205628391485
B: linear vs (1+r^2) = 0.01972566676052767
```

### F. Frozen source axioms do not select `a(r)`

The audited source-law constraints carried by v13.26, v14.03, and v15.03 were:

- retained source amount/extensivity and homogeneous source-current scaling;
- positive projective source rescaling;
- independent local-unitary/frame covariance;
- additivity/linearity in retained scalar source coefficients;
- null-source compatibility.

The linear, logarithmic, and `1+r^2` witness laws all satisfy them simultaneously.

```text
max local-unitary covariance error       = 3.434312402059545e-16
max null-source norm                     = 0.0
max positive-scale projective residual   = 2.603703785810335e-16
max source-additivity error              = 3.510833468576701e-16
max source-homogeneity error             = 1.7763568394002505e-15
```

Therefore

```text
FROZEN_SOURCE_AXIOMS_DO_NOT_SELECT_SPECTRAL_RESPONSE_FUNCTION
NO_UNIQUE_A_OF_R
COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM
```

The distinction is structural: source extensivity constrains dependence on scalar source coefficients `s_i`; it does not impose a functional equation on the spectrum dependence `a(r)`.

The audited dependencies contain no certified tensor-state composition functional equation for this operator-valued source law. Such a composition/monoidal law could reduce the freedom, but unless independently recovered from frozen structure it would be a **NEW ASSUMPTION**.

### G. Exact reconciliation with v15.03

The v15.04 theorem reproduces the frozen v15.03 controls:

```text
A: frozen linear/log residual  = 0.03264343653690659
A: theorem linear/log residual = 0.032643436536906496
absolute difference            = 9.020562075079397e-17

B: frozen linear/log residual  = 0.010460821683241842
B: theorem linear/log residual = 0.010460821683241906
absolute difference            = 6.418476861114186e-17
```

and the exact theorem predicts zero linear/square residual, matching the frozen machine-level values.

```text
V15_03_NUMERICS_ARE_ILLUSTRATIONS_OF_V15_04_THEOREM
```

## Relation to earlier gates

- **v15.03:** preserved and analytically strengthened. State-context nonuniqueness is now classified exactly rather than inferred from candidate disagreement.
- **v15.02:** preserved. Matching five-element cardinality still does not supply a node-to-basis-label functor.
- **v15.01:** preserved. The `C^125 -> C^25` parent/support relation and compression law remain exact.
- **v14.04:** preserved/strengthened. Even once state context supplies a lawful local quantum direction, the upstream representation link and spectral response selector remain underived.
- **v14.03:** preserved conditional. Given a supplied positive projective support source `[P]_+`, hidden-tangent first contact and the local dual ray remain canonical.
- **v14.02:** preserved. A specified smooth compatibility boundary has its intrinsic objective-independent local dual ray.
- **v13.28:** preserved. Absolute downstream source-to-geometry coupling remains blocked in the frozen candidate classes.

## Preserved stack

- Pillar 1 — Global Atlas Closure: **COMPLETE**.
- Pillar 2 — Retained Curvature / Source-Current Compatibility: **CLOSED CONDITIONAL**.
- finite global quantum compatibility / hidden-completion structure: **PRESERVED**.
- QMAR and BKM trace/Weyl theorem: **PRESERVED**.
- source-current balance and conditional current selection: **PRESERVED**.
- v14.01 source-law nonuniqueness: **PRESERVED**.
- v14.02 canonical local dual ray: **PRESERVED**.
- v14.03 supplied-projective-source selection chain: **PRESERVED CONDITIONAL**.
- v14.04 representation-link obstruction: **PRESERVED / STRENGTHENED**.
- v15.01 exact compatibility parent/support compression: **PRESERVED**.
- v15.02 exact finite-label no-go: **PRESERVED**.
- v15.03 graph-site/local-gauge audit: **PRESERVED / ANALYTICALLY STRENGTHENED**.
- v15.04 equivariant source-law classification: **CLOSED — SPECTRAL FREEDOM REMAINS**.
- projective coupled-source ray `[Sigma]`: **PRESERVED**.
- controlled ADM/Einstein comparisons: **EXTERNAL HELDOUT CORRESPONDENCE ONLY**.

## Still not derived

- a unique operator-valued spectral source law `a(r)`;
- a certified exact retained-node-to-quantum-site factorization;
- a natural graph-site-to-`C^125` compatibility-parent map;
- Genesis/provenance selection of `a(r)`;
- Genesis/provenance -> `[A_prov]_+` on `C^125`;
- Genesis/provenance -> v14.03 projective support source `[P]_+`;
- absolute source magnitude or observer calibration;
- physical stress-energy;
- source-to-solder/coframe law;
- absolute source-to-geometry coupling;
- physical metric/coframe/spacetime;
- ontology-native quantum continuum refinement;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

## Stop rule / next lawful frontier

Do **not** choose `log(rho)`, linear `rho`, `rho^2`, `1+r^2`, or any other spectral response because it produces a better downstream PGRL/ADM/Einstein/gravity result. Do not invent a tensor-site identity, tie local frames, pad/reshape into `C^125`, invent an isometry, or promote a minimum-norm current.

The next lawful question is upstream and architectural:

> Does the already-frozen ontology independently contain a state-composition / monoidal / spectral functional law strong enough to constrain `a(r)`?

If such a law exists, it must be identified and hash-bound before consulting downstream gravity targets. If no such frozen law exists, the source-law branch stops with `a(r)` irreducible relative to the current frozen source axioms; any selected response law then enters explicitly as **NEW ASSUMPTION**.

Until then:

```text
retained graph -> exact quantum-site carrier       : STOPPED / UNDERIVED
state-independent scalar/current -> noncentral P   : NO-GO UNDER INDEPENDENT LOCAL GAUGE
state + supplied carrier -> covariant local P      : LAWFUL
local covariance -> source eigenspaces/direction   : EXACTLY CLASSIFIED
local covariance -> spectral response a(r)         : NONUNIQUE
frozen source axioms -> unique a(r)                 : NO
natural graph-site -> C^125/C^25 map               : NOT CERTIFIED
[A]_+ -> [P]_+                                      : EXACT CANONICAL COMPRESSION
[P] -> X* -> [g]                                    : CERTIFIED CONDITIONAL
Pillar 3                                            : OPEN
```
