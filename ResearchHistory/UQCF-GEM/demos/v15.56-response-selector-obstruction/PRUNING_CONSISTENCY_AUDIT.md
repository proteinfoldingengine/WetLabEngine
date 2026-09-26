# v15.56 — Exact pruning consistency audit (corrective continuation)

**Audited snapshot:** `23b6b4487cad036870246af1b044f5ee41784c92` (through Task 37).
**Scope:** the four unchanged Task 30/32 prefix-tree fixtures; exact theorems below apply to finite connected prefix trees with a root-containing, prefix-closed retained subtree. This is a mathematical diagnostic within the retained-response program, not a newly selected physical source law.

## Executive finding

The previous numerical outputs reproduce, but their strongest interpretation needs correction. Task 32's full-source obstruction includes a source-centering mismatch. It is not a proof that all sensible coarse response maps fail. With consistent source transport, restriction to retained vertices satisfies an exact operator identity in all four fixtures, without fitted weights or tolerances.

Task 31 also contains only **two distinct normalized aggregation operators**, not three: its two depth formulas are proportional within each fiber and normalize to the same map. Its twelve recorded numbers remain valid; four duplicate the other depth control. A finite list of nonzero mismatches never certified every admissible measure.

The historical source, tests, fixtures, and outputs are retained unchanged. This audit is separate and supersedes broad interpretations, not the recorded calculations.

## 1. Source centering is not a gauge-free pushforward

Let `n` and `m` be the fine and coarse vertex counts. Write `L_f,L_c` for the unweighted incidence Laplacians, `G_f=L_f^+`, `G_c=L_c^+`, and `C_f=I-11^T/n`, `C_c=I-11^T/m`. The extensive pushforward `P` sums over longest-retained-prefix fibers. The potential restriction `S` selects the value at each retained vertex, with no interpolation.

The historical Task 32 matrix tests

`C_c A G_f = lambda G_c P`

on the **entire raw fine source space**, although the module describes a zero-mean source quotient. If `J=1_f`, its left side is zero for every possible `A`. Its right side is `lambda G_c b`, where `b=P1_f` is the fiber-size vector. For `lambda != 0`, equality requires `b` to be constant. Every frozen fixture has unequal fiber sizes. Thus this particular equation is impossible even for a dense, signed, nonlocal `A`; fiber-local positivity is not the cause of this obstruction.

If sources are represented modulo constants, `P` descends to that quotient only when `P1_f` is coarse-constant. Alternatively, use the zero-sum subspace as the source space: `P` preserves its total-zero condition. These are different constructions and must not be silently identified.

Explicitly,

`P C_f - C_c P = (1_m/m - b/n) 1_f^T`.

This is a rank-one discrepancy in all four fixtures. Fine centering and coarse re-centering subtract different background source distributions. Conserving the raw total source does not remove this difference.

## 2. Exact retained-boundary response theorem

**Theorem.** Under the prefix-tree hypotheses,

`P L_f = L_c S`,

and therefore

`C_c S G_f = G_c P C_f`.

**Proof.** A retraction fiber contains one retained vertex and the discarded branches attached to it. In the sum of `L_f phi` over this fiber, every internal edge cancels. Because the coarse set is prefix closed, the only edges crossing fibers are edges between retained parent-child vertices. The surviving terms are exactly `L_c S phi`. This proves the first identity for every fine potential, not just a selected source.

For `phi_f=G_f J`, we have `L_f phi_f=C_f J`. Apply `P`, use the first identity, and solve on the coarse zero-mean subspace. Since `G_c L_c=C_c`, the second identity follows. No additional rescaling is needed.

Thus the compatible source is

`J_c^balanced = P C_f J = P J - (sum J) b/n`.

It transports the actual centered fine forcing, including its compensating background. The historical alternative was `C_c P J`, with a freshly uniform coarse background. This audit does not select either background as a physical axiom: it identifies which one preserves the stated fine equation.

Restriction to retained vertices is nonnegative and row-normalized, but assigns **zero**, not strictly positive, weight to removed vertices. Therefore it is not a counterexample to a precisely stated strictly-positive-averaging no-go; it is a counterexample to the broader assertion that every fiber-local linear response map fails on consistently transported sources.

## 3. Exact uniqueness in the normalized fiber-local family

Let `m>=2`, require `A1_f=1_m`, and require row `v` of `A` to be supported only on `r^{-1}(v)`. Suppose

`C_c A G_f = lambda G_c P C_f`

with a positive common scale. Multiply by `L_f` and use the boundary identity to obtain

`C_c A = lambda C_c S`.

Consequently `A-lambda S=1_m z^T`. For each fine column there is another coarse row outside its fiber. Locality makes that entry zero, forcing that coordinate of `z` to vanish. Hence `A=lambda S`; row normalization gives `lambda=1`.

**The unique normalized fiber-local compatible map is retained-vertex restriction.** If any vertex was removed, strict positivity at every fine vertex is impossible. This is an exact, scoped no-go about averaging, alongside an exact existence theorem for boundary restriction. The singleton coarse graph is degenerate and excluded from the uniqueness statement.

## 4. What Task 33 actually proves

For a specified response map `Q`, the elementary factorization theorem is

`there exists B with BP=QG_f iff ker(P) is contained in ker(QG_f)`.

Necessity follows by applying both sides to `ker(P)`. Sufficiency follows by defining `B(PJ)=QG_f J`; the kernel condition makes this definition independent of the representative. This is not generally the condition that `ker(P)` be invariant under `G_f`.

When `Q` removes only a constant from the **entire fine response**, a within-fiber contrast `e_u-e_v` lies in `ker(P)` but has a nonzero fine Green response. That proves that the complete fine response cannot be reconstructed from the pruned source alone.

When `Q=C_c S` selects the retained response, the same contrast is invisible: the exact boundary theorem gives `QG_f(e_u-e_v)=0`. Both statements can be true. Lost interior response information must not be conflated with failure of retained-boundary response consistency.

Task 35's fine-information obstruction and Task 37's nested kernels remain meaningful in their stated information-loss roles. A filtration `K_j=ker(P_{0->j})` and dimensions `n_0-n_j` do not, by themselves, establish a new force law or a nonzero retained-boundary response defect.

## 5. Task 31 duplicate-measure correction

Within the fiber of `v`,

`2^(-(depth(k)-depth(v))) = 2^(depth(v)) * 2^(-depth(k))`.

The factor is constant in that fiber and cancels when normalizing the weighted average. Absolute-depth and fiber-depth conditional expectations are therefore identical for every input field, not just accidentally equal in the four runs. The distinct tested aggregators were counting and depth attenuation. Neither weight choice was independently derived as the unique physical retained measure.

## 6. Exact executable receipts

`pruning_consistency_audit.py` uses only the Python standard library. All matrix inverses, ranks, kernel witnesses, and identities use `fractions.Fraction`. Floating point is used only to reproduce the historical ray-distance diagnostic.

| Fixture | Fiber sizes | Raw Task 32 nullity | Balanced operator nullity | Exact boundary-response residual |
|---|---|---:|---:|---:|
| 1 | 1, 3, 3 | 0 | 1 | 0 |
| 2 | 1, 2, 3 | 0 | 1 | 0 |
| 3 | 1, 1, 3, 2 | 0 | 1 | 0 |
| 4 | 1, 1, 1, 2, 2 | 0 | 1 | 0 |

The normalized solution has scale 1 and weights 1 on retained vertices, 0 on discarded ones. The old counting mismatches reproduce as approximately 0.0670206, 0.2478566, 0.2195105, and 0.0838089. They are not deleted or relabeled as zero: they compare a different source/aggregation convention.

Run from this demo directory:

```sh
python -m unittest -v test_pruning_consistency_audit
python pruning_consistency_audit.py
```

The companion JSON records exact rational witnesses. The local test-first receipt was 1 expected assertion failure with 14 skipped tests before the checker existed, followed by all 15 passing after implementation. Full historical CI is separate and is not claimed as locally reproduced.

## 7. Scientific direction and prior art

The useful conclusion is a separation between **discarded interior information**, **retained-boundary observables**, and **source-background transport**. This gives the program a sharper baseline for testing repair-history or higher-incidence effects. Any proposed new response signal must exceed this exact graph-reduction baseline, rather than merely rediscover averaging or centering mismatch.

Boundary-preserving elimination through Laplacian Schur complements is established graph/network mathematics (Kron reduction), not a novelty claim here. See F. Dörfler and F. Bullo, *Kron Reduction of Graphs with Applications to Electrical Networks*, IEEE Transactions on Circuits and Systems I, 60(1), 150–163 (2013), DOI 10.1109/TCSI.2012.2215780; author preprint: https://arxiv.org/abs/1102.2950 . The elementary prefix-tree proof above is self-contained and does not import a geometric coarse-graining primitive.

The next scientific comparison should keep the source background and observable fixed and test whether additional certified retained/repair structure contributes response information not contained in the graph Laplacian and its standard boundary reduction.
