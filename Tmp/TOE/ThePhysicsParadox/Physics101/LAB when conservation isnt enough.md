# Lab: When Conservation Isn't Enough
### Underdetermination, loops, and measurement on a small network

**Level:** First-year computational physics
**Time:** ~90 minutes
**You need:** `python`, `numpy`, `matplotlib`, the file `phi_lab.py`, and a pencil.

---

## The question this lab is about

You have learned conservation laws: charge in equals charge out, current is conserved at a junction (Kirchhoff), mass is neither created nor destroyed. Conservation laws are powerful — but here is a question that is easy to ask and surprising to answer:

> **If a system obeys a conservation law, does that fix a unique answer for what the system is doing?**

Your intuition probably says "yes, more or less." This lab shows that on any network with **loops**, the answer is **no** — conservation leaves a whole family of equally valid flows. You will see *why*, see what it takes to pick one, and meet a pattern that echoes some of the deepest open questions in physics.

You are **not** going to derive anything about spacetime or quantum mechanics here. You are going to understand one clean, true, checkable piece of mathematics — and then be shown, honestly, where it resembles bigger questions and where it does not.

---

## Background you need (one page)

A **network** (graph) is nodes joined by directed edges. We push a fixed amount of "stuff" in at one node and out at another — that is the **source** vector `s`.

A **flow** (or **current**) `J` assigns a number to each edge: how much flows along it (negative = flows the other way).

The **incidence matrix** `B` records the wiring: for each edge, `−1` at its tail node and `+1` at its head node. Then the statement *"flow is conserved at every node"* is exactly the single equation:

```
B J = s
```

Each row is one node's balance: (flow out) − (flow in) = (source at that node).

A **loop** (cycle) is a closed path. If you send flow around a loop, **nothing enters or leaves any node** — it just circulates. In equation form, a loop flow `z` satisfies `B z = 0`. The set of all loop flows is the **cycle space**, and its dimension (the number of independent loops) is:

```
number of independent loops = E − N + 1        (for a connected network)
```

This is the network's **first Betti number**, `β₁`. Keep this formula — you will predict it by hand.

The punchline you are about to verify: if `J` solves `B J = s`, then **`J + z` solves it too**, for *any* loop flow `z`. Conservation fixes the part that crosses node boundaries and says **nothing** about the circulating part.

---

## PART 1 — See the ambiguity

### Exercise 1a — Pre-lab, by hand (do this before running anything)

The network in the code has **N = 5 nodes** and **E = 7 edges**.

1. Using `loops = E − N + 1`, **predict the number of independent loops.** Write it down: `β₁ = ______`
2. Sketch the 5-node network from the edge list in `phi_lab.py` (`EDGES = [...]`). Find **two different loops** by eye and draw them.
3. Predict: if I have one valid current and add a loop flow to it, will conservation `B J = s` still hold? Why?

### Exercise 1b — Run and check

Run `python phi_lab.py`. Look at the **Part 1** printout and the figure `lab_figures/part1_ambiguity.png`.

1. Does the code's loop count match your hand prediction from 1a?
2. The figure shows **three different currents**. Read off the conservation error `|BJ − s|` for each. What is its size, and what does that size mean? *(Hint: 1e-15 is "machine zero" — as exact as a computer gets.)*
3. In your own words: the three currents are visibly different (different arrow thicknesses and directions). What do they have in common? What does this tell you about conservation as a "selector"?

### Exercise 1c — Make it your own

Add one edge to `EDGES` (for example `(3,4)`) and re-run.
1. **Before running**, predict the new loop count with `E − N + 1`.
2. Run and confirm. Did adding one edge that closes a new loop increase `β₁` by exactly 1? Explain why that makes sense.

---

## PART 2 — Try to fix it with a cost rule, and watch it slip

A natural idea: "pick the *cheapest* flow." Assign each edge a cost weight `w`, and choose the conserved current that minimizes total cost `Σ wₑ Jₑ²`. This is the **minimum-cost** (Hodge) current, and for any positive cost it gives **one** answer.

So the ambiguity is solved... if everyone agrees on the cost.

### Exercise 2a — Run and compare

Look at the **Part 2** printout and figures `part2_metric_disagreement.png` and `part2_edge_comparison.png`.

1. Four cost rules each produce a unique conserved current. Do they all conserve? (Check the printed errors.)
2. Do they **agree** with each other? Read the "largest disagreement" line, and look at the bar chart — pick one edge and report its current under all four rules.
3. **The key question:** the network itself — its nodes, edges, and source — does it tell you which cost rule is the right one? Where does the choice of cost come from?

### Exercise 2b — Predict a metric's effect

The rule `cost = length` penalizes long edges.
1. **Predict:** will the minimum-cost current *avoid* or *prefer* long edges? Why?
2. Change one edge's length in the `edge_len` array, re-run, and check whether the current on that edge moved the way you predicted.

> **Lesson of Part 2:** "minimize a cost" is a real method, but it only relocates the question. The unique answer now depends on a choice of cost that the network does not make for you. Picking the cost is *external* information.

---

## PART 3 — Resolve it with a measurement

Now the honest resolution. Suppose there is a real, definite flow (call it the "hidden true current"). We don't get to see it directly — we **probe** it with a measurement. A measurement is a matrix `R` that reports some combination of the edge flows. From what `R` tells us, we try to reconstruct the full current.

The cycle space is what conservation left undetermined. So the question becomes: **does our measurement `R` distinguish the loops?**

### Exercise 3a — Run and read the gate

Look at the **Part 3** printout and figures `part3_measurement_closure.png`, `part3_rank_gate.png`.

1. The **strong probe** sees every loop. Report `rank(RZ)`, the loop count `β₁`, and the recovery error. Did it recover the true current?
2. The **weak probe** sees only one loop. Report the same three numbers. Did it succeed?
3. State the closure condition in your own words. Fill in:
   > The measurement recovers the unique current exactly when **rank(RZ) = ______**.

### Exercise 3b — Build your own probe (predict then verify)

In the code, `R_full = Z.T` (sees all loops) and `R_weak = Z[:, :1].T` (sees one). Make a **medium** probe that sees exactly two loops: `R_med = Z[:, :2].T`.
1. **Predict:** with `β₁ = 3` loops and a probe that resolves 2 of them, will the current be fully recovered? What will `rank(RZ)` be?
2. Add `R_med` to the code, recover with it, and check. Was your prediction right? How large is the leftover error, and which part of the flow is still undetermined?

---

## What this lab shows — and what it does NOT show

**Read this box carefully. Stating the boundary of a result is part of doing science.**

**What you have genuinely shown (true, exact, checkable):**
- On a network with loops, **conservation alone does not determine a unique flow.** The leftover freedom is exactly the cycle space, dimension `E − N + 1`.
- **Adding a cost rule selects a flow, but non-uniquely:** different defensible costs give different flows, and the network does not pick the cost.
- **A measurement resolves the flow exactly when it distinguishes all the loops:** `rank(RZ) = β₁`. Too weak a measurement leaves a residual ambiguity.

**What you have NOT shown (do not claim these):**
- You have **not** derived spacetime, gravity, general relativity, or quantum mechanics. This is a finite graph, not a physical theory of the universe.
- You have **not** proven anything about what "the observer" is in physics. `R` here is just a matrix that reads edge flows.

**Where it honestly connects to bigger questions (this is a *resemblance in structure*, not a proof):**
The pattern you saw — *a conserved structure leaves a family of possibilities, and it takes an interaction/measurement to single out one* — has the **same shape** as a famous unsolved problem in physics: the **measurement problem** in quantum mechanics, where the equations allow many possibilities (superposition) and measurement somehow yields one definite outcome. Physicists genuinely disagree about how that selection works. Your network is *not* a quantum system, and this lab does not resolve that debate. But noticing that the same *closure-vs-selection* structure appears in something as simple as flow on a graph is a real and worthwhile insight: it suggests the pattern may be general to conserved systems, not special to quantum mechanics.

**The transferable skill:** when a system is underdetermined, the right question is not "what is the answer?" but **"what additional information selects the answer, and where does that information come from?"** That habit — and the discipline of stating exactly what you showed and what you didn't — is what you should take from this lab.

---

## What to hand in
1. Your hand predictions from 1a (loop count + two sketched loops) and whether the code matched.
2. The three conservation errors from Part 1 and one sentence on what they mean.
3. The largest cost-rule disagreement from Part 2 and your answer to 2a.3 (where does the cost choice come from?).
4. The completed closure condition from 3a.3, and your `R_med` prediction-and-result from 3b.
5. One paragraph: in your own words, why doesn't conservation determine a unique flow, and what does it take to pin one down?
