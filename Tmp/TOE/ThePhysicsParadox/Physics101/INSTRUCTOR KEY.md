# Instructor Key — *When Conservation Isn't Enough*

**For instructor use. Contains answers, exact values, common student errors, and grading notes.**
All numbers below are computed from `phi_lab.py` with the default network (N=5, E=7).

---

## The one idea students should leave with

Conservation laws constrain, but on a looped network they **underdetermine**. The leftover freedom is the cycle space (dimension `E − N + 1`). Removing it requires *external* information — either a chosen cost rule (non-unique) or a measurement that resolves the loops (`rank(RZ) = β₁`). The transferable habit: *ask what selects the answer, not just what the answer is.*

If a student leaves believing the lab "proved" something about spacetime, the observer, or quantum mechanics, the framing has failed — redirect them to the boundary box. The lab shows a **structural resemblance** to the measurement problem, not a result about it.

---

## PART 1 — answers

**1a (by hand):**
- Loop count: `β₁ = E − N + 1 = 7 − 5 + 1 = 3`. ✓
- Two valid loops (any two independent ones), e.g. `0→1→2→0` (edges e0, e5, reverse e2) and `0→2→4→0` (e2, e3, reverse e6). Accept any two independent cycles drawn correctly.
- Adding a loop flow `z` keeps `BJ = s` because `Bz = 0` (a loop moves nothing across any node boundary). Full credit for stating `B(J+z) = BJ + Bz = s + 0 = s`.

**1b:**
1. Code reports `β₁ = 3` — matches the hand prediction.
2. Conservation errors all ≈ `1e-15` (machine zero). Meaning: every one of the three currents satisfies conservation *exactly* (to floating-point precision). The differences between them are **not** conservation violations.
3. The three currents differ in their circulating (loop) part but share the same source-crossing part. Conservation fixes only the latter, so it cannot distinguish the three — it is not a selector.

**1c (add edge `(3,4)`):**
- Predicted new `β₁ = E − N + 1 = 8 − 5 + 1 = 4`. **Confirmed: actual = 4.** Adding one edge that closes a new independent loop raises `β₁` by exactly 1, because it adds one independent element to the kernel of `B`.

> **Common errors, Part 1**
> - **Counting all cycles instead of *independent* ones.** Students may find 4–5 visible loops and report that as `β₁`. Clarify: `β₁` counts *independent* loops (a basis), given by the formula, not the total number of closed paths.
> - **Reading 1e-15 as "small error / not quite conserved."** It is machine zero = exactly conserved. Emphasize the difference between `1e-15` (an identity holding to precision) and, say, `1e-2` (a real residual).
> - **Disconnected graph trap (only if a student edits the edges and removes connectivity):** the formula `E − N + 1` assumes *one connected component*. If they split the graph, it becomes `E − N + (number of components)`. Worth mentioning if anyone's number looks off after editing.

---

## PART 2 — answers

**2a:**
1. All four cost-rule currents conserve to ≈ `1e-15`. ✓
2. They **disagree**. Largest disagreement ≈ **37%** of the current. Example, **edge e5 (node 1→2)** under the four rules:

   | cost rule | J on e5 |
   |---|---|
   | equal cost | −0.125 |
   | cost = length | −0.000 |
   | cost = 1/access | −0.112 |
   | cost = length/access | −0.003 |

   (Accept any edge reported correctly; e5 is the most dramatic — it ranges from ≈0 to −0.125.) Full per-edge reference for all rules is in the run log.
3. The network — nodes, edges, source — does **not** select the cost rule. The choice of `w` is external information the modeler supplies. This is the central point of Part 2.

**2b:**
1. `cost = length` penalizes long edges, so the minimum-cost current should **avoid** them (push current onto shorter edges).
2. Increasing one edge's length should *decrease* the current on it. Accept any correct directional prediction confirmed by re-running.

> **Common errors, Part 2**
> - **"One of these must be the *true* current."** Students often assume a privileged answer exists. The point is the opposite: all four are equally valid; physics (not the network) would have to supply the cost. Don't let them rank the metrics as "more correct" without an external reason.
> - **Confusing "unique given W" with "unique."** Each W *does* give a unique current — true. The ambiguity moved from "which loop coefficient" to "which W." Make sure they see the ambiguity was *relocated*, not removed.

---

## PART 3 — answers

**3a:**
1. Strong probe: `rank(RZ) = 3`, `β₁ = 3`, recovery error ≈ **4e-16** → recovered exactly. ✓
2. Weak probe: `rank(RZ) = 1`, `β₁ = 3`, recovery error ≈ **0.40** → failed; two loop directions remain undetermined.
3. Closure condition: **rank(RZ) = β₁** (the number of loops). The measurement resolves the flow iff it distinguishes every independent loop.

**3b (medium probe `R_med = Z[:, :2].T`):**
1. Prediction: with `β₁ = 3` and a probe resolving 2 loops, `rank(RZ) = 2 < 3` → **not** fully recovered.
2. Confirmed: `rank(RZ) = 2`, recovery error ≈ **0.40**. One loop direction (the third, unprobed one) remains free — that is exactly the residual ambiguity. Full credit for predicting partial failure *and* identifying that the unresolved direction is the loop the probe doesn't see.

> **Common errors, Part 3**
> - **Expecting the weak/medium probe to "partially work" proportionally** (e.g., "sees 2 of 3 loops → 67% accurate"). Not how it works: the unresolved directions are *completely* free, so the error reflects a whole missing dimension, not a fractional shortfall. The recovered current is exact on the resolved part and arbitrary on the rest.
> - **Thinking a bigger/random R always helps.** What matters is `rank(RZ)`, i.e. whether R's rows are *independent over the cycle space*, not how many rows R has. A probe with many rows that all see the same loop still has `rank(RZ) = 1`. Good discussion point.
> - **Reading "measurement" as physical/quantum.** Keep it concrete: R is a matrix that reports combinations of edge flows. The quantum-measurement connection is structural analogy only (boundary box).

---

## Grading rubric (suggested, 100 pts)

| Item | Pts | Looking for |
|---|---|---|
| 1a hand prediction | 15 | `β₁ = 3` from the formula; two independent loops drawn |
| 1b conservation reading | 15 | identifies 1e-15 as exact; explains conservation isn't a selector |
| 1c add-edge prediction | 10 | predicts `β₁ = 4` before running; explains +1 loop |
| 2a cost disagreement | 15 | reports ~37%; states the cost choice is external |
| 2b metric-effect prediction | 10 | correct direction (avoids long edges), confirmed |
| 3a closure condition | 15 | `rank(RZ) = β₁`; strong succeeds, weak fails |
| 3b medium-probe prediction | 10 | predicts partial failure; identifies unresolved loop |
| Final paragraph | 10 | clear statement of underdetermination + what selects |

**Bonus (up to 5):** a student who, unprompted, writes a correct "what this does and doesn't show" boundary in their own words — that is the deepest learning outcome and worth rewarding.

---

## Discussion prompts (if time allows)

1. *Kirchhoff in circuits:* a resistor network with loops is underdetermined by current conservation alone — Ohm's law (a cost/metric!) is what selects the actual currents. Ask: what plays the role of `W` in a real circuit? (Answer: resistance.) This grounds Part 2 in something they've seen.
2. *Where does the cost come from in nature?* In circuits it's resistance; in fluids, viscosity; in optimal transport, a chosen cost functional. The lab's point is that the *network topology* never supplies it.
3. *The honest analogy:* the closure-vs-selection structure resembles the quantum measurement problem. Stress what's the same (a conserved structure underdetermines; interaction selects) and what's different (this is classical graph algebra, not Hilbert space). Good place to model scientific humility.

---

## Notes for the instructor
- Runtime is ~1 second; no GPU, no internet. Works on a lab machine with `numpy`/`matplotlib`.
- If students edit the network and break connectivity, the Betti formula changes (see Part 1 common errors) — a feature, not a bug, and a good teachable moment.
- The five figures regenerate on every run into `lab_figures/`. Safe to delete and re-run.
- Keep the framing math-only. The value of this lab is as much about teaching *epistemic discipline* (state what you showed, mark what you didn't) as about the linear algebra.
