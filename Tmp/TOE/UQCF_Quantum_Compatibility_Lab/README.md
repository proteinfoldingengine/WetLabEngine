# UQCF–GEM: Computed Quantum Compatibility Lab

## Start here

- `output/UQCF_Quantum_Simulation.mp4`: 27-second film: actual distance curve, two computed 3D sections, and a collective measurement example.
- `output/UQCF_Quantum_Lab.html`: self-contained interactive lab. Open in a browser; drag to rotate and use the state-sample sliders. No network connection is needed.
- `UQCF_Quantum_Compatibility_Lab.ipynb`: self-contained notebook, suitable for Colab or Jupyter. Run all. It installs missing dependencies and does not require any other file from this archive.
- `uqcf_quantum_lab.py`: standalone implementation. Install `requirements.txt`, then run `python uqcf_quantum_lab.py --out output --render`. MP4 generation requires ffmpeg. Without `--render`, computation, validation, data and interactive HTML are still produced.

## What was actually computed

The v9.167–v9.171 matched four-weight family on three five-level quantum systems, A, B1, B2. Global density matrices are 125 by 125; pair density matrices are 25 by 25.

The targets are rho_V(t) = t Phi_5 + (1-t) B_V, with B_V = sum V_ij |ij><ij| / 50. For each target, the program constructs a positive trace-one extension whose two prescribed pair marginals agree. It computes the half trace-norm distance from the target to that marginal and independently evaluates the matching dual witness bound.

Both arrangements are checked at 171 parameter values, including phase boundaries. The global-completion sections use t = 21/41, in the open phase (9/19, 6/11).

The 315/311 counts are reproduced with exact algebraic-number arithmetic, separately from the numerical Hermitian-kernel construction. The full 56-array census and symbolic all-parameter persistence proof are supplied reference results, not rerun in their entirety here.

## What the 3D surfaces mean

Each is a chosen three-dimensional affine SECTION of its full convex optimal-extension set. All three basis directions have zero partial trace on both prescribed pair marginals. The surface radius is computed from the exact positivity formula

    r_max(u) = -1 / lambda_min(X0^(-1/2) [sum_i u_i Q_i] X0^(-1/2)).

The code evaluates eigenvalues numerically and samples this surface on a mesh. The moving point samples verified positive states at 70% of this radial boundary. Its three coordinates are changes in the expectations of three selected Hermitian collective observables. These are not positions of particles or directions in physical space.

A and B use separate seeded choices of three display directions. Their rendered shapes are not a new invariant distinction. The exact full-fiber dimensions establish the distinction independently. No holes, noncontractible topology or spacetime curvature are asserted.

## A concrete measurement

Within arrangement A, two sampled global completions have pair-state trace distances below 4e-18, but a collective two-outcome measurement has Born probabilities approximately 0.480269472 and 0.465533202. The probability difference equals their global trace distance. This is a calculation of observable consequences, not a laboratory observation or a derived intervention law.

## Global purity boundary

The density matrix T on the three original systems can be mixed. The code constructs a normalized pure extension with a 25-dimensional ancilla and verifies that reduction recovers T. This preserves global purity in that enlarged architecture, not on the original three factors alone. Partial traces here are mathematical restrictions, not physical information loss.

## Claim boundaries

This is a static quantum compatibility calculation. Equal-partner obligations, the target family and the trace-distance objective are stipulated. A state parameter and animation frame are not physical time. No force, source-to-obligation mechanism, pruning rule, gravitational dynamics or empirical validation is introduced.

This is the matched-arrangement family of v9.167, NOT the different v9.156 product-side family with slope (12 sqrt(2)-3)/40. The earlier AI-generated infographic blended those examples and was not a quantitative plot. It is not used here.

## Evidence and provenance

`output/validation.json` contains every reported check. `output/arrangement_A.npz` and `output/arrangement_B.npz` contain the actual states, curves, complete numerical hidden Hermitian bases, section directions, surfaces and sampled paths. `output/curve_data.json` supplies the numerical curve data.

The `reference/` folder contains the retrieved v9167, v9168, v9170 and v9171 exact certificate scripts and their hashes. The numerical lab is a fresh implementation of their supplied constructions. The selected exact dimension check was also rerun directly using the original v9170 code, with its result in `exact_dimension_check.json`.

No v9.172 theorem is asserted. These computations reproduce the verified v9.167–v9.171 model.
