# V1689.16 — Common-Generator Sub-Branch Postmortem

**Verdict:** `STRUCTURE_CORRECT_COMPATIBILITY_NOT_ESTABLISHED`

## Bottom line

V1689 succeeded structurally but did not establish compatibility.

The branch correctly moved from:

```text
regression target fitting
```

to:

```text
retained connection identity testing
```

But the clean-room generator still did not satisfy the source-balanced compatibility identity.

## What worked

```text
G_p = generated retained recombination algebra
T_pq = generated-algebra transport
R_Γ = basepoint-normalized endomorphism defect
D_ΓR_Γ = covariant curvature comparison
J_P = provenance/source/pruning-order current
ρ_P = event-action representation
A_pq = common generator upstream of both T_pq and ρ_e
```

This is the correct object stack.

## What failed

V1689.15 emitted:

```text
A_pq first
T_pq = Exp_R(A_pq)
ρ_e = P_event A_pq P_event
```

but the result was still:

```text
mean cosine(D_ΓR_Γ, ρ_P(J_P)) ≈ -0.213
mean E_relative_norm ≈ 0.796
```

So compatibility was not established.

## Root cause

The clean-room `A_pq` was structurally valid but not first-principles selected.

It was built from local differences:

```text
ΔB, ΔS, ΔO3, ΔH4, ΔΠ, Δproduct
```

That is enough to emit a schema, but not enough to produce a lawful connection.

The missing object is:

```text
the selection principle for A_pq
```

A retained connection is not just any algebra-faithful map. It must be the native admissible update selected by the retained recombination principle.

## Mathematical gap

The next question is:

```text
What variational or admissibility principle selects A_pq?
```

Candidate:

```text
A_pq minimizes generated-algebra faithfulness action
subject to provenance/source/order current constraints.
```

A first candidate action is:

```text
I_Γ[A]
=
||δ_⊕||²
+
||δ_O3||²
+
||δ_H4||²
+
||δ_S||²
+
||δ_Π||²
+
λ ||source/order constraint||²
```

The goal is not to fit a target.

The goal is to derive whether stationarity gives:

```text
D_Γ R_Γ = ρ_P(J_P)
```

as the compatibility identity.

## What to keep

```text
G_p generated algebra definition
A_Γ faithfulness gates
R_Γ endomorphism defect
D_ΓR_Γ covariant comparison
J_P ledger current
ρ_P event-action representation
boundary mass/algebra scale normalization
upstream full-pipeline nulls
A_pq as common generator
```

## What to downgrade

```text
clean-room A_pq = scaffold only
standalone event projectors = diagnostic only
schema success = methodological success only
```

## Frozen stop rule

Do not continue modifying clean-room `A_pq` heuristically.

No new generator term is admissible unless it is derived from the variational/admissibility principle.

## Next branch

```text
V1690 — Retained Connection Variational Principle
```

The task is not another emitter tweak.

The task is:

```text
derive A_pq from first principles
```

Required deliverables:

```text
1. define admissibility action I_Γ[A]
2. define source/provenance/order constraints
3. derive stationarity condition
4. show whether D_ΓR_Γ = ρ_P(J_P) follows
5. only then run a new emitter
```

## Safe claim

V1689 established the correct retained connection object stack and showed that compatibility requires a principled generator `A_pq`, not target fitting or arbitrary clean-room transport construction.
