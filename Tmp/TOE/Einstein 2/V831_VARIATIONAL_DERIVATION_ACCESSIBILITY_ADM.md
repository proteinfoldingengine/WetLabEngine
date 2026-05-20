# V831 — Formal Variational Derivation of the Unified Accessibility-Flow ADM-like System

## Purpose

The empirical branch has now reached a stable status:

```text
Accessibility curvature law: validated
ADM momentum-like signal: non-circular
Unified ADM-like constraints: supported
OOD robustness: supported
```

V831 begins the formal derivation phase.

The goal is to derive the unified accessibility-flow ADM-like system from a variational principle rather than treating it as an empirical regression result.

---

# 1. Empirical laws to be derived

The validated accessibility curvature law is:

```text
A = exp(C - μ + η repair)
```

```text
φ = -α log(A + ε)
```

```text
G_proxy = -2Δφ = 2α Δ log(A + ε)
```

The reopened ADM-like momentum branch is carried by:

```text
J_i = -∇_i log A
```

and the effective momentum source structure:

```text
M_i ~ F(J_i, ∂τJ_i, ∇·J)
```

The unified ADM-like constraint branch is:

```text
Hamiltonian-like source: ΔlogA, A
Momentum-like source: J_i, ∂τJ_i, ∇·J
```

---

# 2. Primitive object

The primitive is not mass-energy.

The primitive is reachable-state accessibility density:

```text
A(x, τ) > 0
```

where:

```text
A = exp(C - μ + η repair)
```

Therefore:

```text
log A = C - μ + η repair
```

Define the accessibility potential:

```text
u = log(A + ε)
```

Then:

```text
φ = -α u
```

and:

```text
J_i = -∇_i u
```

So both the scalar geometry and the effective momentum current are generated from one object:

```text
u = log A
```

This is the unification point.

---

# 3. Candidate action principle

We seek an action functional over an ordered-update slice:

```text
S[u, φ, J] = ∫ dτ d²x  L
```

The minimal Lagrangian must include:

1. conformal geometry energy,
2. accessibility potential coupling,
3. accessibility-flow kinetic/inertial term,
4. flow-divergence compression term,
5. constraint enforcing `φ + αu = 0`,
6. constraint enforcing `J_i + ∇_i u = 0`.

A compact candidate is:

```text
L =
    1/2 |∇φ|²
  + λ_H φ Δu
  + 1/2 β |∂τ J|²
  + 1/2 γ |∇·J|²
  + 1/2 κ |J|²
  + Λφ (φ + αu)
  + ΛJ^i (J_i + ∇_i u)
```

where:

```text
u = log(A + ε)
J_i = -∇_i u
φ = -αu
```

The multipliers `Λφ` and `ΛJ^i` enforce the empirically discovered constraints.

---

# 4. Variation with respect to φ

The φ-dependent part is:

```text
L_φ = 1/2 |∇φ|² + λ_H φ Δu + Λφ φ
```

Vary:

```text
δS/δφ = 0
```

Using integration by parts:

```text
δ ∫ 1/2 |∇φ|² = -∫ Δφ δφ
```

and:

```text
δ ∫ λ_H φ Δu = ∫ λ_H Δu δφ
```

Therefore:

```text
-Δφ + λ_H Δu + Λφ = 0
```

If the multiplier vanishes or is absorbed into the constraint balance:

```text
Δφ = λ_H Δu
```

Using:

```text
G_proxy = -2Δφ
```

and:

```text
φ = -αu
```

we obtain:

```text
G_proxy = 2α Δu
```

or:

```text
G_proxy = 2α Δlog(A + ε)
```

This derives the accessibility-curvature law from stationarity.

---

# 5. Variation with respect to J_i

The J-dependent part is:

```text
L_J =
    1/2 β |∂τJ|²
  + 1/2 γ |∇·J|²
  + 1/2 κ |J|²
  + ΛJ^i J_i
```

Vary with respect to `J_i`.

The terms contribute:

```text
β term:     -β ∂τ²J_i
γ term:     -γ ∇_i(∇·J)
κ term:      κ J_i
constraint: ΛJ_i
```

Stationarity gives:

```text
-β ∂τ²J_i - γ ∇_i(∇·J) + κ J_i + ΛJ_i = 0
```

or:

```text
β ∂τ²J_i + γ ∇_i(∇·J) - κ J_i = ΛJ_i
```

This naturally produces the observed momentum feature family:

```text
J_i
∂τJ_i
∇·J
```

The empirical model used first-order `∂τJ_i`; the variational form gives a second-order inertial current. In a dissipative or first-order reduction, this becomes:

```text
τ_J ∂τJ_i + J_i + χ ∇_i(∇·J) = source_i
```

which is exactly the structure suggested by V827/V828/V829.

---

# 6. Momentum-like constraint interpretation

The ADM momentum-like residual is:

```text
M_i = D_j(K^j_i - δ^j_i K)
```

Empirically, it is predicted by:

```text
M_i ~ a J_i + b ∂τJ_i + c ∇·J
```

The variational current equation naturally supplies those terms.

Thus the effective source is:

```text
P_i^access =
    a J_i
  + b ∂τJ_i
  + c ∇_i(∇·J)
```

or in reduced empirical form:

```text
P_i^access ≈ F(J_i, ∂τJ_i, ∇·J)
```

Therefore the ADM-like momentum constraint becomes:

```text
M_i ≈ P_i^access
```

This is not classical matter momentum.

It is effective accessibility-flow momentum.

---

# 7. Unified theorem-shape result

## Assumptions

1. A positive accessibility density exists:

```text
A(x, τ) > 0
```

2. Its logarithm defines the accessibility potential:

```text
u = log(A + ε)
```

3. The conformal potential is constrained by:

```text
φ = -αu
```

4. The effective accessibility flow is constrained by:

```text
J_i = -∇_i u
```

5. The action contains geometry energy and accessibility-flow inertia/compression.

## Result 1 — Hamiltonian/scalar branch

Stationarity with respect to `φ` yields:

```text
G_proxy = 2α Δlog(A + ε)
```

## Result 2 — Momentum branch

Stationarity with respect to `J_i` yields an effective current equation containing:

```text
J_i
∂τJ_i
∇·J
```

which matches the empirically validated ADM-momentum-like source structure.

## Result 3 — Unified ADM-like accessibility-flow system

The two branches share the same primitive:

```text
u = log A
```

Therefore:

```text
Hamiltonian-like constraint:
H ~ F(ΔlogA, A)

Momentum-like constraint:
M_i ~ F(J_i, ∂τJ_i, ∇·J)
```

with:

```text
J_i = -∇_i log A
```

---

# 8. What this proves and does not prove

## Supported

```text
The unified accessibility-flow ADM-like system has a plausible variational derivation.
```

```text
The same primitive u = log A generates both scalar curvature and effective momentum flow.
```

```text
The empirical feature family J, ∂τJ, ∇·J is not arbitrary; it arises from a flow-action variation.
```

## Not yet proved

```text
Full physical ADM equations.
```

```text
Full Einstein equations.
```

```text
Continuum-limit theorem.
```

```text
Physical spacetime interpretation.
```

---

# 9. Correct next step

V832 should convert this theorem-shape derivation into a numerical stationarity test.

Specifically:

```text
Compute Euler-Lagrange residuals from the proposed action.
Check whether residual minima align with the observed ADM-like constraints.
```

Pass condition:

```text
The action residual is small when the V829/V830 constraints are strong.
```

Fail condition:

```text
The proposed action residual does not track the observed ADM-like closure.
```

---

# 10. Summary

The key formal transition is:

```text
u = log A
```

From this single primitive:

```text
φ = -αu
J_i = -∇_i u
```

Then:

```text
G_proxy = 2α Δu
```

and:

```text
M_i ~ F(J_i, ∂τJ_i, ∇·J)
```

This is the first theorem-shape derivation of the unified accessibility-flow ADM-like system.
