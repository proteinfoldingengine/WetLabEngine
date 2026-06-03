# From Path-Certified Admissibility to B-like Source-Flow Closure: A Claim-Hardened Bridge Report

## Abstract

This report consolidates the V1152–V1208 research branch into a claim-hardened bridge result. The work began with a frozen admissibility law for information-to-geometry simulations and then tested whether previously observed curvature-like, flow-like, ADM-like, and B-like structures could be explained as downstream consequences of admissibility. The result is split. The B-like/source-flow closure branch is supported inside the current simulations: closure pressure increases valid retained weight, reduces B-like residuals, stabilizes residual propagation across ordered slices, and improves source-flow alignment. The full ADM-like H/M constraint branch remains unresolved. This report freezes the supported bridge and explicitly avoids forcing the ADM-like branch with weak patched terms.

---

## 1. Core Thesis

The supported thesis is:

```text
Path-certified admissibility produces stable B-like source-flow closure propagation.
```

The current work supports this chain:

```text
admissible history
→ closure pressure
→ retained source-flow coherence
→ stable B-like residual
→ ordered-slice source-flow propagation
```

The stronger chain remains unresolved:

```text
admissible history
→ curvature / flow
→ full ADM-like H/M constraint structure
```

---

## 2. Background

The earlier admissibility branch established that geometry-like final states are not enough. A candidate history had to preserve:

```text
1. normalized / buffered Ω compatibility
2. Genesis / source-origin provenance
3. source-flow closure envelope
4. causal transport path-signature envelope
```

This led to the frozen admissibility law:

```text
AdmissibleGeometry :=
BufferedNormalizedOmegaCompatibility
AND GenesisPin
AND SourceFlowClosureEnvelope
AND CausalTransportSignatureEnvelope
```

The question then moved up the value chain:

```text
Can this admissibility law explain why curvature-like, flow-like, ADM-like, and B-like structures appeared in earlier work?
```

---

## 3. V1200–V1204 Supported Branch

### V1200 — Unification Audit

V1200 tested whether primitive admissibility pressure could produce downstream structure. The result was partial. B-like closure and source-flow alignment tracked valid retained weight strongly, but ADM-like residuals did not.

Key signal:

```text
valid weight ↔ source-flow alignment: strong positive relationship
valid weight ↔ lower B-like residual: strong positive relationship
```

### V1201 — U_info Term Ablation

V1201 showed that closure imbalance was the dominant necessary term. Removing closure imbalance damaged the system sharply:

```text
valid retained weight decreased
valid winner rate decreased
flow coherence decreased
source-flow alignment decreased
B-like residual worsened
```

This established closure pressure as not merely decorative.

### V1202 — Native Closure-Driven Pruning

V1202 strengthened only the closure term identified by V1201. The best regime was around:

```text
closure_weight ≈ 1.5–2.0
```

This improved:

```text
valid retained weight
valid winner rate
B-like residual
source-flow alignment
```

without introducing a new diagnostic.

### V1203 — Constraint Propagation Test

V1203 tested ordered-slice propagation. B-like residuals propagated stably across slices. Source-flow alignment also tracked valid retained weight. ADM-like H/M residuals remained weak or mixed.

### V1204 — B-like Necessity Test

V1204 compared no-closure, baseline-closure, and strengthened-closure regimes. Strengthened closure produced:

```text
valid_weight:           +0.318 vs no closure
valid_winner_rate:      +0.281 vs no closure
B_like_residual:        -0.525 vs no closure
B_like_std:             -0.024 vs no closure
source_flow_alignment:  +0.444 vs no closure
flow_coherence:         +0.086 vs no closure
```

This is the strongest evidence for the supported bridge.

---

## 4. V1205–V1208 Claim Split

V1205 separated the result into two branches:

```text
Supported:
admissibility → B-like/source-flow closure propagation

Unresolved:
admissibility → full ADM-like H/M constraint structure
```

V1206 and V1207 tested candidate momentum primitives:

```text
flow divergence imbalance
current continuity imbalance
flux balance imbalance
accessibility displacement
response momentum
phase transport
```

None materially unlocked ADM_M without either negligible effect or damage to valid winner behavior.

V1208 therefore froze the supported result and recommended not forcing ADM_M.

---

## 5. Claim-Hardened Result

The supported claim is:

```text
Within the tested simulation framework, B-like/source-flow closure behaves as a necessary primitive pressure for retained admissible histories.
```

More explicitly:

```text
Closure pressure helps admissible histories dominate.
Closure pressure reduces B-like residuals.
Closure pressure stabilizes B-like residuals across ordered slices.
Closure pressure improves source-flow alignment.
Closure pressure improves flow coherence.
```

The unsupported or unresolved claim is:

```text
The same admissibility law fully recovers ADM-like H/M constraint structure.
```

That remains open.

---

## 6. Why This Matters

This result is valuable because it separates two concepts that were previously bundled:

```text
1. source-flow / B-like closure propagation
2. ADM-like H/M constraint recovery
```

The first now has internal support.

The second remains a future theory problem.

This makes the bridge cleaner and more scientifically usable.

---

## 7. GR-Facing Interpretation

The work does not need to claim physical GR to be valuable. The useful GR-facing insight is structural:

```text
GR-like consistency has geometry/source/conservation/constraint components.
The current framework has recovered a supported source-flow closure branch,
but not the full constraint structure.
```

So the honest bridge is:

```text
admissibility → B-like source-flow closure
```

not:

```text
admissibility → Einstein equations
```

The next GR-facing question should be:

```text
What native primitive would make momentum-like consistency inevitable,
rather than patched?
```

---

## 8. Recommended Next Work

There are two clean paths.

### Option A — External Review

Freeze this branch and ask for clean-room review of:

```text
V1152–V1161 admissibility law
V1200–V1208 supported B-like bridge
```

### Option B — Separate ADM_M-First Theory Branch

Start a new branch that asks:

```text
What primitive makes ADM_M native?
```

Do not continue patching weak momentum terms into the current branch.

---

## 9. Final Boundary

Supported:

```text
Path-certified admissibility produces stable B-like/source-flow closure propagation inside the tested simulations.
```

Unresolved:

```text
Full ADM-like H/M constraint recovery.
```

Not claimed:

```text
Physical spacetime, GR, Einstein equations, or physical curvature derivation.
```
