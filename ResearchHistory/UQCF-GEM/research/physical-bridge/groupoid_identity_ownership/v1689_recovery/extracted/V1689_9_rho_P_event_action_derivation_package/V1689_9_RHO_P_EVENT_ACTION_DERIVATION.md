# V1689.9 — Deriving `ρ_P` from Provenance Event Action on `G_p`

**Verdict:** `RHO_P_EVENT_ACTION_DERIVATION_FROZEN_NO_EXECUTION`

## Why this step is necessary

V1689.8 showed that arbitrary maps:

```text
ρ_P : provenance/source current → End_alg(G_i)
```

leave high residual:

```text
E_Γ = D_ΓR_Γ − ρ_P(J_P)
```

and introduce scale mismatch.

So `ρ_P` cannot be chosen as a convenient embedding.

It must be derived from the way provenance/source events act on the generated retained algebra.

---

## 1. Local algebra

At a retained sector:

```text
G_p = ⟨B_p, O3_p, H4⊥_p, S_p, Π_p, ⊕_p⟩
```

A provenance event:

```text
e ∈ Π_p
```

acts on the local algebra:

```text
A_e : G_p → G'_p
```

The representation map is the linearized endomorphism induced by this event action:

```text
ρ_e = dA_e|_{G_p}
```

The boundary current representation is:

```text
ρ_P(J_P,ij)
=
Σ_{e ∈ Events(B_ij)}
σ(e) · magnitude(e) · ρ_e
```

where:

```text
σ(e)
```

is the retained-order/source orientation of the event crossing the boundary.

---

## 2. Event actions

### Source injection/removal

A source event modifies the source-supported branch/source subspace.

```text
ρ_source(e) = ± P_S(e)
```

where `P_S(e)` is a projector onto the source-affected subspace.

Positive for injection, negative for removal.

---

### Branch birth/prune

A branch birth adds a retained generator:

```text
ρ_birth(e) = + P_B(k)
```

A branch prune suppresses/removes one:

```text
ρ_prune(e) = − P_B(k)
```

where:

```text
P_B(k) = b_k b_k^T / (||b_k||^2 + ε)
```

---

### Dependency addition/break

A dependency event acts on a branch pair or provenance-supported incidence relation.

For branches `b_a`, `b_b`:

```text
I_dep(a,b)
=
(b_a − b_b)(b_a − b_b)^T
/
(||b_a − b_b||^2 + ε)
```

Then:

```text
ρ_dep_add(e)   = + I_dep(a,b)
ρ_dep_break(e) = − I_dep(a,b)
```

---

### Repair / closure event

A repair event acts on the defect subspace it repairs.

Allowed subspaces:

```text
product defect subspace
O3 associator defect subspace
H4⊥ residual defect subspace
```

Examples:

```text
ρ_repair_product(e) = + P_product_defect(e)
ρ_repair_O3(e)      = + P_O3
ρ_repair_H4(e)      = + P_H4
```

where:

```text
P_O3 = O3 O3^T / (||O3||^2 + ε)
P_H4 = H4⊥ H4⊥^T / (||H4⊥||^2 + ε)
```

Critical rule:

```text
These projectors must be constructed before E_Γ is computed.
```

They may not be fitted from the residual.

---

### Order-boundary crossing

An order event carries retained-order orientation.

```text
ρ_order(e)
=
σ_order(e) · I_order(e)
```

where `σ_order(e)` is determined by the pruning-order direction.

If the event reverses retained order, it contributes a violation rather than a valid current.

---

### Provenance relabel

A relabel event acts as a provenance-label permutation/conjugation on the labeled subspace.

```text
ρ_label(e) = + P_label
```

if lineage is conserved.

If lineage breaks:

```text
ρ_label(e) = − P_label
```

or the current becomes inadmissible, depending on the rule.

---

## 3. Full current representation

The represented source/provenance current is:

```text
ρ_P(J_P,ij)
=
Σ_e σ(e) magnitude(e) ρ_e
```

Component form:

```text
ρ_P(J_P)
=
ρ_source(J_source)
+
ρ_dependency(J_dependency)
+
ρ_repair(J_repair)
+
ρ_order(J_order)
+
ρ_label(J_label)
```

This object lives in:

```text
End_alg(G_i)
```

so it can be compared to:

```text
D_Γ R_Γ
```

---

## 4. Normalization

`ρ_P` must be normalized by the boundary algebra scale:

```text
||G_i||_alg
=
||B_i|| + ||O3_i|| + ||H4⊥_i|| + ||S_i|| + ε
```

not by:

```text
E_Γ
D_ΓR_Γ
fitted target performance
```

The normalization must be known before the identity residual is computed.

---

## 5. Forbidden dependencies

`ρ_P` may not use:

```text
R_Γ
D_ΓR_Γ
E_Γ
weak_target
scalar holonomy
fitted coefficients
post-hoc residuals
```

This is the firewall against construction recovery.

---

## 6. New required table: `event_actions.csv`

Future execution must emit:

```text
event_id
comparison_id
boundary_id
node_id
event_type
event_orientation
event_magnitude
affected_subspace_id
rho_e_serialized
rho_e_norm
rho_e_source
rho_uses_forbidden_fields
```

Then `source_currents.csv` must aggregate:

```text
ρ_P(J_P,ij)
=
Σ_e σ(e) magnitude(e) ρ_e
```

---

## 7. Killer nulls for `ρ_P`

### `N_event_action_shuffle`

Preserve event counts and magnitudes but assign events to wrong affected algebra subspaces.

Expected:

```text
same event statistics
wrong ρ_P
E_Γ fails
```

### `N_order_reverse`

Reverse event orientation.

Expected:

```text
same event counts
opposite source/order current
E_Γ fails or current inadmissible
```

### `N_projector_shuffle`

Preserve projector norms but shuffle branch/O3/H4 target subspaces.

Expected:

```text
same ρ_e norms
wrong algebra action
E_Γ fails
```

### `N_current_zero`

Set:

```text
ρ_P(J_P) = 0
```

in active-source regimes.

Expected:

```text
source-free closure fails when source-balanced closure is needed
```

---

## 8. Final identity

The law candidate is:

```text
D_Γ R_Γ = ρ_P(J_P)
```

with residual:

```text
E_Γ = D_Γ R_Γ − ρ_P(J_P)
```

But this identity cannot be tested until:

```text
Γ_R is admissible
R_Γ is admissible
D_ΓR_Γ is admissible
ρ_P is emitted from event actions
null pipelines regenerate event-action maps upstream
```

---

## Final statement

`ρ_P` is not a tunable bridge.

It is the event-action representation of provenance/source/pruning-order current on the generated retained algebra.

This is the required bridge from ledger current to curvature compatibility.
