# UQCF-GEM Current Status

**As of:** 2026-09-13  
**Latest completed gate:** v15.05 — Frozen Composition-Law Audit / Monoidal Non-Selection and Log-Selector Boundary  
**v15.05 primary adjudication:** `FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE`  
**Secondary:** `LOG_SHAPE_REQUIRES_NEW_FUNCTIONAL_CALCULUS_ASSUMPTION`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`  
**Reproducibility policy:** scientific tolerances are enforced independently; frozen floating telemetry uses a tight mixed archive-binding tolerance rather than bitwise/absolute `1e-15` identity.

## Current scientific picture

The upstream source/admissibility problem is now localized beyond representation and local covariance to the exact kind of extra law that would be required to select a state-dependent source response.

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

shared-label / graph-site candidates
    -> five graph nodes do not canonically identify the five internal labels (v15.02)
    -> exact retained five-node graph -> five quantum subsystems remains underived (v15.03)
    -> state-independent scalar/current lift + independent local gauge -> center -> PGRL-null
    -> supplied quantum-state context permits noncentral covariant lifts
    -> no natural graph-site -> compatibility-parent map is certified

state-dependent local source law
    -> F(U rho U^dagger)=U F(rho) U^dagger
    -> full stabilizer forces F(rho) scalar on every rho spectral block
    -> for qubits: F_traceless(rho)=a(r)(rho-I/2)
    -> covariance fixes direction / spectral blocks but leaves a(r) free
    -> frozen source linearity, null-source behavior, positive scaling, and local-frame covariance preserve the freedom
    -> COVARIANCE_LEAVES_SPECTRAL_SOURCE_FREEDOM (v15.04)

composition-law selector audit
    -> v13.22 refinement source rule is supplied P -> P tensor I
       NOT a state-to-source equation P=F(rho)
    -> for any already-chosen local a(r), the labeled local-source sum
       M_a = sum_i I tensor ... tensor F_a(rho_i) tensor ... tensor I
       is associative, permutation-natural, and locally covariant
    -> linear / log / (1+r^2) remain projectively distinct while all satisfy those laws
    -> generic monoidal composition therefore does NOT select a(r)
    -> FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE (v15.05)

stronger conditional selector theorem
    -> assume one dimension-independent continuous scalar f acts by functional calculus
    -> center F_d(rho)=f(rho)-Tr[f(rho)]I/d
    -> impose F(rho tensor sigma)=F(rho) tensor I + I tensor F(sigma)
    -> pairwise spectral differences imply f(xy)-f(zy)=f(x)-f(z)
    -> multiplicative Cauchy equation + continuity
    -> f(x)=alpha log(x)+beta
    -> noncentral projective shape [log rho] for alpha>0
    -> premise is NOT frozen ontology
    -> LOG_SHAPE_REQUIRES_NEW_FUNCTIONAL_CALCULUS_ASSUMPTION (v15.05)

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

## Latest result — v15.05

### A. Frozen archive contains tensor structure, but not the required selector

The important archive fact is v13.22:

```text
R_tau(rho) = rho tensor tau
P -> P tensor I
```

with exact two-step composition and ETL/PGRL naturality. This does not define `P=F(rho)`. It transports an already-supplied source. The exact identity

```text
log(rho tensor tau) = log(rho) tensor I + I tensor log(tau)
```

therefore proves naturality of the PGRL exponential family; it does not prove that the source generator must itself be `log(rho)`.

The frozen dependency classification is

```text
NO_FROZEN_STATE_TO_SOURCE_COMPOSITION_SELECTOR
```

### B. Labeled monoidal composition preserves arbitrary local spectral response

For any local covariant law `F_a`, define

```text
M_a(rho_1 tensor ... tensor rho_n)
  = sum_i I tensor ... tensor F_a(rho_i) tensor ... tensor I.
```

This construction is associative, permutation/swap-natural, and independently local-unitary covariant for every already-chosen `a(r)`.

Executed witnesses:

```text
witnesses                                  = linear, log, 1+r^2
max local covariance error                 = 8.588717521894646e-16
max associativity error                    = 2.3551386880256624e-16
max swap-naturality error                  = 0.0
linear vs log projective separation        = 0.04038732286659571
linear vs polynomial separation            = 0.06600014410325687
log vs polynomial separation               = 0.025621359948040462
```

Thus all three laws compose correctly while remaining physically different projective source rays on the test product state.

```text
LABELED_MONOIDAL_COMPOSITION_PRESERVES_ARBITRARY_LOCAL_SPECTRAL_RESPONSE
```

This is an algebraic theorem; the numerics validate the implementation.

### C. A stronger law selects the logarithmic shape

If one additionally assumes one dimension-independent continuous scalar function `f` acts by functional calculus on every faithful finite-dimensional state and the centered **state-derived** source obeys

```text
F(rho tensor sigma) = F(rho) tensor I + I tensor F(sigma),
```

then diagonal spectral differences give

```text
f(xy)-f(zy) = f(x)-f(z),
f(xy)-f(x)  = c(y),
c(yz)       = c(y)+c(z).
```

Continuity yields

```text
f(x) = alpha log(x) + beta.
```

The central `beta` drops out after centering; positive-projective orientation corresponds to `alpha>0`.

Executed controls:

```text
centered log tensor error    = 1.6421465606029517e-15
centered linear tensor error = 0.3716732435890426
centered cubic tensor error  = 0.5553605272997411
```

But the premise is stronger than v15.04 conjugation-equivariance and is not derived anywhere in the frozen archive.

```text
CONTINUOUS_UNIVERSAL_SCALAR_FUNCTIONAL_CALCULUS_PLUS_CENTERED_TENSOR_DERIVATION_SELECTS_LOG_SHAPE
status = NEW_ASSUMPTION_NOT_FROZEN
```

### D. Scientific meaning

v15.05 changes the target from a vague search for “some composition law” to a sharply typed problem.

Generic tensor consistency is insufficient. The missing principle must constrain the **state-to-source map itself**, not merely specify how already-chosen local source operators are assembled across labeled subsystems.

The logarithmic source shape is therefore mathematically special under a clean stronger law, but it is not yet ontologically earned.

No downstream gravity/ADM/Einstein/cosmology target was used to choose the law. No entropy, pruning, or physical time was used as a pre-pruning selector.

## Relation to earlier gates

- **v15.04:** preserved and strengthened. The arbitrary qubit response `a(r)` survives generic monoidal composition.
- **v15.03:** preserved. State context can provide a covariant noncentral direction, but neither the exact carrier identification nor the spectral response is canonically selected.
- **v15.02:** preserved. Equal cardinality still does not create a node↔quantum-label identification.
- **v15.01:** preserved. The exact `C^125 -> C^25` parent/support relation remains available once a lawful parent source exists.
- **v14.04:** preserved. The provenance-to-source representation link remains missing.
- **v14.03:** preserved conditional. A supplied positive projective support source still selects the hidden first-contact/dual-ray chain.
- **v13.22:** clarified, not contradicted. Its source naturality is `P -> P tensor I` for an independently supplied source.
- **v13.28:** preserved. Absolute downstream source-to-geometry coupling remains underived.

## Preserved stack

- Pillar 1 — Global Atlas Closure: **COMPLETE**.
- Pillar 2 — Retained Curvature / Source-Current Compatibility: **CLOSED CONDITIONAL**.
- finite global quantum compatibility / hidden-completion structure: **PRESERVED**.
- QMAR and BKM trace/Weyl theorem: **PRESERVED**.
- source-current balance and conditional current selection: **PRESERVED**.
- v14.02 canonical local dual ray: **PRESERVED**.
- v14.03 supplied-projective-source selection chain: **PRESERVED CONDITIONAL**.
- v14.04 representation-link obstruction: **PRESERVED**.
- v15.01 compatibility parent/support compression: **PRESERVED**.
- v15.02 finite-label no-go: **PRESERVED**.
- v15.03 graph-site/local-gauge audit: **PRESERVED**.
- v15.04 equivariant source-law classification: **PRESERVED / STRENGTHENED**.
- v15.05 composition selector boundary: **CLOSED — FROZEN LAWS DO NOT SELECT `a(r)`**.
- projective coupled-source ray `[Sigma]`: **PRESERVED**.
- controlled ADM/Einstein comparisons: **EXTERNAL HELDOUT CORRESPONDENCE ONLY**.

## Still not derived

- an ontology-native principle selecting `a(r)`;
- the universal scalar-functional-calculus premise used in the conditional log theorem;
- `log(rho)` as the Genesis/provenance source law;
- a certified exact retained-node-to-quantum-site factorization;
- a natural graph-site-to-`C^125` compatibility-parent map;
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

Do **not** adopt `log(rho)` merely because v15.05 found a clean theorem under a stronger tensor-functional premise. That would convert a sufficient characterization into an invented ontology.

Do not select any state-to-source law using downstream PGRL/ADM/Einstein/gravity performance.

The next lawful question is:

> Does the already-earned ontology independently justify why a state-derived source should be one universal dimension-independent scalar functional calculus obeying the centered tensor derivation, or does it contain another equally strong source-law principle that selects the spectral response without downstream fitting?

Candidate origins must be audited upstream against the frozen structures themselves: Genesis/provenance composition, independent-system/disjoint-union structure, recoverability/compatibility functoriality, and any already-certified source grading or naturality law. If none supplies the premise, this branch stops with the spectral response irreducible relative to the frozen ontology and any chosen `a(r)` must be declared **NEW ASSUMPTION**.

Until then:

```text
retained graph -> exact quantum-site carrier       : STOPPED / UNDERIVED
state-independent scalar/current -> noncentral P   : NO-GO UNDER INDEPENDENT LOCAL GAUGE
state + supplied carrier -> covariant local P      : LAWFUL
local covariance -> spectral blocks/direction      : EXACTLY CLASSIFIED
local covariance -> spectral response a(r)         : NONUNIQUE
frozen generic composition -> unique a(r)           : NO
strong universal scalar tensor law -> log shape    : YES, CONDITIONAL / NEW ASSUMPTION
natural graph-site -> C^125/C^25 map               : NOT CERTIFIED
[A]_+ -> [P]_+                                      : EXACT CANONICAL COMPRESSION
[P] -> X* -> [g]                                    : CERTIFIED CONDITIONAL
Pillar 3                                            : OPEN
```
