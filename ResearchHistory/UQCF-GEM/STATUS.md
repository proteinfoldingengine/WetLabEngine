# UQCF-GEM Current Status

**As of:** 2026-09-13  
**Latest completed gate:** v15.07 — Canonical Neutral Reference / Relative-Density Generator Gate  
**Primary adjudication:** `CANONICAL_NEUTRAL_RELATIVE_GENERATOR_EXISTS_SOURCE_IDENTIFICATION_UNDERIVED`  
**Secondary:** `UNIQUE_FRAME_INVARIANT_REFERENCE_IS_MAXIMALLY_MIXED`  
**Tertiary:** `NEUTRAL_TO_STATE_PGRL_ENDPOINT_SELECTS_LOG_PROJECTIVE_RAY_CONDITIONALLY`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`  
**Reproducibility policy:** scientific thresholds are enforced independently; frozen floating telemetry uses a tight mixed archive-binding tolerance.

## Current scientific picture

The upstream source problem has narrowed substantially.

```text
Genesis / frozen provenance
    -> source origin / grading / source-current structure
    -> source-current balance and conditional current selection
    -> no certified natural noncentral support-source representation (v14.04-v15.03)

state-dependent local source law
    -> F(U rho U^dagger)=U F(rho) U^dagger
    -> F(rho) is scalar on every rho spectral block
    -> qubit traceless law = a(r)(rho-I/2)
    -> covariance fixes direction, not response a(r) (v15.04)

generic composition
    -> already-supplied local source operators compose naturally
    -> arbitrary already-chosen a(r) survives associative / swap-natural composition
    -> frozen composition does not select a(r) (v15.05)

conditional log-selector theorem
    -> universal scalar functional calculus + centered tensor derivation
    -> f(x)=alpha log x+beta
    -> log projective shape selected
    -> premise was not frozen (v15.05)

recoverability multiplicativity
    -> root fidelity is multiplicative on independent recovery pairs
    -> -log F_root is additive
    -> this remains a scalar comparison generator
    -> exact recovery can stay F_root=1 while local spectra/source rays vary
    -> scalar recoverability does not select the operator source (v15.06)

canonical local operator
    -> require a normalized state with no preferred local quantum frame
    -> unique reference tau_d = I_d/d
    -> tau_{d1*d2}=tau_d1 tensor tau_d2
    -> Q_d(rho)=tau_d^{-1/2} rho tau_d^{-1/2}=d rho
    -> Q is multiplicative on independent product states
    -> K_d(rho)=log Q_d(rho)=log rho + log(d) I
    -> centered K = centered log rho
    -> canonical local multiplicative operator and additive Hermitian generator EARNED (v15.07)

neutral-to-state PGRL endpoint
    -> if sourcehood is defined as the generator preparing rho from tau_d
    -> [P]_+ = [centered log rho]_+
    -> positive projective log-generator ray selected exactly
    -> absolute source scale remains free
    -> sourcehood = neutral-preparation-generator is NOT a frozen source semantic (v15.07)

supplied positive projective support source [P]
    -> exact PGRL tangent
    -> canonical hidden projection
    -> hidden-tangent radial first contact X*(P)
    -> intrinsic local dual ray [g(P)]
    -> PROJECTIVE_SOURCE_RAY_SELECTS_DUAL_RAY remains certified conditional (v14.03)

retained/downstream source-geometry bridge
    -> projective coupled-source ray [Sigma] survives
    -> absolute source->geometry coupling remains NOT DERIVED
    -> v13.28 REQUIRES_NEW_AXIOM remains in force
```

## Latest result — v15.07

### A. Unique frame-neutral local state

For a normalized density operator `tau_d`, full local-frame invariance

```text
U tau_d U^dagger = tau_d  for every U in U(d)
```

forces `tau_d` into the full-unitary commutant. Therefore

```text
tau_d = I_d/d.
```

It also obeys

```text
tau_{d1*d2} = tau_d1 tensor tau_d2.
```

Executed dimensions and controls:

```text
dimensions                       = 2,3,4,5
commutant nullity                = 1 in every dimension
max commutant residual           = 0.0
max unitary-invariance error     = 1.9272741954495747e-16
max neutral-reference tensor err = 0.0
```

This is an exact symmetry theorem. “Neutral” means only **no preferred local quantum frame**. It does not mean Genesis Pin, physical vacuum, source-free state, equilibrium, pruning state, or time origin.

### B. Canonical multiplicative operator

Relative to `tau_d`, define

```text
Q_d(rho) = tau_d^(-1/2) rho tau_d^(-1/2) = d rho.
```

Then

```text
Q_{d1*d2}(rho tensor sigma)
  = Q_d1(rho) tensor Q_d2(sigma).
```

Executed maximum tensor error:

```text
6.675060769998483e-16
```

Thus the missing multiplicative object from v15.06 can be operator-valued and canonical without a basis choice or external reference state.

### C. Canonical additive Hermitian generator

For faithful `rho`,

```text
K_d(rho) = log Q_d(rho)
         = log rho + log(d) I.
```

After centering,

```text
K_d^0(rho)
  = log rho - Tr(log rho) I/d.
```

This is exactly the logarithmic projective shape isolated in v15.04-v15.05.

Executed controls:

```text
max log tensor-additivity error  = 2.896658855432451e-14
max centered-log identity error  = 2.8379538820721116e-15
max local-frame covariance error = 1.1729620862932955e-14
```

The logarithmic generator is therefore no longer merely a convenient candidate or a consequence of an independently postulated functional equation. It is the additive generator of the canonical relative-density operator determined by local-frame neutrality.

### D. Conditional neutral-to-state source-ray theorem

If one declares a PGRL preparation problem

```text
rho = exp(log tau_d + s P)/Z,
s > 0,
```

then modulo the central normalization,

```text
s P^0 = centered log rho.
```

Hence

```text
[P]_+ = [centered log rho]_+.
```

Executed controls:

```text
max endpoint reconstruction error = 6.123282208614186e-16
max generator identity error       = 3.5046408488399772e-15
product endpoint error             = 8.309111647037891e-16
```

Only the projective ray is selected. Absolute magnitude remains degenerate with the source parameter `s`, consistent with the v13.25-v13.26 source-normalization obstruction.

### E. Why physical source identification remains open

The audited frozen source semantics say:

```text
v13.04: PGRL acts at a supplied faithful state; it does not prescribe baseline-state origin.
v13.11: P is an independently supplied Hermitian source generator.
v13.25: Genesis/source anchoring and source-current compatibility exist, but do not define state-preparation sourcehood.
v13.26: Genesis anchoring is identity/compatibility structure; calling the origin itself source strength would add an axiom.
```

The v15.07 checker hash-binds these source-origin reports in addition to the prior v15 dependencies.

At one fixed state, finite PGRL deformations from linear, logarithmic, and polynomial generators all remain valid while their rays differ:

```text
linear vs log        = 0.06248625684944288
linear vs polynomial = 0.08772246091732862
log vs polynomial    = 0.025253513918714537
```

The canonical neutral-relative generator matches the logarithmic ray to

```text
5.77851202639302e-16.
```

So the mathematics selects a canonical log generator, while the frozen ontology has not yet declared that generator to be the source.

## Relation to earlier gates

- **v15.06:** materially advanced. The missing multiplicative object is no longer confined to a scalar recovery quantity; a canonical local operator-valued one now exists.
- **v15.05:** strengthened. Its conditional logarithmic shape is realized by an independently derived canonical relative-density construction, but the source-semantic premise remains open.
- **v15.04:** strengthened. The arbitrary qubit response family remains the full covariance classification, but frame-neutral relative-density structure supplies one canonical distinguished log generator.
- **v15.03:** preserved. State context is lawful, while the exact retained-node-to-quantum-site carrier remains underived.
- **v15.02:** preserved. Equal cardinality is still not an identification.
- **v15.01:** preserved. Compatibility parent/support compression remains exact once a lawful source on the parent/support is available.
- **v14.04:** preserved. Provenance-to-source representation remains open.
- **v14.03:** preserved conditional. A supplied positive projective support source selects the hidden first-contact/dual-ray chain.
- **v13.25-v13.26:** preserved. Absolute source calibration remains irreducible relative to the frozen ontology.
- **v13.28:** preserved. Absolute source-to-geometry coupling remains underived.

## Preserved pillar status

- Pillar 1 — Global Atlas Closure: **COMPLETE**.
- Pillar 2 — Retained Curvature / Source-Current Compatibility: **CLOSED CONDITIONAL**.
- Pillar 3 — GR/ADM Correspondence: **OPEN**.

## Still not derived

- `sourcehood = neutral-reference-to-state preparation generator`;
- identification of `I/d` with Genesis Pin or physical vacuum;
- a certified retained-node-to-quantum-site factorization;
- a natural graph-site-to-`C^125/C^25` compatibility map;
- Genesis/provenance -> v14.03 projective support source `[P]_+`;
- absolute source magnitude / observer calibration;
- physical stress-energy;
- source-to-solder/coframe law;
- absolute source-to-geometry coupling;
- physical metric/coframe/spacetime;
- ontology-native quantum continuum refinement;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

## Stop rule / next lawful frontier

Do **not** promote `centered log(rho)` to the physical source merely because the generator is now canonical.

Do **not** identify `I/d` with Genesis, vacuum, or a source-free physical state without an independently earned law.

Do **not** use downstream gravity/ADM/Einstein performance to supply the missing semantic identification.

The next lawful question is:

> Does the frozen Genesis/provenance ontology independently imply that **sourcehood is the generator that prepares a local quantum state from the unique frame-neutral reference**?

If yes, then the positive projective logarithmic source ray becomes canonically selected without downstream fitting.

If no, the source-law-selection branch stops here. The statement

```text
SOURCEHOOD_IS_NEUTRAL_PREPARATION_GENERATOR
```

must then be marked **NEW ASSUMPTION** before any downstream use.
