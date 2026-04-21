# Bridge-Closure Status Note

## Purpose

This note consolidates the current bridge-closure program into one master status statement.

It combines the strongest current results from:

- selector closure
- seam audit
- transfer audit
- ladder derivation

and records what is now strong enough to treat as the current bridge result versus what remains provisional.

---

## 1. Current overall status

The bridge is no longer at the stage of a loose hypothesis.

It now supports a structured and partially closed scientific picture:

1. a **hierarchical selector** rather than a flat selector
2. real local seam structure
3. strong family and perturbation transfer
4. renormalizable scale behavior
5. a lower weak ladder that emerges from normalized retained-envelope thresholding

This is the strongest current closure state.

---

## 2. Selector status

### Flat selector result
A single flat pointwise selector was too weak.
It captured coarse poles but compressed the hardest weak and boundary seams.

### Trajectory-level result
Trajectory-level regime signatures improved the map substantially and showed that the remaining confusion concentrated into two local seam problems:

- weak ladder ordering
- boundary/crossover ordering

### Hierarchical selector result
A hierarchical selector with:

- a coarse global router
- a weak-ladder local refiner
- a boundary/crossover local refiner

performed strongly:

- heldout accuracy ≈ **0.938**
- heldout macro F1 ≈ **0.933**
- leave-one-family-out macro F1 mean ≈ **0.884**

This is the strongest current selector result.

### Current selector conclusion
The bridge closes substantially better as a **low-complexity hierarchical selector** than as one flat classifier.

That is now a supported result.

---

## 3. Seam status

### Weak ladder seam
The weak ladder seam is real and ordered.
It does not collapse directly into noise.

However, it remains relatively narrow and still tends to be biased upward into the stronger weak class.

### Boundary/crossover seam
The boundary/crossover frontier now shows a soft measurable transition band.
This is the first strong evidence that the bridge supports real local seam geometry rather than only hard forced partitions.

### Crossover state
The explicit crossover state remains useful as a local abstention or caution state, but it does not yet appear as a broad stable repeated bulk region.

### Current seam conclusion
The bridge now supports:
- a real weak ladder seam
- a real soft boundary/crossover band

but:
- the exact thickness calibration remains incomplete
- the crossover state is still provisional as a repeated regime

---

## 4. Transfer status

### Cross-family transfer
Strong.

Current result:
- LOFO macro F1 mean ≈ **0.884**

### Cross-perturbation transfer
Strong.

Current result:
- mean perturbation macro F1 ≈ **0.876**

### Cross-scale transfer
Not fully raw-invariant.

Raw macro F1:
- T = 60 → ≈ **0.662**
- T = 100 → ≈ **0.863**
- T = 140 → ≈ **0.506**

### Scale renormalization
A small affine renormalization of the trajectory-signature space substantially restores scale performance:

- T = 60 → macro F1 improved to ≈ **0.906**
- T = 140 → macro F1 improved to ≈ **0.667**

### Current transfer conclusion
The bridge transfers strongly across:
- families
- moderate perturbations

and shows:
- structured but not fully raw-closed scale dependence
- substantial scale recovery under affine renormalization

This is a strong but qualified transfer result.

---

## 5. Ladder derivation status

The lower weak ladder was tested against simple threshold laws on normalized retained-envelope variables.

The strongest lower-ladder variable was:

- **eta_t_q75**
  (equivalently `v_t_q75` in the current construction)

A simple two-threshold law on this quantity separated the lower weak ladder on the heldout set with:

- heldout accuracy ≈ **1.000**
- heldout macro F1 ≈ **1.000**

with thresholds approximately:

- **0.8647**
- **1.6326**

### Current derivation conclusion
The lower weak ladder is now consistent with emergence from **nested thresholding of normalized retained mismatch**.

This is the first strong bridge-side support that the ladder is not merely hand labeling.

### Remaining limitation
With only three lower ladder levels currently stabilized, affine vs multiplicative recursion is not yet strongly distinguishable.

So nested thresholding is supported, but recursion family is still open.

---

## 6. Strongest current admissible claim

The strongest current admissible claim is:

> a retained-state bridge built from normalized residual-envelope coordinates supports a low-complexity hierarchical selector with real local seam structure, strong family and perturbation transfer, renormalizable scale behavior, and a lower weak ladder that emerges from nested thresholding of a normalized retained-envelope variable.

That is the strongest supported current bridge-closure claim.

---

## 7. Strongest current inadmissible overclaim

It is not yet justified to claim:

- full raw scale invariance
- final seam-thickness calibration
- a broadly repeated certified crossover bulk regime
- or a fully settled affine-versus-multiplicative recursion law for the ladder

Those remain open.

---

## 8. Best current publication posture

The bridge should now be described as:

- **selector closure:** strongly supported, in hierarchical form
- **seam structure:** supported, with some provisional local calibration
- **transfer:** strong on family and perturbation, qualified on scale
- **ladder derivation:** strongly supported for nested thresholding, qualified on recursion family

That is a strong and honest publication posture.

---

## 9. Best next step

The strongest next move is:

> convert this status into the current bridge memorandum / paper packet, with the open items clearly identified as:
- scale raw invariance
- seam thickness calibration
- crossover bulk certification
- recursion-family discrimination

That is now the correct transition from model work to scientific writeup.
