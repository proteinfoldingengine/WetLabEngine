# V1694.4 — Exact Product Support-Boundary Decomposition

**Verdict:** `PRODUCT_SUPPORT_BOUNDARY_DECOMPOSITION_DERIVED_NO_EXECUTION`

## Purpose

V1694.3 showed that the product channel has robust structure, but the identity is still blocked by incomplete separation between:

```text
Q_A^oplus
ρ_var^oplus
```

So V1694.4 derives the exact decomposition:

```text
δI_⊕
=
interior
+
boundary
+
support-current
```

---

## 1. Product action

Define:

```text
I_⊕[A,T,w,⊕]
=
Σ_e Σ_a w_{e,a} <δ_{e,a},δ_{e,a}>_B
```

where `a` indexes retained pairs:

```text
(x_a,y_a) ∈ T_e
```

and:

```text
δ_{e,a}
=
T_A(x_a⊕_p y_a)
−
(T_Ax_a⊕_qT_Ay_a)
```

---

## 2. Total variation

The exact split is:

```text
δI_⊕
=
δ_A I_⊕
+
δ_support I_⊕
```

where:

```text
δ_A I_⊕ = interior_A + boundary_A
```

and:

```text
δ_support I_⊕
=
δ_T I
+
δ_w I
+
δ_kernel I
+
δ_orientation I
```

The product identity is only meaningful if these pieces are disjoint.

---

## 3. Boundary term

The boundary term is:

```text
Q_A^⊕(∂C)
=
Σ_{e∈∂C}
σ(C,e) τ_e→C^⊕(Grad_A I_⊕,e)
```

Allowed dependence:

```text
connection variation only
```

Forbidden inside `Q_A`:

```text
pair weight variation
pair set birth/death variation
source/support variation
post-hoc residual correction
```

---

## 4. Support current

The support current is:

```text
ρ_support^⊕
=
δ_T I
+
δ_w I
+
δ_kernel I
+
δ_orientation I
```

It lives in:

```text
V_⊕*
```

after mapping support variations back to retained-pair dual covectors.

### Weight variation

```text
δ_w I
=
Σ_a (δw_a)<δ_a,δ_a>
```

### Pair set variation

```text
δ_T I
```

captures pair birth/death/replacement and must use signed pair-incidence orientation.

### Product-kernel variation

```text
δ_kernel I
```

comes from variation of the native product law `⊕`.

### Orientation variation

```text
δ_orientation I
```

comes from `Π`-driven retained-pair orientation changes.

---

## 5. Disjointness rule

```text
ρ_support may not include Grad_A I_⊕ terms.
Q_A may not include support variations.
```

This prevents double-counting or correction leakage.

---

## 6. Required audits

```text
boundary_support_disjointness
support_current_disjointness
overlap_norm <Q_A, rho_support>
zero_support_gate
zero_boundary_gate
```

The overlap may be reported, but not optimized.

---

## 7. Required nulls

```text
N_Q_support_contamination
N_rho_boundary_contamination
N_weight_label_only
N_pair_birth_unsigned
N_source_free_false
```

---

## Next

```text
V1694.5 — Product Support-Boundary Decomposition Python Test
```
