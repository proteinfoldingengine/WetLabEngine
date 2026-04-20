# Weak Multifrequency / Boundary Crossover Note

## Purpose

This note records the current scientifically sharpest unresolved seam inside the vector-family selector.

It concerns the crossover between:

- **true weak multifrequency**
and
- **balanced transient boundary**

The clearest current crossover pair is:

- `exotic_weak_multifreq_a`
- `balanced_blur`

These two cases now define the next refinement target.

---

## 1. Why this crossover note is needed

Recent selector refinements produced two complementary outcomes:

### v7
- preserved the weak-channel successes
- rescued clean multifrequency
- but still misread `balanced_blur`

### v8
- rescued `balanced_blur`
- but regressed `exotic_weak_multifreq_a`

This means the current seam is not accidental.
It is structural.

The selector can currently favor:
- weak multifrequency
or
- balanced transient boundary

but not both at once with one simple additional veto rule.

That is why this seam now deserves its own note.

---

## 2. The crossover pair

### Case A — exotic_weak_multifreq_a
Current best reading:
- **weak_signal_multifrequency**

Why:
- meaningful weak multifrequency evidence
- not simply noisy
- preserved by the safer v7 routing

### Case B — balanced_blur
Current best reading:
- **transient_boundary_directional**

Why:
- balanced mixed structure
- boundary-like rather than weak-success-like
- recovered by the stronger boundary veto in v8

These two cases now bracket the seam.

---

## 3. Scientific interpretation

The current evidence suggests this is not just a threshold problem.

It is better understood as a **crossover region** where:

- weak multifrequency evidence is present
- but boundary-like balance is also present

In other words:

> the selector is now encountering cases that legitimately share evidence from both channels.

That is why one-directional fixes cause tradeoff regressions.

---

## 4. Proposed next concept

The next scientifically honest move is to introduce an explicit abstaining intermediate notion such as:

> **weak_multifrequency_boundary_crossover**

This would not replace the existing states.
It would mark cases that:
- show weak multifrequency evidence
- but also show enough balanced-boundary structure that forcing one side causes regressions

This is the same logic that previously justified:
- `sub_boundary_weak_multifrequency`

Now the same reasoning is reaching the next seam.

---

## 5. Why this is scientifically useful

This refinement is useful because it prevents false neatness.

Instead of pretending the current selector can already separate every case cleanly, it acknowledges:

- some weak-channel cases are still true crossovers
- and that crossover is now concentrated into a very small number of patterns

That is a stronger scientific position than overclaiming clean separation.

---

## 6. Strongest current admissible claim

The strongest current admissible claim is:

> the weakest remaining selector seam is now concentrated in a crossover region between weak multifrequency and balanced transient boundary structure.

That is the correct current claim level.

---

## 7. Best next step

The strongest next move is:

> treat this crossover as an explicit abstaining selector state and test whether that removes the last forced tradeoff between `exotic_weak_multifreq_a` and `balanced_blur`.

That is the next meaningful scientific refinement.
