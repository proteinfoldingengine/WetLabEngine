# Vector Family Selector v4

## Scope

This selector is the first explicit **six-state** internal routing system for the vector family.

It routes vector-side cases into:

1. **coherent_rotational_directional**
2. **multifrequency_directional**
3. **weak_signal_multifrequency**
4. **transient_boundary_directional**
5. **switching_boundary_directional**
6. **noisy_scalar_like**

This is a restricted selector built from the current tested suite and refinement work.

---

## 1. Why v4 is needed

Earlier selector versions were strong enough to discover and separate:
- clean rotational cases
- clean multifrequency cases
- boundary directional cases
- noisy contrast cases

But later refinement showed that two “failure” patterns were actually real internal states:

- **weak_signal_multifrequency**
- **switching_boundary_directional**

So the selector must now be expanded from the earlier four-state version to the full six-state version.

That is what v4 does.

---

## 2. Six routing states

### A. coherent_rotational_directional
Use for:
- smooth spiral-like or chirped rotational cases
- highly coherent directional geometry
- cases favoring high-retention clipped vector memory

### B. multifrequency_directional
Use for:
- clean structured multi-frequency directional cases
- Lissajous-like directional regimes
- cases favoring lower-retention vector memory

### C. weak_signal_multifrequency
Use for:
- blurred or weaker multifrequency cases
- directional structure present, but not strong enough for the clean multifrequency bucket
- cases rescued by spectral richness rather than by geometry alone

### D. transient_boundary_directional
Use for:
- balanced mixed directional geometry
- directional but not closure-clean
- cases best interpreted as vector-side boundary states

### E. switching_boundary_directional
Use for:
- vector-side boundary cases with episodic switching or instability
- more structured than simple noise
- not stable enough for a clean subclass assignment

### F. noisy_scalar_like
Use for:
- noisy contrast states
- irregular geometry that should not be over-promoted into clean vector routing

---

## 3. Current feature layers

Vector Family Selector v4 now rests on three feature layers:

### Geometry layer
- winding
- monotonicity
- sign-change rate
- angular velocity
- acceleration variance

### Spectral layer
- dominant spectral fraction
- effective mode count
- spectral concentration vs spread

### Weak/boundary refinement layer
- logic for weak multifrequency recovery
- logic for switching-boundary recognition
- logic separating noisy contrast from true vector-side weak structure

These three layers define the current selector.

---

## 4. Strongest current admissible claim

The strongest current admissible claim is:

> the vector family now supports a six-state internal selector that reflects both clean and weak directional subclasses on the current tested suite.

That is the correct current claim level.

---

## 5. Strongest inadmissible overclaim

It is not yet justified to claim:
- that the six-state selector is final
- that no further vector-side states exist
- or that the six-state map is universal across all future directional families

Those remain open.

---

## 6. Scientific meaning

Vector Family Selector v4 matters because it means the program has now moved beyond:

- scalar vs vector
- vector split into rotational vs multifrequency
- and now into a **full six-state internal vector routing system**

That is a major increase in scientific structure.

It means the vector family is now being treated as a real internal regime system, not just one auxiliary branch.

---

## 7. Best next step

The strongest next move is:

> test whether the six-state vector-family selector remains stable on new out-of-suite directional families without collapsing weak states back into generic boundary or noise buckets.

That is the next scientifically meaningful stress test.
