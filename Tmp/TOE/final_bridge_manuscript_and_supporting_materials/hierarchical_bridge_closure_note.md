# Hierarchical Bridge-Closure Note

## Purpose

This note records the current strongest bridge-closure result.

The central finding is that the retained-state bridge does **not** close best as a single flat selector. It closes substantially better as a **hierarchical selector** with:

1. a coarse global router
2. a weak-ladder local refiner
3. a boundary/crossover local refiner

This is the strongest current model result in the closure program.

---

## 1. Why the hierarchy was needed

Earlier closure tests showed that a single flat selector on pointwise coordinates was too weak.

### Flat pointwise selector
Using pointwise state variables such as:
- `u_t`
- `v_t`
- `Δu_t`
- `Δv_t`

the selector captured some coarse poles, but the weak frontier and boundary seams remained highly compressed.

### Pointwise selector with persistence
Adding short-window persistence improved results and separated structure from noise more clearly, but the selector still compressed:
- lower weak-channel states upward into `weak_signal_multifrequency`
- and some boundary states into switching-like structure

### Trajectory-level selector
Moving to trajectory-level regime signatures improved the situation substantially.
The coarse map became much clearer, but the remaining unresolved seams separated into two distinct local problems:

- weak-ladder ordering
- boundary/crossover ordering

This directly suggested a hierarchical architecture.

---

## 2. Hierarchical architecture

The current hierarchical bridge selector has three stages.

### Stage 1 — Coarse router
Routes trajectories into broad groups:
- coherent rotational
- multifrequency directional
- noisy scalar-like
- weak ladder group
- boundary/crossover group

### Stage 2A — Weak-ladder refiner
Locally resolves:
- `weak_signal_multifrequency`
- `sub_boundary_weak_multifrequency`

### Stage 2B — Boundary/crossover refiner
Locally resolves:
- `transient_boundary_directional`
- `switching_boundary_directional`
- `weak_multifrequency_boundary_crossover`

This architecture is still low-complexity.
It just respects the fact that the hardest seams are local ordering problems rather than one universal flat partition.

---

## 3. Current result

The hierarchical selector achieved:

- **heldout accuracy ≈ 0.938**
- **heldout macro F1 ≈ 0.933**
- **leave-one-family-out macro F1 mean ≈ 0.884**

with a small model:

- coarse router leaves: 5
- weak refiner leaves: 2
- boundary refiner leaves: 3

This is substantially stronger than the earlier flat selectors.

---

## 4. Scientific meaning

This result supports a stronger bridge interpretation.

The retained-state bridge appears to generate a **low-dimensional but multi-stage regime law**.

That means:
- the bridge still closes in a compact observable state
- but closure is hierarchical rather than flat
- local seam refiners are part of the law, not a hack

This is scientifically important because many real systems organize by:
- coarse global routing
followed by
- local discrimination within specific transition families

The bridge is now behaving that way.

---

## 5. Strongest current admissible claim

The strongest current admissible claim is:

> a retained-state bridge built from normalized residual-envelope coordinates supports a low-complexity hierarchical selector that separates the coarse regime map and locally resolves both the weak ladder and the boundary/crossover seam with strong heldout and family-transfer performance.

That is the strongest current claim level.

---

## 6. What remains before full closure

The bridge is closer to closure, but not fully closed yet.

The remaining required audits are still:

1. **Seam audit**
   - measure boundary thickness, purity, persistence, and drift

2. **Transfer audit**
   - verify survival across families, scales, and perturbations

3. **Ladder derivation**
   - show that the weak ladder emerges from retained-state normalization rather than hand labels

So the current hierarchy is the strongest selector result, but not the final full closure by itself.

---

## 7. Best current interpretation

The right interpretation now is:

- flat closure was too weak
- hierarchical closure works
- the weak frontier and boundary frontier are locally resolvable
- the bridge law appears structured and compact enough to be scientific
- final closure now depends on seam, transfer, and derivation audits

That is the most honest current reading.

---

## 8. Best next step

The strongest next move is:

> freeze the hierarchical selector as the current best model and move into the remaining closure audits:
- seam audit
- transfer audit
- ladder derivation

That is the correct next stage of the bridge program.
