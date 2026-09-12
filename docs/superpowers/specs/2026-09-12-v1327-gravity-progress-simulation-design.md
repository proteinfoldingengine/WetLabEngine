# v13.27 Gravity Progress Simulation Design

## Purpose

Build a deterministic, research-grade Python simulation that visualizes the current UQCF-GEM / Retained Atlas Path-A progress from pre-time quantum relations toward gravity-like geometry without inserting Newton's law or the Einstein equations as dynamics.

The package is a demonstration and integration harness for already established finite-scale ingredients and currently open boundaries. It must visually distinguish derived mathematics, conditional constructions, controlled correspondence, and missing physical laws.

## Scientific scope

The simulation represents a finite relational quantum network with no fundamental spacetime or physical-time variable. Animation frames sweep a source-family parameter `lambda_source`; this parameter is explicitly **not physical time**.

```text
Genesis-rooted finite quantum relation network
-> PGRL/ETL source family
-> exact reduced one- and two-node states
-> local BKM response metrics K_i
-> connected pair correlations C_ij
-> polar transports O_ij
-> discrete nonmetricity M_ij
-> loop holonomy / curvature proxy
-> source-current balance B J = s
-> conditional response-selected current witness
-> represented q=A^-1 and DeWitt-sign ADM-like sector
-> projective coupled-source ray [Sigma]
-> explicit v13.27 RGCL gap before physical Einstein closure
```

No step may claim that visualization coordinates are physical space, that the source-family parameter is time, that loop holonomy is already Riemann curvature of spacetime, or that an Einstein field equation has been derived.

## Architecture

The package lives under `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/`.

- `uqcf_demo/linalg.py`: Hermitian matrix functions, partial trace, Pauli operators, SO(3) utilities.
- `uqcf_demo/quantum.py`: finite qubit Hamiltonian, Genesis-rooted base state, PGRL source family, reduced density matrices, BKM covariance metrics, connected correlations.
- `uqcf_demo/geometry.py`: polar transports, nonmetricity defects, cycle holonomy, curvature proxies, finite-difference QMAR jets.
- `uqcf_demo/source_current.py`: incidence matrix, balanced retained source, cycle-space decomposition, conditional response-selected current witness, projective source-ray controls.
- `uqcf_demo/adm.py`: represented `q=A^-1` construction and DeWitt trace-sign diagnostics; no physical-time interpretation.
- `uqcf_demo/ledger.py`: scientific claim ledger with categories `DERIVED`, `CONDITIONAL`, `CONTROLLED_CORRESPONDENCE`, `MISSING_LAW`.
- `uqcf_demo/render.py`: four-panel static/animated visualization.
- `run_simulation.py`: CLI orchestration and artifact export.

## Quantum model

Use `N=6` qubits by default so the full `2^N x 2^N` density matrix remains exact and tractable.

`H0 = sum_(i,j in E) Jx X_i X_j + Jy Y_i Y_j + Jz Z_i Z_j + sum_i h_i Z_i`.

The Genesis root appears only as a deterministic source/provenance anchor for the local bias profile; it does not define a spacetime origin.

`rho0 = exp(-beta H0) / Tr exp(-beta H0)`.

`rho(lambda) = exp(log(rho0) + lambda P) / Z(lambda)`

with `P` a deterministic two-lobe local Pauli source centered on two selected graph nodes. The code computes the state by Hermitian eigendecomposition and never approximates with an inserted force law.

## Local information geometry

For each one-qubit reduced state `rho_i`, compute the BKM covariance metric for Pauli generators using the logarithmic mean

`L(a,b) = (a-b)/(log a-log b)`, with `L(a,a)=a`.

`K_ab = Re sum_mn L(lambda_m,lambda_n) (A_a)_mn (A_b)_nm - <A_a><A_b>`.

Each `K_i` must be symmetric positive semidefinite to numerical tolerance; a small declared regularizer is allowed only for inversion in the represented ADM diagnostic.

## Relational transport and curvature proxy

For each edge `(i,j)` calculate

`C_ij[a,b] = <sigma_a tensor sigma_b> - <sigma_a>_i <sigma_b>_j`.

Take its closest proper orthogonal polar factor `O_ij in SO(3)` by SVD with determinant correction.

`M_ij = K_j - O_ij^T K_i O_ij`.

For each predeclared graph cycle,

`H_C = product_(i,j in C) O_ij`

and

`theta_C = arccos(clamp((Tr H_C - 1)/2,-1,1))`.

This is a finite retained holonomy diagnostic, not certified spacetime curvature.

## Source-current layer

Build oriented incidence matrix `B`. Derive a balanced node-source vector from the source-family response of a declared local observable and remove its graph mean so `sum_i s_i = 0`.

Solve `B J = s` and expose the cycle-space ambiguity using a null basis `Z` of `B`.

A conditional response-selection witness may select one current by minimizing mismatch to independently computed edge-response telemetry. It must be labeled conditional and must not be used as a physical stress-energy law.

The projective ray `[J]` and `[Sigma]` controls explicitly demonstrate invariance under positive common scaling.

## Represented ADM-like diagnostic

Use `A_i = K_i + eps I` and define `q_i = A_i^-1`. Compute finite-difference source-family derivatives `dq_i/dlambda`.

For symmetric `X`, report

`D(X;q) = ||X_TF||_q^2 - (1/2) (tr_q X)^2`.

Construct a pure-trace control and verify `D<0`, while a traceless control has `D>=0`. This demonstrates the represented negative trace direction only; it is not an ADM dynamical closure proof.

## Visualization

Generate a deterministic 1920x1080 four-panel animation:

1. **Pre-time quantum relation network** — abstract graph embedding; node size from source response; edge width from correlation strength.
2. **Retained geometry** — same abstract embedding lifted in `z` by curvature/nonmetricity score; loop curvature overlays.
3. **Source/current and projective coupling** — currents plus a live sweep illustrating `[Sigma]` invariance and unresolved coupling magnitude.
4. **ADM-like correspondence ledger** — DeWitt diagnostic, telemetry curves, and live claim-status table.

Every frame displays `source-family parameter (not physical time)`.

Exports:

- `outputs/gravity_progress.mp4` when ffmpeg is available;
- `outputs/gravity_progress.gif` fallback/companion;
- `outputs/final_frame.png`;
- `outputs/telemetry.csv`;
- `outputs/summary.json`.

Binary outputs are generated by the script and are not required to be committed.

## Claim ledger

**DERIVED / exact finite construction:** faithful finite source family, exact reductions, BKM metrics, connected correlations, polar transports, nonmetricity defects, loop holonomy, QMAR finite-difference response diagnostics.

**CONDITIONAL:** response-selected retained current witness, represented `q=A^-1`, finite metric-affine-to-ADM-like diagnostic.

**CONTROLLED CORRESPONDENCE:** previously retained weak ADM/Einstein correspondence envelope may be shown only as an external overlay and never as a selector.

**MISSING LAW:** RGCL source-to-coframe/geometric coupling magnitude, full spatial-stress completion, ontology-native continuum refinement/QRSL, physical Einstein closure.

## Tests and reproducibility

Tests verify density-matrix validity, partial trace, BKM symmetry/PSD, proper orthogonal transports, source-current balance, cycle basis, projective invariance, PGRL reparameterization, DeWitt trace-sign controls, and deterministic telemetry hashing.

Default runtime target: under 90 seconds for the full 6-qubit telemetry sweep on a normal laptop, excluding video encoding.

## Communication artifacts

Include `MATH_AND_PHYSICS.md`, `CLAIM_BOUNDARIES.md`, and `X_UPDATE.md`. The X copy may say the simulation shows a quantum-relational route generating metric-affine and ADM-like structure, but must explicitly say the gravitational coupling law and physical Einstein closure remain open.
