
# V812 — Accessibility Curvature Law

## Purpose

V811 changed the interpretation:

```text
Recoverability geometry may encode reachable-state accessibility,
not local conserved transport.
```

V812 derives the curvature law under that interpretation.

---

# First principle

A system under pruning/repair pressure does not primarily need to conserve local momentum.

It needs to preserve access to viable future states.

So the primitive object is:

```text
A(x, τ) = reachable-state density
```

not:

```text
J_i = local transported momentum current
```

---

# Accessibility field

Define an accessibility density:

```text
A(x, τ)
```

where high A means:

```text
many viable recovery futures remain reachable
```

and low A means:

```text
future recovery options are collapsing
```

The recoverability geometry should respond to this accessibility field.

---

# Conformal factor

The natural conformal relation becomes:

```text
Ω = F(A)
```

A minimal logarithmic form is:

```text
φ = log Ω = -α log(A + ε)
```

Interpretation:

```text
as accessibility decreases, curvature/warping increases
```

This matches the observed scalar branch:

```text
φ responds to defect / repair / surplus pressure
```

---

# Curvature law

The scalar/conformal curvature object was:

```text
G_proxy = -2Δφ
```

Substitute:

```text
φ = -α log(A + ε)
```

Then:

```text
G_proxy = 2α Δ log(A + ε)
```

So the accessibility curvature law is:

```text
curvature ∝ Laplacian of log reachable-state density
```

This is the cleanest first-principles expression discovered so far.

---

# Meaning

The model is not saying:

```text
matter momentum curves spacetime
```

It is saying:

```text
collapse of accessible recovery futures generates curvature-like geometry
```

That exactly fits the recoverability framework.

---

# Why Hamiltonian closes

The ADM Hamiltonian constraint is scalar.

It measures density/curvature balance.

Accessibility is scalar.

Therefore Hamiltonian closure is natural:

```text
curvature density ↔ accessibility density
```

---

# Why momentum fails

ADM momentum requires:

```text
local conserved vector transport
```

But accessibility geometry does not require local conserved transport.

The system can change reachable future states globally or nonlocally.

So momentum failure is not necessarily a defect.

It may be telling us:

```text
this is accessibility geometry, not fluid-momentum geometry
```

---

# Correct replacement for momentum

Instead of asking:

```text
D_j(K^j_i - δ^j_i K) = J_i
```

we should ask:

```text
how does accessibility redistribute?
```

The relevant equation is closer to:

```text
∂τ A = repair_gain - defect_loss + accessibility_diffusion + nonlocal_recovery
```

Then geometry follows:

```text
φ = -α log(A + ε)
```

and curvature follows:

```text
G_proxy = -2Δφ
```

---

# The new core law

```text
Accessible-state collapse generates conformal curvature.
```

Mathematically:

```text
φ = -α log(A + ε)
G_proxy = 2α Δ log(A + ε)
R_conf = exp(-2φ)G_proxy
```

---

# Interpretation of prior results

## Strong scalar/conformal closure

Expected.

Accessibility is scalar.

## Strong Hamiltonian closure

Expected.

Hamiltonian is scalar curvature/density balance.

## Weak momentum closure

Expected.

Momentum assumes local vector transport.

## Observable transport partial signal

Expected.

Visible transport is a projection of accessibility reorganization.

## Conservation failure

Expected.

Accessibility can change through creation/loss of future options, not just conserved movement.

---

# New research target

The next object is not:

```text
T_ab full tensor stress
```

The next object is:

```text
A(x, τ)
```

and its evolution law.

---

# V813 target

Test whether an explicit accessibility field A predicts the already observed curvature field better than defect/repair/surplus terms alone.

Pass condition:

```text
G_proxy ≈ 2α Δ log(A + ε)
```

with strong held-out transfer.

Fail condition:

```text
A does not improve curvature closure beyond existing source law.
```
