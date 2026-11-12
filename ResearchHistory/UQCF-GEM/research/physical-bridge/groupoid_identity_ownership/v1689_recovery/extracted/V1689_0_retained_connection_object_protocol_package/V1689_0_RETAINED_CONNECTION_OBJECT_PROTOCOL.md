# V1689.0 — Retained Connection Object Protocol

**Verdict:** `DERIVATION_PROTOCOL_FROZEN_NO_REGRESSION_TARGET`

## Core reset

The next branch does not ask:

```text
Can a cycle-flow predictor fit a target?
```

It asks:

```text
What object does Γ_R naturally define,
what identity must that object satisfy,
and what observable follows before regression?
```

The missing bridge is not a better scalar holonomy. It is the correct retained curvature object of a generated-algebra connection, plus a source-balanced compatibility identity.

---

## 1. Local generated retained algebra

At each retained sector `p`, define:

```text
G_p = ⟨B_p, O3_p, H4⊥_p, S_p, Π_p, ⊕_p⟩
```

where:

```text
B_p      = retained branch generators
O3_p     = third-order associator obstruction
H4⊥_p    = fourth-order residual outside span(B_p, O3_p)
S_p      = source/access/divergence state
Π_p      = provenance/pruning-order ledger
⊕_p      = native retained recombination product
```

The local object is therefore not a coordinate patch and not a vector space alone. It is a generated retained recombination algebra with provenance order.

The product may be represented abstractly as:

```text
x ⊕_p y
```

or, in one concrete native-kernel form:

```text
x ⊕ y = x + y + γ_xy K(x,y)
K(x,y) = roll(x) ⊙ y − x ⊙ roll(y)
```

The associator is:

```text
A3_p(x,y,z)
=
(x ⊕_p y) ⊕_p z − x ⊕_p (y ⊕_p z)
```

The L4 object is the retained four-way residual component not contained in the span of branches and L3 associators:

```text
H4⊥_p ∉ span(B_p, O3_p)
```

---

## 2. Admissible retained transport

A retained connection edge is:

```text
T_pq : G_p → G_q
```

It is admissible only if it is generated-algebra faithful.

Required conditions:

```text
T_pq(B_p) ≈ B_q
```

```text
T_pq(x ⊕_p y) ≈ T_pq(x) ⊕_q T_pq(y)
```

```text
T_pq(O3_p) ≈ O3_q
```

```text
T_pq(H4⊥_p) ≈ H4⊥_q
```

```text
T_pq(Π_p) respects pruning-order dependencies in Π_q
```

Equivalently:

```text
A_Γ =
A_branch
∧ A_product
∧ A_O3
∧ A_H4
∧ A_source/provenance
∧ A_order-arrow
```

A branch-only map is not a retained connection if it destroys the product, associator, H4 residual, or provenance order.

This permanently downgrades:

```text
Kabsch / Procrustes / Gramian alignment
```

to diagnostics only. They cannot drive Γ_R.

---

## 3. Curvature object

For a loop:

```text
C = (p0 → p1 → ... → pn → p0)
```

define loop transport:

```text
Ω_C,p0 =
T_pn,p0 ∘ ... ∘ T_p1,p2 ∘ T_p0,p1
```

Then retained curvature is:

```text
R_Γ(C)_p0 = Ω_C,p0 − Id_Gp0
```

This is not primarily a scalar. It is a basepoint-normalized endomorphism defect:

```text
R_Γ(C)_p0 ∈ End(G_p0)
```

Because generated-algebra frames may change, the invariant object is the admissible conjugacy class:

```text
[R_Γ(C)_p0] ∈ End_alg(G_p0) / Aut_alg(G_p0)
```

where `Aut_alg(G_p0)` means admissible automorphisms preserving the generated retained algebra, not arbitrary vector-space rotations.

Scalar holonomy is therefore only a diagnostic projection of the richer object.

---

## 4. Covariant comparison

Curvatures at neighboring loops live in different endomorphism spaces:

```text
R_i ∈ End(G_i)
R_j ∈ End(G_j)
```

So raw subtraction is invalid.

Define a retained comparison map:

```text
Comp_{j→i}(R_j)
```

If local transport is invertible enough:

```text
Comp_{j→i}(R_j) = T_ji R_j T_ij
```

If transport is directed/non-invertible, use an admissible directed comparison:

```text
Comp_{j→i}(R_j)
=
Π_i ∘ T_{j→i} ∘ R_j ∘ T_{i→j}^{admissible}
```

Then the discrete retained covariant derivative is:

```text
(D_Γ R_Γ)_{ij}
=
Comp_{j→i}(R_j) − R_i
```

---

## 5. Source-balanced compatibility

The source-free identity is not primary.

A retained recombination system has provenance/source/pruning-order current. Therefore the first candidate identity is:

```text
D_Γ R_Γ = J_P
```

where:

```text
J_P = provenance/source/pruning-order current
```

Define the residual:

```text
E_Γ = D_Γ R_Γ − J_P
```

The compatibility test is:

```text
E_Γ ≈ 0
```

The source-free case is only a special case:

```text
if J_P = 0, then D_Γ R_Γ = 0
```

This is the correct physics analogue: curvature balance is source-balanced before it is source-free.

---

## 6. Proof obligation

### Proposition

If `T_pq` is not generated-algebra faithful, then `R_Γ(C)_p` is not an invariant retained curvature object.

### Proof sketch

Let:

```text
G_p = (V_p, ⊕_p)
G_q = (V_q, ⊕_q)
```

Suppose `T_pq : V_p → V_q` preserves branch vectors but not the product. Then there exist `x,y ∈ G_p` such that:

```text
T_pq(x ⊕_p y)
≠
T_pq(x) ⊕_q T_pq(y)
```

Define the product transport defect:

```text
δ_pq(x,y)
=
T_pq(x ⊕_p y)
−
[T_pq(x) ⊕_q T_pq(y)]
```

If `δ_pq ≠ 0`, then associator transport generically fails:

```text
T_pq A3_p(x,y,z)
≠
A3_q(T_pq x, T_pq y, T_pq z)
```

Because `H4⊥` is defined relative to lower branch/O3 span, H4 transport is also contaminated.

Therefore loop transport:

```text
Ω_C − Id
```

contains a mixture of:

```text
true retained curvature
+ product transport error
+ associator mismatch
+ H4 frame artifact
```

So it is not an invariant curvature object of the retained recombination system.

Thus any compatibility test using non-generated-algebra-faithful transport is mathematically premature.

QED.

---

## 7. Killer null suite

The primary falsifier is:

```text
N_alg_shuffle
```

It preserves surface statistics:

```text
source/access/divergence marginals
O3 norm distribution
H4 norm distribution
cycle length distribution
local graph degree distribution
cycle defect histogram
```

but breaks:

```text
product alignment
O3 transport alignment
H4⊥ transport alignment
provenance/pruning-order alignment
```

Expected result:

```text
valid Γ_R:
  ||D_Γ R_Γ − J_P|| small / structured / convergent

N_alg_shuffle:
  same surface statistics
  same apparent cycle magnitudes
  but ||D_Γ R_Γ − J_P|| fails
```

If `N_alg_shuffle` passes, the identity is not a retained connection law.

---

## 8. Frozen governance

```text
dashboard metrics = visualization only
generic scalar holonomy = diagnostic only
toy weak_target = banned as law evidence
construction recovery ≠ law discovery
target/predictor provenance separation mandatory
generated-algebra faithfulness mandatory
source-balanced closure before source-free closure
no regression rescue without a first-principles identity
```

---

## 9. Next execution conditions

Python is not admissible until an emitter can produce:

```text
G_p generated algebra objects
T_pq retained transports
product faithfulness defects
O3 transport faithfulness defects
H4⊥ transport faithfulness defects
Ω_C,p loop endomorphisms
R_Γ(C)_p curvature endomorphism defects
J_P provenance/source currents
E_Γ = D_Γ R_Γ − J_P
N_alg_shuffle nulls
```

Only then can V1689 become an execution branch.

---

## Final statement

The next scientific object is not a scalar target.

It is:

```text
Γ_R as a generated-algebra connection
```

and the next law candidate is not a regression equation.

It is:

```text
D_Γ R_Γ = J_P
```

with generated-algebra faithfulness as the admissibility condition and `N_alg_shuffle` as the killer null.
