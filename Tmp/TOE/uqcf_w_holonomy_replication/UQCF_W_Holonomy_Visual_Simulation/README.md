# UQCF-GEM — Visual W-Holonomy Simulation

This package turns the generalized-W observable-response holonomy theorem into a human-readable Python simulation.

## What it demonstrates

Starting from the explicit global state

\[
|\psi_W\rangle=a|100\rangle+b|010\rangle+c|001\rangle,
\qquad abc\neq0,
\]

the code independently performs:

1. construction of the full \(8\times8\) density matrix;
2. exact one- and two-qubit partial traces;
3. centered Pauli observable bases;
4. explicit Kubo–Mori/BKM metric matrices;
5. pair covariance-response maps;
6. metric whitening;
7. SVD-supported polar transport on each edge;
8. triangle composition \(H_\triangle=V_{31}V_{23}V_{12}\).

For pure generalized-W states, the executable assertions verify

\[
H_\triangle^\sharp H_\triangle=I,
\qquad
\operatorname{spec}(H_\triangle)=\{-1,+1,+1\},
\qquad
\det H_\triangle=-1.
\]

This is the lossless reflection result.

## Human-readable visuals

- `01_edge_transport_triangle.png` — the three pair links, phase rotations, and population signs.
- `02_loop_reflection_3d.png` — the loop leaves the transverse response plane unchanged and flips the population direction.
- `03_noise_threshold.png` — the exact edge covariance crossing that forces the topological class change.
- `04_noise_phase_diagram.png` — reflection, rank-loss boundary, and identity regions.
- `05_transition.gif` — animated reflection → rank loss → identity transition.
- `verification_summary.json` — machine-readable assertion results.

## Run

```bash
python -m pip install -r requirements.txt
python visual_w_holonomy_simulation.py --output-dir visual_output
pytest -q
```

To skip GIF generation:

```bash
python visual_w_holonomy_simulation.py --output-dir visual_output --skip-animation
```

## Why the transition is exact

For white-noise regularization

\[
\rho_\epsilon=(1-\epsilon)|\psi_W\rangle\langle\psi_W|+\epsilon I/8,
\]

the population response on edge \(ij\) has the sign of

\[
q_{ij}(\epsilon)
=
\epsilon(1-2p_i)(1-2p_j)-4p_ip_j,
\qquad p_i=|a_i|^2.
\]

The loop is a reflection when the product of the three signs is negative, the identity when it is positive, and rank deficient when one factor is zero. For \((p_1,p_2,p_3)=(0.8,0.1,0.1)\),

\[
\epsilon_*=\frac1{16}=0.0625.
\]

## Scientific boundary

A numerical simulation does not by itself constitute a formal mathematical proof. This package provides:

- an independent executable derivation from the global density matrix;
- strict numerical assertions;
- null and transition controls;
- visual explanation of the exact analytic identities.

The result concerns pair-marginal BKM observable-response holonomy. It is not a derivation of spacetime curvature, gravity, ADM dynamics, or Einstein's equations.
