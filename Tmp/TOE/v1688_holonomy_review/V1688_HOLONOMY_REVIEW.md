# V1688 "Directed Native Holonomy" — Findings for Peer Review

**Object reviewed:** V1688 Holonomy Proof Visualizer V4 and its positioning paper.
**Question:** Is the reported "directed native holonomy" a loop-holonomy (a property of the
provenance cycle), or is it edge-level non-reciprocity wearing a holonomy name?
**Status:** finite-sector, deterministic. Every number below is produced by the companion
script `v1688_holonomy_proofs.py` (output captured in `v1688_holonomy_proofs_OUTPUT.txt`).

---

## Summary verdict

| Quantity in the paper | What it actually is |
|---|---|
| `native_directional_cycle_defect ≈ 0.54` | `mean(\|C_corr\|)` scaled by ≈1; **no cycle information** |
| `orientation_asymmetry ≈ 9e-5` (directed signal) | **provenance-independent** residual of non-reciprocal cosines |
| loop / path dependence (the holonomy property) | **vanishes** under length-matched control (≈1e-15) |

**Bottom line:** The simulation exhibits a real, built-in **non-reciprocal edge transport**
(`T_qp ≠ T_pq⁻¹`). It does **not** demonstrate **holonomy** in the standard sense
(loop/path-dependent transport). "Directed native holonomy" is the wrong name for the
object; "non-reciprocal directed transport" is the claim the math supports at full strength.

The paper is otherwise correctly bounded (it disclaims GR, curvature, ADM, continuum).
This review concerns only the holonomy claim.

---

## What holonomy requires

Holonomy = transport a quantity around a **closed loop** and compare to the start; the
signature is **path/loop dependence** (loop A ≠ loop B between the same endpoints). The
test for holonomy is therefore a *loop* test, not an *edge* test.

---

## Finding 1 — the "defect" is `mean(|C_corr|)`, not a holonomy defect

`native_directional_cycle_defect = |1 − H_cycle^dir| · mean(|C_corr|)`, with
`H_cycle^dir = Π_loop c_pq` a product of 8 normalized cosines.

```
seed= 168864 | H_cycle=-1.482e-03 | |1-H|=1.001482 | mean|C|=0.542648 | defect=0.543452
seed=      1 | H_cycle=-2.632e-04 | |1-H|=1.000263 | mean|C|=0.541756 | defect=0.541899
seed=     42 | H_cycle=+1.895e-05 | |1-H|=0.999981 | mean|C|=0.546950 | defect=0.546940
```

A product of 8 sub-unit cosines is generically ≈0, so `|1 − H_cycle| ≈ 1` always, and the
defect collapses to `mean(|C_corr|)` (matches to 3–4 digits every seed). **The defect
reports the size of the correction coordinate, not failure-to-close around the cycle.**

---

## Finding 2 — the directed signal is provenance-independent (γ-shuffle null)

The paper's evidence for *directedness* is `orientation_asymmetry` (forward vs reverse).
Across 200 seeds:

```
native (provenance order):  mean = 2.362e-04
gamma-shuffle null:         mean = 2.343e-04      <- shuffles provenance order
reciprocal control:         mean = 1.110e-18      <- forces T_qp = inverse
native / shuffle ratio = 1.008
```

- **Reciprocal control ≈ 1e-18:** confirms the test logic — when transport is reciprocal,
  asymmetry vanishes. So the asymmetry genuinely comes from non-reciprocity.
- **γ-shuffle null ≈ native (ratio 1.008):** destroying the provenance order changes the
  asymmetry by <1%. The asymmetry does **not** depend on the provenance structure it is
  named after. It is the generic residual of multiplying non-reciprocal cosines.

(The paper's own Section 15 already lists "raw orientation asymmetry as an independent law"
among *demoted* objects — this finding makes that demotion quantitative.)

---

## Finding 3 — no loop dependence under a length-matched control

The actual holonomy test: transport along two **same-length** routes between the same
endpoints and compare.

```
length-matched two-path difference: mean = 9.132e-16  max = 2.578e-15
```

Machine precision. Loops close. Any nonzero "path dependence" seen with unequal-length
paths was a **path-length confound** (more hops accumulate more), not holonomy.

---

## Interpretation

- **Real and worth claiming:** `T_pq` is non-reciprocal by construction (`T_qp ≠ T_pq⁻¹`),
  confirmed by the reciprocal control. This is a legitimate, interesting modeling choice
  consistent with "recombination is ordered and history-bearing." It is an **edge**
  property.
- **Not demonstrated:** that this non-reciprocity yields a **loop** holonomy. The three
  quantities offered (defect, orientation asymmetry, cycle product) are respectively a
  normalization artifact, a provenance-independent residual, and a generically-zero product.
  None exhibits loop/path dependence tied to the retained structure.

---

## Recommended edits (preserve everything actually shown)

1. Rename `native_directional_cycle_defect`: it is `mean(|C_corr|)·|1−H|` with `|1−H|≈1`.
   Report `H_cycle^dir` raw, or call the term a C_corr-scale, not a holonomy defect.
2. Do not present `orientation_asymmetry` as evidence of directed holonomy. Report the
   γ-shuffle null (ratio 1.008) alongside it.
3. Replace "produces directed native holonomy" with **"exhibits a non-reciprocal directed
   transport."** Nothing demonstrated is lost; the overreaching word is removed.

---

## Falsification of THIS review

This review's verdict flips if someone exhibits:
1. a **loop**-level quantity (length- and step-matched) that is nonzero for the native
   provenance cycle and ~0 for a shuffled/reciprocal control, at ≥3σ; or
2. an `orientation_asymmetry` that drops to the reciprocal-control floor (≈1e-18) under
   γ-shuffle while staying large for native order (i.e. provenance-dependent after all).

Neither was found here across 200 seeds. The edge-vs-loop distinction is the crux: edge
non-reciprocity is real; loop holonomy is not demonstrated.
