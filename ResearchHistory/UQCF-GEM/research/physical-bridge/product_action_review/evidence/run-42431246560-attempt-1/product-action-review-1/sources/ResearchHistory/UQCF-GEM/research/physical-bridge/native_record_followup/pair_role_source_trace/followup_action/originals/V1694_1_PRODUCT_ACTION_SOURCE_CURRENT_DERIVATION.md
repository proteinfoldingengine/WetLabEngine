# V1694.1 — Product-Action Source Current Derivation

**Verdict:** `PRODUCT_ACTION_CURRENT_DERIVED_NO_EXECUTION`

## Purpose

V1693.2 showed that the product derivative probe is meaningful, but the source-balanced product identity failed.

The failed current was:

```text
ρ_P^oplus = Σ Φ_⊕(E_event)
```

That formula is no longer admissible as evidence.

V1694.1 derives the only acceptable replacement:

```text
ρ_var^oplus
```

from variation of the product action itself.

---

## 1. Product action

Define:

```text
I_⊕[A]
=
Σ_edges Σ_(x,y)∈T_p
ω_xy ||δ_⊕[A_e](x,y)||_B²
```

where:

```text
δ_⊕[A](x,y)
=
T_A(x⊕_p y)
−
(T_Ax⊕_q T_Ay)
```

This action measures whether retained recombination products are transported faithfully.

---

## 2. Variation split

The variation must split as:

```text
δI_⊕
=
interior stationarity
+
boundary trace
+
source remainder
```

The boundary term is:

```text
Q_⊕ = Tr_boundary(Grad_⊕)
```

The source/current term is the remaining support variation:

```text
J_⊕
=
δ_support I_⊕
−
Q_support
```

So the corrected current is:

```text
ρ_var^⊕
=
SourceRemainder_⊕
```

This is fundamentally different from assigning current by event labels or event projectors.

---

## 3. What can generate source current?

The allowed source variations are:

```text
variation of retained pair set T_p
variation of pair weights ω_xy
variation of native product kernel ⊕_p
variation of S changing pair admissibility
variation of Π changing pair orientation/admissibility
```

Each must induce a covector in:

```text
V_⊕*
```

---

## 4. Correct identity candidate

The revised identity is:

```text
D_ΓR_Γ^⊕
=
ρ_var^⊕
+
Q_A^⊕
```

where:

```text
ρ_var^⊕
```

is derived from product-action support variation.

---

## 5. Source-free special case

If support variation vanishes:

```text
δ_support I_⊕ = 0
```

and the pair ledger is frozen:

```text
T_p, ω_xy, S, Π inactive
```

then the source-free special case is:

```text
D_ΓR_Γ^⊕
=
Q_A^⊕
```

This can only be tested after a support audit confirms source inactivity.

---

## 6. Forbidden shortcuts

Do not use:

```text
event-label-only current
Σ Φ_⊕(E_event) without variation support
rho scaling fit after residuals
source current inserted as correction term
```

---

## Next

```text
V1694.2 — Product Source-Variation Current Python Test
```
