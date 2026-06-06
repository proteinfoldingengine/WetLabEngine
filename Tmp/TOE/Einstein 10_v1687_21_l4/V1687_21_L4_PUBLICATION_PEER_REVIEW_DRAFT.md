# L4 as Irreducible Fourth-Order Hyper-Associator Information in Retained Recombination Systems

**Manuscript ID:** V1687.21-L4-PUBLICATION-DRAFT  
**Framework:** Retained Bridge / Recoverability Geometry  
**Status:** Peer-review draft  
**Claim level:** bounded finite-sector / natural-admissibility support; not a universal theorem or empirical physics claim  
**Keywords:** retained recombination, associator, hyper-associator, non-associativity, higher-order information, operator-faithfulness, natural admissibility, rank-lift, obstruction, ε4-floor

---

## Abstract

We report a bounded symbolic and computational investigation of the layer following L3 in a retained recombination framework. Earlier L3 work identified an irreducible third-order associator obstruction \(O_{123}\) that could not be reduced to the span of the original retained branch currents. The present work asks whether four-branch recombination reduces to branches plus all L3 associators, or whether it introduces a new fourth-order information layer. For retained branches \(J_1,J_2,J_3,J_4\), with recombination operator \(\oplus\), we define the fourth-order bracketing residual

\[
H_4
=
(((J_1\oplus J_2)\oplus J_3)\oplus J_4)
-
(J_1\oplus(J_2\oplus(J_3\oplus J_4))).
\]

The lower-order comparison space is

\[
\operatorname{span}\{J_1,J_2,J_3,J_4,O_{123},O_{124},O_{134},O_{234}\},
\]

where \(O_{ijk}\) are L3 triple associators. Across random-sector hardening, targeted finite-sector certificates, and a finite symbolic-sector family sweep, \(H_4\) was found to contribute an independent rank direction beyond branches plus all L3 associators. A targeted nonzero \(9\times9\) minor certificate produced a nonzero exact rational determinant, and an 8-sector symbolic family sweep certified \(8/8\) sectors with \( \operatorname{rank}[B_4,O_3]=8\), \( \operatorname{rank}[B_4,O_3,H_4]=9\), and \( \operatorname{rank\_lift}_{H4}=1\).

An adversarial non-diagonal projection was later found that erased \(H_4\) while passing a weak admissibility proxy. Auditing showed that this projection was constructed from the \(H_4\) residual itself, failed generated-algebra faithfulness, and was post-hoc obstruction-targeting. This led to a corrected admissibility class, \(A_{op}^{nd,\natural}(L4)\), requiring naturality and generated-algebra operator-faithfulness. Under this strengthened class, no natural admissible \(H_4\)-erasing projection was found in the finite-sector search.

The strongest bounded conclusion is that, inside the tested retained recombination operator family, finite symbolic support/order sectors exist in which \(H_4\) contributes an independent fourth-order retained direction beyond branches plus all L3 associators. This supports the interpretation of L4 as irreducible fourth-order hyper-associator information. Universal theorem closure and empirical validation remain open.

---

## 1. Introduction

The Retained Bridge / Recoverability Geometry program studies how structure may arise from retained information, ordered recombination, and admissible projection. Previous L3 work found that three-branch retained recombination can contain irreducible information not captured by pairwise branch geometry. The central L3 obstruction was:

\[
O_{123}
=
(J_1\oplus J_2)\oplus J_3
-
J_1\oplus(J_2\oplus J_3).
\]

The L3 result reclassified the residual \( \varepsilon_{\mathrm{floor}} \) as a lower-bound route from irreducible third-order retained associator information.

The present work asks what follows L3. There were two possibilities:

```text
Option A:
L4 is law-closure over L3.
Four-branch residuals reduce to branches plus all L3 associators.

Option B:
L4 is a new obstruction layer.
Four-branch recombination produces information not reducible to branches plus all L3 associators.
```

The result of the V1687 branch supports Option B in bounded finite sectors:

\[
H_4\notin \operatorname{span}(B_4\cup O_3).
\]

This report describes the full discovery path, including the important adversarial counterprojection that exposed a weakness in the first admissibility definition and led to the stronger natural admissibility class.

---

## 2. Definitions

### 2.1 Retained branch currents

Let \(V\) be a finite-dimensional retained-current vector space. Let:

\[
J_1,J_2,J_3,J_4\in V
\]

be four retained branch currents.

Each branch represents a retained source/order/provenance-support structure. The ordered index used in simulations is a retained-order or pruning-order index, not a primitive physical time parameter.

### 2.2 Retained recombination operator

Let:

\[
\oplus: V\times V\to V
\]

be a retained recombination operator.

The tested operator family has the form:

\[
x\oplus y=x+y+\gamma_{xy}K(x,y),
\]

where \(K(x,y)\) is a nonlinear retained-overlap kernel. In the symbolic and numerical tests, a representative kernel was:

\[
K(x,y)=\operatorname{roll}(x)y-x\operatorname{roll}(y).
\]

This operator is not claimed to be universal. It is the tested retained recombination class for this branch.

### 2.3 L3 associators

For each triple \(i,j,k\), define:

\[
O_{ijk}
=
(J_i\oplus J_j)\oplus J_k
-
J_i\oplus(J_j\oplus J_k).
\]

For four branches:

\[
O_3=\{O_{123},O_{124},O_{134},O_{234}\}.
\]

Define:

\[
B_4=\{J_1,J_2,J_3,J_4\}.
\]

### 2.4 L4 hyper-associator residual

Define the canonical fourth-order residual:

\[
H_4
=
(((J_1\oplus J_2)\oplus J_3)\oplus J_4)
-
(J_1\oplus(J_2\oplus(J_3\oplus J_4))).
\]

Other four-branch bracketing residuals may also be considered, but this manuscript focuses on the canonical left-right bracketing residual.

### 2.5 L4 rank-lift

Define:

\[
I_4
=
\operatorname{rank}[B_4,O_3,H_4]
-
\operatorname{rank}[B_4,O_3].
\]

L4 is certified in a finite sector when:

\[
I_4>0.
\]

In the certified sectors of this work:

\[
\operatorname{rank}[B_4,O_3]=8,
\]

\[
\operatorname{rank}[B_4,O_3,H_4]=9,
\]

so:

\[
I_4=1.
\]

---

## 3. Methods

### 3.1 Numerical random-sector hardening

Random sectors were generated by varying support masks, branch fields, and retained-overlap structure while preserving nondegenerate branch identities. Each sector was tested for:

```text
branch rank,
L3 associator rank,
four-branch bracketing dispersion,
single L4 residual rank-lift,
joint L4 residual rank-lift,
reducibility to branches plus all L3 associators.
```

Operator controls included:

```text
linear_associative_control
closure_only_control
symmetric_overlap_control
nonlinear_symmetric_control
antisym_no_order_control
full_gated_order_overlap
```

### 3.2 Symbolic/numeric finite-sector witness

A finite symbolic support/order sector was constructed with four branches embedded in a 12-dimensional retained-current space. Exact rational values were substituted into the symbolic construction to test whether:

\[
\operatorname{rank}[B_4,O_3,H_4]
>
\operatorname{rank}[B_4,O_3].
\]

### 3.3 Targeted nonzero-minor certificate

Given a successful exact rational witness, the evaluated \(12\times9\) matrix:

\[
[B_4,O_3,H_4]
\]

was searched for a nonzero \(9\times9\) determinant. A single nonzero evaluated determinant proves the corresponding symbolic minor is not identically zero.

### 3.4 Finite symbolic-sector family sweep

The finite-sector certificate was extended to a small family of symbolic support/order sectors. For each sector, the same rank and nonzero-minor tests were applied.

### 3.5 Projection-faithfulness and admissibility audit

The projection question was central:

```text
Can H4 be erased by an admissible projection?
```

The first admissibility proxy required branch preservation, L3 preservation, rank preservation, and pairwise operator-faithfulness. A broader non-diagonal search found a weak-proxy H4-erasing projection.

That counterprojection was audited for:

```text
pair faithfulness,
nested bracketing faithfulness,
generated-algebra faithfulness,
construction dependence on H4,
naturality.
```

This audit motivated the corrected class:

\[
A_{op}^{nd,\natural}(L4).
\]

---

## 4. Results

### 4.1 Random-sector hardening

In V1687.2, the target full-gated order-overlap operator produced:

```json
{
  "sectors": 24,
  "collapsed": 0,
  "l4_new": 24,
  "l4_law": 0,
  "unresolved": 0,
  "mean_l4_joint_lift": 4.0,
  "mean_single_l4_new_count": 4.0,
  "mean_l3_lift": 4.0,
  "mean_triple_NOOCI": 1.0,
  "l4_new_rate": 1.0
}
```

Thus:

```text
24 / 24 random sectors produced L4-new behavior.
```

The associative and closure-only controls collapsed as expected, showing that the harness was not automatically inventing L4.

### 4.2 Targeted finite-sector nonzero-minor certificate

V1687.5 produced:

```json
{
  "rank_base_8": 8,
  "rank_with_H4": 9,
  "rank_lift_H4": 1
}
```

The exact rational nonzero determinant was:

```text
256480337840586992720981 / 144703125
```

Therefore, in that finite symbolic sector:

\[
H_4\notin \operatorname{span}(B_4\cup O_3).
\]

### 4.3 Finite symbolic-sector family sweep

V1687.6 produced:

```json
{
  "sector_count": 8,
  "certified_count": 8,
  "certified_rate": 1.0,
  "rank_lift_min": 1,
  "rank_lift_mean": 1.0,
  "rank_lift_max": 1
}
```

Thus:

```text
8 / 8 finite symbolic support/order sectors certified L4 rank-lift.
```

### 4.4 Weak-proxy counterprojection

V1687.15 found a non-diagonal projection that erased \(H_4\) while passing the earlier weak admissibility proxy:

```json
{
  "base_rank_B4_O3": 8,
  "rank_with_H4": 8,
  "rank_lift_H4": 0,
  "H4_residual_to_B4_O3": 1.13e-9,
  "operator_faithfulness_gap_max": 6.29e-12,
  "operator_faithful": true,
  "admissible_Aopnd_proxy": true,
  "H4_erased": true
}
```

This was not treated as a nuisance. It was treated as an adversarial failure exposing a missing admissibility condition.

### 4.5 Audit of the counterprojection

V1687.16 showed that the H4-erasing projection had the form:

\[
P=I-uu^T,
\]

where:

\[
u=
\frac{\operatorname{residual}(H_4\mid \operatorname{span}(B_4+O_3))}
{\|\operatorname{residual}(H_4\mid \operatorname{span}(B_4+O_3))\|}.
\]

Thus the projection was constructed from the obstruction it erased.

The audit returned:

```text
H4_ERASURE_PROJECTION_INADMISSIBLE_POSTHOC
```

Key failure:

```json
{
  "generated_faithful": false,
  "construction_depends_on_H4": true,
  "construction_natural": false,
  "strict_admissible": false
}
```

Generated-algebra faithfulness failed sharply:

```json
{
  "generated_gap_max": 335274816.82744825,
  "generated_gap_mean": 8332377.074726313
}
```

### 4.6 Corrected natural admissibility

The corrected admissibility class is:

\[
A_{op}^{nd,\natural}(L4).
\]

It requires:

```text
linearity
branch noncollapse
branch rank preservation
L3 associator noncollapse
L3 rank preservation
normalization
retained provenance/order compatibility
generated-algebra operator-faithfulness
naturality / no obstruction targeting
```

The key additions are:

```text
generated-algebra operator-faithfulness
naturality / no obstruction targeting
```

### 4.7 Natural projection search

V1687.18 searched predefined natural projections and found:

```text
NO_NATURAL_ADMISSIBLE_H4_ERASURE_FOUND_EPS4_STRENGTHENED
```

Summary:

```json
{
  "projection_count": 31,
  "admissible_natural_count": 2,
  "admissible_natural_erasure_count": 0
}
```

Classification counts:

```json
{
  "NATURAL_BUT_INADMISSIBLE_H4_PERSISTS": 26,
  "NATURAL_BUT_INADMISSIBLE_H4_ERASURE": 3,
  "NATURAL_ADMISSIBLE_H4_PERSISTS": 2
}
```

Therefore:

```text
No natural, generated-algebra-faithful, admissible projection erased H4 in the finite-sector search.
```

---

## 5. Theorem Route

### 5.1 Rank-lift lemma

If:

\[
\operatorname{rank}[B_4,O_3,H_4]
>
\operatorname{rank}[B_4,O_3],
\]

then:

\[
H_4\notin\operatorname{span}(B_4\cup O_3).
\]

This follows immediately because appending a vector already in the span cannot increase rank.

### 5.2 Nonzero-minor lemma

If a \(9\times9\) minor of \([B_4,O_3,H_4]\) has a nonzero determinant polynomial, then there exists a nonempty algebraic-open subset of parameter space where:

\[
I_4=1.
\]

A nonzero evaluated determinant certifies the corresponding symbolic determinant is not identically zero.

### 5.3 Projection-faithfulness lemma

If \(\Pi\) is generated-algebra operator-faithful, then:

\[
\Pi(x\oplus y)=\Pi x\oplus \Pi y
\]

for all \(x,y\) in the retained recombination algebra generated by \(B_4\).

This prevents erasing \(H_4\) by changing the recombination law locally or post-hoc.

### 5.4 ε4 route

The desired theorem target is:

\[
\varepsilon_{4,\min}
=
\inf_{\Pi\in A_{op}^{nd,\natural}(L4)}\|\Pi H_4\|
>
0.
\]

The route requires:

```text
compactness of A_op^nd,natural(L4),
continuity of Π ↦ ||ΠH4||,
and noncollapse ΠH4 ≠ 0 for all admissible natural Π.
```

This is not yet universally proven.

---

## 6. Discussion

The L4 branch is significant because it shows that L3 is not the end of retained recombination irreducibility. L3 showed that three-way recombination can contain information not reducible to pairwise branch structure. L4 now shows that four-way recombination can contain information not reducible even to branches plus all three-way associators.

This suggests a possible higher-order hierarchy:

```text
L1 = retained identity
L2 = pairwise geometry-like closure
L3 = third-order associator obstruction
L4 = fourth-order hyper-associator obstruction
```

The deeper hypothesis is:

```text
Ln = irreducible n-branch retained recombination information.
```

However, this remains a hypothesis beyond L4.

The most important scientific feature of the L4 branch is not that every test passed. It did not. The weak-proxy counterprojection was a valuable failure. It revealed that admissibility must include naturality and generated-algebra faithfulness, not merely pairwise faithfulness and rank preservation. After that correction, L4 survived the stricter finite-sector natural-admissibility search.

---

## 7. Limitations

This work does not claim:

```text
universal L4 theorem
all projections searched
all operators certified
all support/order sectors certified
empirical L4
physical geometry
GR / ADM
L5 closure
complete infinite obstruction hierarchy
```

The result is bounded.

---

## 8. Falsification Checklist

The L4 route weakens if any of the following are found:

```text
1. a natural generated-algebra-faithful projection that erases H4;
2. a correct lower-order basis term missing from B4 + O3 that absorbs H4;
3. gate consistency constraints that collapse H4;
4. proof that the nonzero-minor sectors are inadmissible;
5. evidence that rank-lift is a sector artifact;
6. failure of compactness for A_op^nd,natural(L4);
7. a non-post-hoc operator-natural map with ΠH4 = 0.
```

---

## 9. Conclusion

The V1687 L4 branch supports a bounded but meaningful result:

\[
H_4\notin \operatorname{span}(B_4\cup O_3)
\]

in certified finite symbolic sectors.

A weak-proxy H4-erasing projection was found, but it was post-hoc, obstruction-targeting, and failed generated-algebra faithfulness. After strengthening admissibility to \(A_{op}^{nd,\natural}(L4)\), no natural admissible H4 erasure was found in the finite-sector search.

The best current interpretation is:

```text
L4 is irreducible fourth-order hyper-associator information,
with a strengthened ε4 route under natural admissibility.
```

Universal theorem closure remains open.

---

## Appendix A — Evidence Chain

```text
V1687.1  — First L4 discovery harness
V1687.2  — Random-sector hardening: 24/24 L4-new
V1687.3  — L4 interpretation checkpoint
V1687.4  — Symbolic/numeric witness
V1687.5  — Targeted nonzero 9×9 minor certificate
V1687.6  — Finite symbolic-sector family sweep: 8/8 certified
V1687.7  — L4 closure status transfer report
V1687.8  — L4 theorem-boundary memo
V1687.9  — Projection-faithfulness / ε4 route
V1687.10 — ε4-floor closure status
V1687.11 — Formal theorem skeleton
V1687.12 — A_op^nd definition
V1687.13 — H4 erasure search
V1687.14 — Strengthened closure memo
V1687.15 — Non-diagonal weak-proxy H4 erasure
V1687.16 — Counterprojection audit: inadmissible post-hoc
V1687.17 — A_op^nd,natural update
V1687.18 — Natural projection search
V1687.19 — Natural-admissibility closure memo
V1687.20 — Final bounded scientific report
```

---

## Appendix B — Glossary

**B4**  
The four retained branches \(J_1,J_2,J_3,J_4\).

**O3**  
The set of all L3 triple associators for four branches: \(O_{123},O_{124},O_{134},O_{234}\).

**H4**  
The fourth-order bracketing residual.

**Rank-lift**  
The rank increase obtained by appending a candidate obstruction to the lower-order basis.

**A_op^nd,natural(L4)**  
The corrected admissible projection class requiring nondegeneracy, operator-faithfulness on the generated algebra, and naturality.

**ε4 route**  
The route toward a lower-bound residual associated with irreducible fourth-order hyper-associator information.

---

## Appendix C — Claim Boundary

This manuscript reports bounded finite-sector and natural-admissibility support. It does not claim universal theorem closure, empirical validation, physical spacetime, GR, ADM, or an infinite obstruction hierarchy.
