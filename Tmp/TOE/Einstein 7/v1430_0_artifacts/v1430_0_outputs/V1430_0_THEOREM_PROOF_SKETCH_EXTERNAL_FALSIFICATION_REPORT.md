# V1430.0 — Theorem / Proof Sketch + External Falsification Plan

## Status
Completed.

## Claim Boundary

Theorem/proof-sketch and external falsification plan only.

No physical GR, Einstein equations, full ADM derivation, physical spacetime, or physical curvature is claimed.

---

# Candidate Theorem

```text
Recoverability under pruning requires retained source-origin information.
```

Formal implication:

```text
E_R ≤ ε  ⇒  I_source > I_min
```

with:

```text
ε = 0.20
```

---

# Definitions

Let:

```text
G = (V, E)
```

be a finite carrier graph.

Let:

```text
S
```

be a finite source-origin alphabet.

Let:

```text
σ: V → S
```

be the hidden source-origin assignment.

Let:

```text
x₀
```

be the initial state.

Let:

```text
T
```

be a transformation.

Let:

```text
P
```

be a pruning/compression map.

Let:

```text
Y = P(T(x₀))
```

be the retained compressed observation.

Let:

```text
R(Y) = σ̂
```

be the reconstructed source assignment.

Define reconstruction error:

```text
E_R = (1 / |V|) Σ_v 1[σ̂(v) ≠ σ(v)]
```

Define retained source-origin information:

```text
I_source = I(Σ; Y)
```

Use the Fano-style threshold:

```text
I_min(ε, |S|) = H(Σ) - h(ε) - ε log(|S|-1)
```

where:

```text
h(ε) = -ε log ε - (1-ε) log(1-ε)
```

---

# Proof Sketch

1. If a reconstruction map recovers the source assignment with error no greater than ε, then the compressed observation must preserve distinctions among source classes.

2. Those distinctions are source-origin information in the information-theoretic sense:

```text
I(Σ; Y)
```

3. Fano-style reasoning gives a lower bound: low reconstruction error requires sufficient mutual information between source assignment and retained observation.

4. Therefore, if:

```text
E_R ≤ ε
```

then, under the estimator and finite-sample assumptions:

```text
I_source > I_min
```

5. The synthetic tests are not a universal proof. They are falsification attempts: try to produce successful reconstruction after source-origin information is removed.

---

# Simulation Support

The current synthetic hardening result:

```text
trials: 5,040
successful reconstructions: 708
falsifications: 0
positive source success rate: ≈ 0.983
source-destroyed success rate: 0.000
```

Interpretation:

```text
In this synthetic finite-graph harness,
successful reconstruction after pruning required retained source-origin information.
```

---

# What This Corrects

Earlier branches failed because they tried to close law through observables:

```text
transport
lineage
continuity
H-like summaries
geometry-like summaries
```

Those are not currently supported as primitive laws.

The stronger candidate is:

```text
retained source-origin information
```

Transport, lineage, continuity, H, and geometry may be mechanisms or diagnostics, but they are not the closed primitive.

---

# External Falsification Plan

The theorem candidate fails if any independent system demonstrates:

```text
E_R ≤ ε
```

while:

```text
I_source ≤ I_min
```

Specific falsifiers:

1. Successful source reconstruction after source-origin information is destroyed.
2. Reconstruction succeeds using only transport while source-origin information is absent.
3. Reconstruction succeeds using only continuity or geometry summaries while source-origin information is absent.
4. A different reconstruction operator succeeds with insufficient measured source-origin information.
5. A richer information estimator shows the current I_source threshold was miscalibrated.

---

# What Is Not Claimed

```text
universal mathematical proof
physical spacetime
GR
Einstein equations
full ADM
geometry as primitive
transport as primitive
lineage as primitive
continuity as primitive
```

---

# Safe Scientific Statement

```text
In synthetic finite-graph recoverability tests,
successful reconstruction after pruning required retained source-origin information
under the frozen theorem test.
```

---

# Recommended Next Step

Do not tune more simulations.

Next legitimate step:

```text
external replication / independent implementation
```

or:

```text
formal proof refinement using information-theoretic bounds
```
