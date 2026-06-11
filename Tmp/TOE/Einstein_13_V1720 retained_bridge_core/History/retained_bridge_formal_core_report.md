# The Retained Bridge: Formal Core Report

**Document status:** Frozen formal core memo  
**Scope:** Simulation-internal retained-information geometry  
**Primary result:** Non-associative retained recombination produces scale-stable non-metric information geometry with amplitude-like interference and a pruning-sourced dissipative-statistical retained-order arrow.  
**Claim boundary:** This is not a derivation of GR, unitary quantum mechanics, a Born rule, or thermodynamic entropy production. It is a bottom-up characterization of what the model actually builds.

---

## 1. Executive summary

The Retained Bridge model starts without physical spacetime and without physical time as a primitive. Its primitive structure is retained information, ordered recombination, and pruning / non-invertible retention. From those ingredients, the model builds a real local geometry: a metric, positive scalar curvature, a native connection, and amplitude-like interference across recombination histories.

The geometry is not ordinary Riemannian geometry at the native level. Its leading geometric object is non-metricity: the native transport does not preserve the metric. This non-metricity is shear-dominated rather than Weyl/dilation-dominated, and it remains stable under coarse-graining. The non-metricity is therefore not a microscopic artifact; it is an RG-stable metric-affine fixed-point feature.

The model also exhibits destructive cancellation among alternative recombination histories. This is amplitude-like interference, but it is not unitary quantum dynamics. The transport is non-invertible and non-norm-preserving; the interference is dissipative rather than unitary.

The dissipative behavior is tied to the retained-order / pruning structure. Forward and reverse behavior are asymmetric, loops drift, and un-pruned controls remove the effect. However, the retained-order arrow is not governed by a strict scalar Lyapunov function and does not satisfy a state-defined thermodynamic entropy-production law under the pre-registered entropy candidates. The arrow is therefore best described as **dissipative-statistical and non-thermal**.

The final formal result is:

> A non-associative retained-information recombination process builds a non-metric, RG-stable, amplitude-interfering information geometry with an intrinsic pruning-sourced dissipative-statistical retained-order arrow. The structure is non-thermal under the tested entropy-production laws and non-unitary under the tested amplitude dynamics.

---

## 2. Minimal primitives

The model is best understood from three primitive ingredients.

### Primitive 1 — Retained information state

The state is not a point in pre-existing spacetime. It is a retained configuration of information / support / amplitude structure. The model’s geometry is induced from this retained structure rather than imposed externally.

### Primitive 2 — Ordered recombination

The native recombination operation is order-sensitive. The core local update has the schematic form:

```text
T(dx) = dx + g · (roll(dx) ⊙ q − dx ⊙ roll(q))
```

where `q` is the local retained state, `dx` is a local variation, `g` is coupling strength, `roll` encodes ordered neighbor structure, and `⊙` is elementwise interaction.

The critical feature is that recombination is noncommutative and non-associative. The result depends on ordering and grouping.

### Primitive 3 — Pruning / non-invertible retention

The model’s forward process is not invertible. Retained structure is carried forward through pruning/recoverability ordering, not through reversible physical time evolution. The directionality arises from retained-order loss / non-invertible retention, not from a primitive time coordinate.

---

## 3. Derived structures

### 3.1 Local metric

The native recombination kernel induces a local metric candidate from its own linearized structure. The metric is not imposed as an external quadratic form.

Established properties:

- Positive-definite / Riemannian locally.
- Nontrivial and anisotropic in the tested sectors.
- Supports local distances.
- Satisfies local metric tests such as triangle inequality.

Formal status:

> Local metric geometry is established.

### 3.2 Direct global metric gluing

The local metrics do not directly glue into a single global metric manifold under the tested atlas transitions.

Established result:

- Local metrics exist.
- Direct overlap gluing fails relative to matched nulls.
- Native transport is not metric-compatible.

Formal status:

> Direct global metric manifold structure is not established and fails under the tested direct-gluing route.

This does not mean no global behavior exists. Later coarse-graining tests show global/effective behavior exists, but it remains non-metric.

### 3.3 Native connection and non-metricity

The model has two relevant connections:

1. The Levi-Civita connection of the induced metric, which is metric-compatible by construction.
2. The native recombination transport connection, which is not metric-compatible.

The defect is non-metricity:

```text
Q_native = ∇^native g
```

or equivalently a connection defect:

```text
C = Γ_native − Γ_LC
```

Established properties:

- Non-metricity vanishes at `g = 0`.
- Associative controls remove the effect.
- Non-metricity scales approximately linearly with small coupling `g`.
- Non-metricity is the leading geometric effect.

Formal status:

> The primary native geometric object is non-metricity, not curvature.

### 3.4 Shear-dominated non-metricity

The non-metricity decomposes into trace/Weyl-like and traceless/shear-like components.

Established result:

- Traceless/shear component dominates by norm, roughly 3:1 over the Weyl/trace component.
- The shear dominance is stable across tested coupling strengths.

Formal status:

> The native geometry is not merely Weyl-like dilation geometry. It is shear-dominated metric-affine geometry.

### 3.5 Local scalar curvature

The induced local metric has positive scalar curvature.

Established properties:

- Scalar curvature is h-stable under finite-difference verification.
- Flat control gives zero.
- Sphere control verifies the curvature machinery.
- Curvature vanishes at `g = 0`.
- Associative control remains flat.
- Curvature scales approximately as `g²` in the small-coupling regime, with higher-order behavior at stronger coupling.

Formal status:

> Positive local scalar curvature is real and sourced by non-associative recombination, but it is secondary to non-metricity.

The causal hierarchy is:

```text
non-associative recombination
→ shear-dominated non-metricity, Q ~ g
→ positive local scalar curvature, R ~ g²
```

### 3.6 RG-stable metric-affine fixed point

Direct global metric gluing fails, but effective coarse-graining was tested separately.

Two routes were audited:

1. Independent block averaging.
2. Coupled RG-like coarse-graining through native transport.

Established result:

- Non-metricity does not cancel under independent averaging.
- Under coupled RG coarse-graining, the magnitude of `Q` remains approximately fixed across scale.
- The shear/Weyl decomposition shape also remains stable across scale.

Formal status:

> The effective large-scale object is not a metric-compatible sector under the tested routes. It is an RG-stable non-metric / metric-affine fixed point.

### 3.7 Amplitude-like history interference

Alternative recombination histories between matched endpoints partially cancel.

Established properties:

- Cancellation vanishes at `g = 0`.
- Cancellation vanishes in associative controls.
- Cancellation grows monotonically with coupling.
- At the operating coupling it is weak but structure-specific; at stronger coupling it becomes substantial.

Formal status:

> The model exhibits amplitude-like destructive interference among recombination histories.

Claim boundary:

This is not Hilbert-space quantum mechanics. It shows signed/vector cancellation among histories, not complex phase, Born weights, or unitary evolution.

### 3.8 Non-unitary amplitude dynamics

Unitary tests failed.

Established result:

- Native transport does not conserve norm.
- The generator is not skew-dominated; symmetric/stretching components are significant.
- Skew/unitary approximation leaves substantial residual error.
- No Born rule is established.

Formal status:

> The model has amplitude-like interference, but not unitary quantum-mechanical amplitude dynamics.

### 3.9 Pruning-sourced retained-order arrow

The non-unitarity is tied to pruning/non-invertibility.

Established properties:

- Forward/reverse reconstruction asymmetry exists.
- Closed loops drift under native pruning transport.
- Invertible/un-pruned controls remove the non-unitary drift.
- Ensemble-average directionality is strong.
- Individual trajectories fluctuate substantially.

V1719 resolved the arrow classification:

- No strict scalar Lyapunov function was found.
- The arrow is ensemble/cumulative rather than per-step monotone.
- Best per-trajectory monotonicity candidate was weak.

Formal status:

> The retained-order arrow is real, pruning-sourced, irreversible, and dissipative-statistical, but not a strict scalar Lyapunov law.

### 3.10 Thermodynamic-law audit

The thermodynamic-law arc tested whether the retained-order arrow obeys a state-defined entropy-production law.

Pre-registered candidates:

- Support entropy.
- Participation entropy.
- Reconstruction entropy.

Established result:

- Entropy drift collapses in the invertible master null.
- Entropy drift vanishes at `g = 0`.
- Native entropy drift scales with coupling.
- But entropy production is not sign-definite per step.
- Associative controls produce stronger and opposite-signed entropy change.

Formal status:

> T1 closed-negative. The arrow is irreversible and dissipative-statistical, but non-thermal under the tested state-defined entropy-production laws.

Because T1 failed, Crooks/Jarzynski and effective-temperature tests were not licensed under the pre-registration.

---

## 4. Layer ledger

| Layer | Object | Status | Meaning |
|---|---|---:|---|
| Algebra | noncommutative / non-associative recombination | established | order and grouping matter |
| Metric | local metric | established | local distance exists |
| Global gluing | direct global metric | failed under tested route | no direct metric manifold |
| Connection | native transport | established non-metric | transport changes metric |
| Non-metricity | shear-dominated Q | established | shape distortion dominates dilation |
| Curvature | positive scalar curvature | established | secondary local curvature |
| Scale | coupled RG | established | non-metricity fixed in magnitude and shape |
| Histories | destructive recombination interference | established | amplitude-like, not merely path dependence |
| Quantum ceiling | unitary dynamics | failed | no Hilbert/unitary claim |
| Ordered direction | pruning-sourced arrow | established | statistical/dissipative retained-order direction |
| Lyapunov ceiling | strict scalar monotone | failed | no deterministic Lyapunov law |
| Thermodynamic ceiling | entropy-production law | failed | arrow is non-thermal under tested entropies |

---

## 5. Control ledger

The major controls and what they established:

| Control | Role | Result |
|---|---|---|
| `g = 0` | flat / no coupling limit | geometry, curvature, interference, and entropy drift collapse appropriately |
| associative kernel | removes non-associative source | curvature and interference collapse; entropy drift does not, killing thermodynamic interpretation |
| invertible / un-pruned transport | master null for pruning irreversibility | non-unitarity, loop drift, entropy drift collapse |
| flat control | curvature floor | zero curvature |
| sphere control | curvature sanity check | known positive curvature recovered |
| matched nulls | prevent random structure from passing | separated real structure from generic path/transport effects |
| shuffled-history null | destroys order structure | used to identify history/order dependence |
| coupled RG control | tests coarse-graining | non-metricity survives as fixed point |

---

## 6. What is established

The model establishes the following simulation-internal architecture:

```text
retained information
→ non-associative ordered recombination
→ local metric geometry
→ shear-dominated non-metricity
→ positive secondary scalar curvature
→ RG-stable metric-affine fixed point
→ amplitude-like destructive history interference
→ non-unitary pruning-sourced dynamics
→ dissipative-statistical retained-order arrow
→ non-thermal irreversibility under tested entropy laws
```

The short version:

> The Retained Bridge builds a scale-stable, shear-type, non-metric information geometry with amplitude-like interference and a pruning-sourced non-thermal arrow.

---

## 7. What is not claimed

The following are not claimed:

1. **Not GR.**  
   The model does not currently derive Einstein equations, ADM closure, or a metric-compatible spacetime manifold.

2. **Not closed against all future GR-like sectors.**  
   The model does not support a direct GR-like closure under the tested routes. A future effective-sector projection would require a separate derivation and audit.

3. **Not unitary quantum mechanics.**  
   The model exhibits amplitude-like interference, but not norm-preserving unitary evolution, complex phase structure, Hilbert-space dynamics, or a Born rule.

4. **Not thermodynamics in the full sense.**  
   The retained-order arrow is irreversible, but no state-defined entropy-production law was found under the pre-registered candidates.

5. **Not physical time as primitive.**  
   The directionality is retained-order / pruning-sourced. Physical time, if relevant, would need to emerge as an interpretation or effective projection.

6. **Not a universal theorem yet.**  
   The results are simulation-internal and finite-sector, tied to the tested kernel, dimensions, and controls.

---

## 8. Minimal formal statement

Let `R` denote retained information states and let `T_g` be a non-associative ordered recombination transport with pruning/non-invertible retention. Then, in the tested sectors:

1. The linearization of `T_g` induces a local metric `g_R`.
2. The native connection `Γ_native` is not the Levi-Civita connection of `g_R`.
3. The non-metricity `Q = ∇^native g_R` is nonzero for `g > 0`, vanishes at `g = 0`, and is shear-dominated.
4. The scalar curvature of `g_R` is positive and second-order in coupling relative to `Q`.
5. Under coupled coarse-graining, `Q` remains stable in magnitude and shear/Weyl composition.
6. Recombination histories exhibit destructive cancellation, but the transport is non-unitary.
7. The non-unitarity is pruning-sourced and produces a dissipative-statistical retained-order arrow.
8. No strict Lyapunov scalar or state-defined entropy-production law was found under the pre-registered candidates.

---

## 9. Preferred vocabulary

Use:

- retained-order direction
- pruning-sourced arrow
- ordered recombination
- recoverability ordering
- non-metric information geometry
- shear-dominated metric-affine geometry
- amplitude-like history interference
- non-unitary dissipative dynamics
- non-thermal irreversibility

Avoid:

- physical time as primitive
- spacetime as primitive
- GR derivation
- quantum gravity claim
- thermodynamic law claim
- Born rule / Hilbert-space claim
- strict Lyapunov claim

---

## 10. Final frozen claim

> A non-associative retained-information recombination process builds a local metric geometry whose native connection is shear-dominated and non-metric. This non-metricity is the primary geometric effect, remains stable under coarse-graining, and produces secondary positive curvature. Alternative recombination histories exhibit amplitude-like destructive interference, but the dynamics are non-unitary because transport is forward-pruning and non-invertible. The resulting retained-order arrow is real, irreversible, and dissipative-statistical, but not governed by a strict scalar Lyapunov function or a state-defined thermodynamic entropy-production law under the tested candidates. The model therefore identifies a non-metric, RG-stable, amplitude-interfering information geometry with non-thermal pruning irreversibility.

---

## 11. Recommended next phase

No new simulation arc should begin until the above architecture is preserved in a durable package with:

1. This formal core memo.
2. A reproduction README.
3. Script ledger by rung / audit.
4. Claim-boundary summary.
5. Reviewer-facing table of controls and falsification gates.

After that, any future arc should begin deliberately with a fresh pre-registration. Candidate arcs:

1. Effective-sector projection: Can a metric-compatible Einstein-like sector be extracted as a projection from the non-metric base?
2. Algebraic formalization: Can the recombination law be written as a theorem over a non-associative algebra with induced metric-affine structure?
3. Empirical analogy / substrate comparison: Do similar retained-order non-metric signatures appear in real information-processing systems?

The current result should be considered frozen until a specific reviewer objection, new primitive derivation, or fresh pre-registered arc reopens it.
