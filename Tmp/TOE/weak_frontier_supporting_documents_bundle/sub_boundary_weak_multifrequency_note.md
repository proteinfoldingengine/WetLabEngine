# Sub-Boundary Weak Multifrequency Note

## Purpose

This note records the current scientific refinement of the weakest remaining vector-family seam.

It concerns the case:

- **exotic_weak_multifreq_b**

This case has repeatedly resisted clean assignment to either:

- **weak_signal_multifrequency**
or
- **noisy_scalar_like**

The current evidence supports treating it as the first candidate for a new intermediate state:

> **sub_boundary_weak_multifrequency**

---

## 1. Why this refinement is needed

Several detector refinements have already been tested against the hardest weak-signal seam:

- global spectral richness
- windowed instability
- phase-shape smoothness
- segment-presence logic
- weak multifrequency evidence score
- gated weak-multifrequency logic

These refinements produced a clear pattern:

### What stayed true
- clean noisy contrast cases stayed noisy
- clean multifrequency cases stayed multifrequency
- true boundary cases stayed boundary after gating
- a stronger weak multifrequency case (`exotic_weak_multifreq_a`) remained classifiable

### What did not resolve
- `exotic_weak_multifreq_b` still failed to cross the threshold into weak multifrequency
- but it also continued to show more structure than simple noise in some local windows

This means the case is not well-described by the existing two-way choice.

---

## 2. Why it should not be forced into noisy_scalar_like

The evidence against collapsing it fully into noisy contrast is:

- it still shows **nonzero segment presence** of structured windows
- it retains some weak multifrequency evidence
- it is not simply featureless noise
- its failure mode is much narrower than the true noisy-contrast neighbors

So calling it purely noisy is too coarse.

---

## 3. Why it should not yet be promoted to weak_signal_multifrequency

The evidence against promoting it fully into weak multifrequency is:

- it does not pass the weak-signal rescue tests
- it remains too degraded under the current thresholds
- detector rescues that tried to include it caused regressions into true boundary cases
- its evidence is weaker and less stable than the already-supported weak multifrequency case

So calling it a clean weak multifrequency state would currently overclaim.

---

## 4. Proposed intermediate state

### New candidate state
**sub_boundary_weak_multifrequency**

### Intended meaning
A case with:
- some recurring multifrequency structure
- not enough evidence for weak multifrequency closure
- more structure than noisy contrast
- but too degraded to count as a stable weak multifrequency success

### Scientific interpretation
This is an intermediate regime that sits:

- below **weak_signal_multifrequency**
- above **noisy_scalar_like**
- and near the vector-side weak boundary

That is why “sub-boundary” is the right label.

---

## 5. Why this is scientifically honest

This refinement is not inflationary.
It is conservative.

It does not claim:
- that the weak case is already solved
- that it belongs in the multifrequency success bucket
- or that noise is the whole story

Instead it says:

> the current science has isolated a real intermediate state that should not be overcollapsed into either of the existing buckets.

That is the most honest reading of the evidence.

---

## 6. Current placement in the vector-family map

The vector-family map now reads:

1. **coherent_rotational_directional**
2. **multifrequency_directional**
3. **weak_signal_multifrequency**
4. **sub_boundary_weak_multifrequency**   <-- new candidate
5. **transient_boundary_directional**
6. **switching_boundary_directional**
7. **noisy_scalar_like**

This is now the clearest scientific refinement of the vector side.

---

## 7. Strongest current admissible claim

The strongest current admissible claim is:

> the weakest unresolved vector-side seam is now best interpreted as a sub-boundary weak multifrequency state rather than as a clean success or simple noise.

That is the correct current claim level.

---

## 8. Strongest inadmissible overclaim

It is not yet justified to claim:
- that this new state is final
- that it will survive all future out-of-suite testing
- or that every ultra-weak multifrequency case belongs here

Those remain open.

---

## 9. Best next step

The strongest next move is:

> explicitly add **sub_boundary_weak_multifrequency** to the vector-family map and selector as an abstaining intermediate state, then test whether that reduces forced misclassification without harming the clean states.

That is the next scientifically meaningful refinement.
