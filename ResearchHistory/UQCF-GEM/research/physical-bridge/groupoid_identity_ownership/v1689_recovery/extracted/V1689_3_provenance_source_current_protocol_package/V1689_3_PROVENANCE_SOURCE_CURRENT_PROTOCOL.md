# V1689.3 — Provenance / Source Current `J_P` Protocol

**Verdict:** `PROVENANCE_SOURCE_CURRENT_PROTOCOL_FROZEN_NO_EXECUTION`

V1689.2 defined:

```text
(D_Γ R_Γ)_{ij}
```

as the retained covariant comparison of curvature objects across neighboring retained loops/cells.

V1689.3 defines the right-hand side:

```text
J_P,ij
```

the provenance/source/pruning-order current across the same boundary.

---

## 1. Core rule

`J_P` is not a fitted residual.

It is not:

```text
weak_target
scalar holonomy
post-hoc correction term
E_Γ after the fact
```

It is a ledger-derived current emitted independently from curvature.

The identity is:

```text
D_Γ R_Γ = J_P
```

with residual:

```text
E_Γ = D_Γ R_Γ − J_P
```

The source-free identity:

```text
D_Γ R_Γ = 0
```

is only the special case:

```text
J_P = 0
```

---

## 2. Same-boundary rule

Let:

```text
B_ij
```

be the retained comparison boundary used to compute:

```text
(D_Γ R_Γ)_{ij}
```

Then `J_P,ij` must be computed over exactly that same boundary:

```text
J_P,ij = J_P(B_ij)
```

This prevents another construction-recovery loop.

Forbidden:

```text
compute curvature over one boundary
compute source current over another boundary
compare them anyway
```

---

## 3. Allowed ledger events

`J_P` may use only provenance/source/order events such as:

```text
source_injection
source_removal
branch_birth
branch_prune
dependency_addition
dependency_break
repair_event
closure_event
provenance_relabel
order_boundary_crossing
```

Each event must carry:

```text
event_id
ordered_index
event_type
node_id
source_label
magnitude
dependencies
prior_event_ids
valid_order_arrow
boundary_id
```

Forbidden inputs:

```text
R_Γ
D_Γ R_Γ
E_Γ
weak_target
scalar_holonomy
posthoc_fit_residual
```

---

## 4. Component currents

Define:

```text
J_P,ij
=
J_source,ij
+
J_dependency,ij
+
J_repair,ij
+
J_order,ij
+
J_label,ij
```

### Source current

```text
J_source,ij
=
signed_sum(source_injection − source_removal across B_ij)
```

### Dependency current

```text
J_dependency,ij
=
signed_sum(dependency_addition − dependency_break across B_ij)
```

### Repair current

```text
J_repair,ij
=
signed_sum(repair_event − unresolved_break across B_ij)
```

### Order current

```text
J_order,ij
=
signed_sum(order_boundary_crossing)
−
order_arrow_violations
```

### Label current

```text
J_label,ij
=
signed_sum(provenance_relabel with conserved lineage)
−
lineage_breaks
```

Each component must be reported separately.

A small aggregate `J_P` cannot hide a failed component or order violation.

---

## 5. Representation problem

`D_Γ R_Γ` is endomorphism-valued:

```text
(D_Γ R_Γ)_{ij} ∈ End_alg(G_i)
```

So `J_P` must be represented in the same comparison space.

Define a representation map:

```text
ρ_P : provenance/source current → End_alg(G_i)
```

Then the identity is really:

```text
D_Γ R_Γ = ρ_P(J_P)
```

or, by notation convention:

```text
D_Γ R_Γ = J_P
```

where `J_P` already means the represented current.

Critical rule:

```text
ρ_P may use ledger event structure only.
ρ_P may not use R_Γ, D_Γ R_Γ, E_Γ, weak_target, or fitted residuals.
```

---

## 6. Current admissibility

Define:

```text
J_boundary_pass
```

all events used in `J_P` share the boundary of the comparison.

```text
J_order_pass
```

retained-order arrows are valid, or violations are explicitly counted.

```text
J_independence_pass
```

forbidden fields are absent.

```text
J_conservation_pass
```

event accounting balances internally before curvature comparison.

Then:

```text
J_P_admissible
=
J_boundary_pass
∧
J_order_pass
∧
J_independence_pass
∧
J_conservation_pass
```

If `J_P_admissible` fails, the identity cannot be promoted.

---

## 7. Output schema

### `provenance_events.csv`

```text
event_id
ordered_index
event_type
node_id
source_label
magnitude
dependencies
prior_event_ids
valid_order_arrow
boundary_id
```

### `source_currents.csv`

```text
comparison_id
boundary_id
J_source
J_dependency
J_repair
J_order
J_label
J_P_serialized
rho_P_map_id
J_P_norm
J_boundary_pass
J_order_pass
J_independence_pass
J_conservation_pass
J_P_admissible
```

### `current_manifest.json`

```text
forbidden_fields_absent
rho_P_definition
event_accounting_rule
boundary_alignment_rule
claim_boundary
```

---

## 8. Killer current nulls

### `N_source_shuffle`

Preserve event counts and magnitudes but shuffle boundary assignments.

Expected:

```text
same source statistics
wrong boundary current
E_Γ fails
```

### `N_order_reverse`

Preserve events but reverse retained-order dependencies.

Expected:

```text
same event counts
J_order fails
E_Γ fails or J_P inadmissible
```

### `N_label_shuffle`

Preserve provenance-label counts but break lineage continuity.

Expected:

```text
same labels
broken provenance current
E_Γ fails
```

### `N_current_zero`

Force:

```text
J_P = 0
```

in active-source regimes.

Expected:

```text
source-balanced identity passes
source-free identity fails
```

---

## 9. Frozen nonclaims

```text
J_P is not a target fitted after seeing curvature.
J_P is not weak_target.
J_P is not scalar holonomy.
J_P cannot be computed from E_Γ.
Source-free closure cannot be tested before source-balanced closure.
```

---

## Final statement

V1689.3 freezes `J_P` as a ledger-derived provenance/source/pruning-order current over the same comparison boundary as `D_Γ R_Γ`.

The identity is:

```text
D_Γ R_Γ = J_P
```

but only after:

```text
Γ_R admissibility passes
R_Γ admissibility passes
comparison admissibility passes
J_P admissibility passes
```

This prevents the right-hand side from becoming another constructed target.
