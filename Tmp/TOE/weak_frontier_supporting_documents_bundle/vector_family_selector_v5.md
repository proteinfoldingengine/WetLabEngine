# Vector Family Selector v5 — Weak-Channel Refinement

## Purpose

This selector extends the vector-family routing system to include:

- **sub_boundary_weak_multifrequency**

as an explicit output state.

The vector-family selector now routes into:

1. coherent_rotational_directional
2. multifrequency_directional
3. weak_signal_multifrequency
4. sub_boundary_weak_multifrequency
5. transient_boundary_directional
6. switching_boundary_directional
7. noisy_scalar_like

This update is motivated by the ultra-weak seam-family test, which showed a real intermediate band between weak multifrequency and noisy contrast.

---

## Key idea

Weak-channel routing now has three levels:

- **weak_signal_multifrequency**
- **sub_boundary_weak_multifrequency**
- **noisy_scalar_like**

This is more honest than forcing the weakest cases into only a success-or-noise dichotomy.

---

## Current scientific role

Selector v5 should improve weak-channel honesty without disturbing the already-established clean states.
