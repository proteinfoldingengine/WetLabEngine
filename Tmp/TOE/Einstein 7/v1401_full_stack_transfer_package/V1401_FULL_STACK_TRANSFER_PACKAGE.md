# V1401 — Full-Stack Transfer Package for Next AI

## Purpose

Transfer the current UQCF-GEM / Recoverability / It-from-Bit bridge work to another AI.

The immediate task is **not** to continue the optimizer spoof-defense rabbit hole. The immediate task is to move back up the GR-facing value chain:

```text
bit / source distinction
→ retained admissible path
→ identity + closure
→ local momentum / continuity propagation
→ local constraint propagation
→ H-like scalar branch
→ ADM-like bridge
```

Latest result, V1400:

```text
identity + closure strongly preserves local M-like / continuity propagation,
but does not yet recover H-like scalar constraint behavior.
```

So the next bottleneck is:

```text
Why does the local momentum / continuity branch work,
while the H-like scalar curvature/source branch remains flat?
```

---

## 1. Claim Boundaries

Allowed language:

```text
ADM-like
constraint-like
local momentum-like propagation
continuity-like propagation
curvature-like proxy
ordered recoverability slices
synthetic transport simulations
model-native evidence
```

Do **not** claim:

```text
physical GR
Einstein equations
physical spacetime curvature
full ADM derivation
actual spacetime
physical time evolution
```

The update index is not physical time. Use:

```text
ordered recoverability slices
ordered updates
retained-order propagation
```

---

## 2. Current Scientific State

### Branch A — B-like / source-flow closure

Frozen and externally reviewed.

Supported chain:

```text
path-certified admissibility
→ closure pressure
→ retained source-flow coherence
→ B-like closure propagation
```

### Branch B — identity + closure minimal sufficiency

The stack:

```text
identity + closure
```

was shown to be minimally sufficient under synthetic adversaries for rejecting identity-matched counterfeits, preserving B-like closure, and preserving ADM_M-like propagation.

But V1313 optimizer spoofing showed:

```text
identity + closure is winner-stable, but not weight-stable.
```

V1315 showed local/windowed closure helps, but does not fully solve spoofing.

### Decision

Stop spoof-defense for now.

Use the lesson:

```text
global constraints are insufficient;
local constraint propagation matters.
```

Return to GR-facing bridge.

---

## 3. Latest Result — V1400

V1400 asked:

```text
Does retained identity + closure produce local ADM-like constraint propagation across ordered recoverability slices?
```

Result:

```text
identity + closure:
    valid_winner_rate = 1.000
    valid_weight      ≈ 1.000
    M residual        ≈ 0.0187
    continuity        ≈ 0.4257
```

Compared with closure-only:

```text
closure-only:
    valid_winner_rate = 0.000
    valid_weight      ≈ 0.0109
    M residual        ≈ 1.3402
    continuity        ≈ 1.0882
```

Interpretation:

```text
identity + closure strongly preserves local momentum/continuity propagation.
```

But:

```text
H-like residual stayed near ~1.02.
```

So V1400 supports the **local M-like / continuity bridge**, but **not** full local H/M ADM-like closure.

---

## 4. Mathematical Stack

Let:

```text
k = ordered recoverability slice index
x = spatial lattice coordinate
```

Each candidate history is:

```text
H_i = {ρ_i(k,x), J_i(k,x), S_i(k,x), F_i(k,x), R_i(k,x), Ω_i(k,x)}
```

where:

```text
ρ  = retained accessibility density
J  = accessibility current
S  = source field
F  = flow field
R  = response field
Ω  = conformal-like accessibility response
```

### Accessibility/source relation

```text
S(k,x) = z(log ρ(k,x))
```

### Continuity-like primitive

```text
C(k,x) = z(ρ(k+1,x) - ρ(k,x)) + z(∂x J(k,x))
```

Local score:

```text
C_local(k,w) = RMS_{x∈w}[C(k,x)]
```

### Native flow / M-like residual

```text
J_native(k,x) = -∂x log ρ(k,x)
M(k,x) = z(J_native(k,x)) - z(F(k,x))
M_local(k,w) = RMS_{x∈w}[M(k,x)]
```

This is the branch V1400 supports.

### B-like closure

Global closure:

```text
R(k,x) ≈ a0 + a1 S(k,x) + a2 F(k,x)
B(k) = RMS[R(k,x) - (a0 + a1S(k,x) + a2F(k,x))]
```

Local closure:

```text
B_local(k,w) = RMS_{x∈w}[R(k,x) - (a0_w + a1_w S(k,x) + a2_w F(k,x))]
```

### Identity residual

```text
I(H_i,H_ref) =
mean_k [
    1 - cos(ρ_i(k), ρ_ref(k))
  + 1 - cos(J_i(k), J_ref(k))
  + 1 - cos(S_i(k), S_ref(k))
]
```

Identity is not sufficient alone. Identity-matched response spoofs pass identity but break closure.

### Candidate energy and retained weight

```text
U_i =
    w_I I_i
  + w_B B_i
  + w_M M_i
  + w_path P_i
  + w_repair Rpair_i
  + w_access Aloss_i
```

Retained weight:

```text
W_i = exp(-β U_i) / Σ_j exp(-β U_j)
```

Current best GR-facing stack:

```text
identity + closure
```

not because it is perfect, but because it produces stable legitimate retention and downstream M-like propagation in the tested model.

### Conformal-like field / H-like branch

Current field:

```text
Ω(k,x) = exp[-0.35 S(k,x) + 0.12 F(k,x)]
K(k,x) = z(∂xx log Ω(k,x))
```

Current H-like residual:

```text
H(k,x) = z(K(k,x)) - z(0.65 S(k,x) + 0.35 R(k,x))
H_local(k,w) = RMS_{x∈w}[H(k,x)]
```

Problem:

```text
H_local does not improve under identity + closure.
```

This is the next bottleneck.

---

## 5. What the Other AI Must Do Next

Correct next version:

```text
V1401 — H-Branch Root Cause Audit
```

Core question:

```text
Why does identity + closure propagate local M/continuity,
but fail to improve local H-like scalar residual?
```

### Hypotheses

#### A — H residual is malformed

Test alternatives:

```text
H1 = z(K) - z(S)
H2 = z(K) - z(R)
H3 = z(K) - z(S + ∂xF)
H4 = z(K) - z(S + C)
H5 = z(K + α∂xF) - z(S + βR)
H6 = weak-form integral residual over windows
```

#### B — Ω is wrong

Current:

```text
Ω = exp[-0.35S + 0.12F]
```

Test:

```text
ψ = log ρ
Ωρ = exp(-ψ)
ΩS = exp(-S)
Ωmix = exp[-aS + bF + cR]
```

Do not fit to labels.

#### C — H requires local closure

Test regimes:

```text
identity + closure
identity + local closure
identity + closure + local closure
identity + closure + momentum
```

#### D — H is downstream of M propagation

Rerun:

```text
identity + closure
identity + closure + momentum
```

and test whether momentum stabilizes scalar behavior.

---

## 6. Required V1401 Outputs

Generate:

```text
v1401_h_branch_root_cause.py
V1401_H_BRANCH_ROOT_CAUSE_REPORT.md
v1401_summary.json
v1401_summary_by_H_definition.csv
v1401_summary_by_regime.csv
v1401_local_window_HM_constraints.csv
v1401_artifacts.zip
```

### Required tables

Table 1: H definitions.

Rows:

```text
H_current
H_source_only
H_response_only
H_source_divflow
H_weak_form
H_rho_based_omega
```

Columns:

```text
mean_H_residual
mean_local_H_residual
mean_M_residual
mean_continuity_residual
valid_weight
```

Table 2: regimes.

Rows:

```text
weak_control
identity_only
closure_only
identity_plus_closure
identity_plus_local_closure
identity_plus_closure_momentum
identity_closure_local_momentum
```

Columns:

```text
valid_winner_rate
valid_weight
mean_H
mean_M
mean_continuity
mean_alignment
```

### Pass/fail criteria

M bridge passes if:

```text
M residual improves vs weak_control and closure_only
continuity improves vs weak_control and closure_only
```

H bridge passes if:

```text
H residual improves vs weak_control, identity_only, closure_only
improvement persists locally across windows
```

---

## 7. V1401 Claim Rules

If M improves but H does not:

```text
identity + closure supports local M-like / continuity propagation,
but H-like scalar closure remains unresolved.
```

If a new H definition improves:

```text
a candidate scalar/H-like residual becomes downstream of retained identity + closure
under [specific H definition].
```

If only fitted coefficients make H improve:

```text
Do not claim H closure. Call it a fitted diagnostic.
```

If local closure is required:

```text
H-like scalar propagation requires local/windowed closure, not global closure alone.
```

---

## 8. Suggested V1401 Python Shape

```python
H_DEFS = {
    "H_current": lambda s: z(s["curvature"]) - z(0.65*s["source"] + 0.35*s["response"]),
    "H_source_only": lambda s: z(s["curvature"]) - z(s["source"]),
    "H_response_only": lambda s: z(s["curvature"]) - z(s["response"]),
    "H_source_divflow": lambda s: z(s["curvature"]) - z(s["source"] + grad(s["flow"], s["x"])),
}
```

For each retained path:

```python
for H_name, H_fn in H_DEFS.items():
    compute local H residuals over windows
    compute M residual
    compute continuity residual
```

Then compare:

```python
ΔH = H_regime - H_weak_control
ΔM = M_regime - M_weak_control
```

Do not use target/native labels in H selection.

---

## 9. Scientific Interpretation to Preserve

Current best story:

```text
identity + closure
→ admissible retained path
→ local M-like continuity propagation
```

Not yet:

```text
identity + closure
→ full local H/M ADM-like closure
```

The H branch is unresolved and is the correct next scientific target.

---

## 10. Final Instruction

Do not chase optimizer spoofing further unless H-branch work depends on it.

Do not keep proving identity + closure again.

Do not overclaim GR.

Answer one question:

```text
What scalar/H-like residual, if any,
is naturally downstream of retained identity + closure
in the ordered recoverability model?
```

If none, say none.
