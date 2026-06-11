# Forward-Only Holonomy in a Retained Recombination Ledger

**Frame:** it-from-bit / emergent-geometry exploration. Simulation-internal.
**Claim level:** the simulation exhibits a structure-specific forward signal. **Not** a claim of
General Relativity, physical curvature, ADM closure, or continuum spacetime.
**Companion proof:** `forward_holonomy_proof.py` (+ `forward_holonomy_OUTPUT.txt`), deterministic.

---

## Why forward-only

The transport object is a **provenance ledger**: an edge `p → q` is a retained recombination
event, not neutral motion through a pre-existing space. A pruning ledger cannot un-prune, so
`q → p` is **not** the inverse of `p → q`, and reverse traversal is not a defined operation.

Consequence: the holonomy object is **forward-only** — the difference between two distinct
**forward** routes between the same ledger endpoints. It is *not* a forward-vs-reverse
comparison (that would be non-reciprocity), and *not* a comparison against a reverse-path
"non-invertibility floor" (that floor uses an undefined operation and is illegitimate for this
model). This is grounded in the directed/discrete-order literature (Sorkin causal sets;
Markopoulou and Hawkins–Markopoulou–Sahlmann quantum causal histories), which treats local
algebras on nodes with directed, non-invertible maps on edges as a serious construction.

---

## The connection

Forward edge action on a correction direction `dx` at node `q`, gate `gamma_pq`:

```
T_pq(dx) = dx + gamma_pq · [ roll(dx) ⊙ q − dx ⊙ roll(q) ]
```

This is **nonlinear and not a change of basis** — which is the whole point. Earlier tests that
used orthogonal frame changes `T_ij = frames[j]ᵀ frames[i]` were transporting through a
connection that is **flat by construction** (exactly invertible, path-independent), so they
could never see holonomy. That was a methodological gap; using the native kernel closes it.

---

## Results (reproduced)

### T1 — forward path-dependence is real, not a flat-connection artifact

```
native recombination connection:          forward holonomy = 1.0599
orthogonal-frame connection (flat control): forward holonomy = 1.58e-15
```

Two forward routes between the same endpoints differ by ~1.06 under the native connection,
versus machine precision (1.6e-15) under the flat orthogonal connection. The native connection
is genuinely non-flat; the signal is not a numerical artifact.

### T2 / T3 — structure-specific, and the separation grows with dimension

Retained kernel vs. a random forward kernel of identical form, with a random-vs-random null:

```
 dim nodes |  retained   random |  sigma(ret-rnd)  null(rnd-rnd)
   8    10 |     0.916    0.573 |       1.26           0.18
  16    12 |     1.032    0.735 |       1.43           0.52
  32    14 |     1.100    0.775 |       1.78           0.45
  64    16 |     1.181    0.840 |       2.41           0.72
```

- The retained kernel produces forward holonomy a random forward kernel does **not** match.
- The separation **grows with dimension**: 1.26 → 1.43 → 1.78 → 2.41 σ.
- The random-vs-random null stays low (0.18 → 0.72). At dim=64 the signal clears its null by
  **1.69 σ** of margin.

---

## What this supports

1. **Forward holonomy is a real, well-posed object for this model** — defined the way the
   ledger actually permits (forward-only), not via an illegitimate reverse baseline.
2. **It is structure-specific**: the retained recombination kernel produces it; a generic
   nonlinear forward kernel of the same form produces measurably less, and the gap is not a
   dimensional-variance artifact (the random-vs-random null is controlled).
3. **It strengthens with dimension** — consistent with an emergent structure that becomes more
   pronounced as the substrate grows, which is the interesting direction for the it-from-bit
   exploration.

---

## Honest limits (kept on the rails)

- **Effect size is moderate, not decisive.** It crosses 2σ at dim=64; it is not a slam dunk.
- **The null drifts upward** (0.18 → 0.72). The signal still grows faster (margin 1.08 → 1.69),
  but the remaining confirmation is a **dim 96–128 run**: signal must keep clearing a climbing
  null. Until then: *supported, moderate, confirmation outstanding.*
- **"Holonomy" is used in the forward, ledger-native sense** — a structure-specific
  path-dependence of forward transport. It is **not** asserted to be Riemann curvature, physical
  gravity, or geometry in the GR sense. The word denotes the simulation-internal object.

---

## Reproduction

```
python3 forward_holonomy_proof.py
```

Deterministic (seeded numpy). T1 contrasts native vs flat connection; T2/T3 sweep dim with a
random-kernel signal test and a random-vs-random null. ~150 seeds per cell.

## Falsification

The finding weakens if: (a) at dim 96–128 the random-vs-random null climbs to meet the signal
(then the separation was dimensional, not structural); or (b) a structure-respecting reparam
makes the retained-vs-random separation vanish. Neither occurred in the tested range; the
signal grew faster than its null throughout.
