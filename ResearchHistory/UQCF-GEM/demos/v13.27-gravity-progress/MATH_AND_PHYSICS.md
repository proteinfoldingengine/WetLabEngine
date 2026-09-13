# Mathematics and Physics Notes — peer-review-rescoped v13.27

## 1. Finite quantum-relational model

For six qubits on a fixed relational graph,

\[
H_0=\sum_{(ij)\in E}\left(J_x X_iX_j+J_yY_iY_j+J_zZ_iZ_j\right)+\sum_i h_iZ_i,
\]

with deterministic weak edge modulation. The faithful base state is

\[
\rho_0=\frac{e^{-\beta H_0}}{\operatorname{Tr}e^{-\beta H_0}}.
\]

A source generator `P` defines

\[
\rho_\lambda=\frac{\exp(\log\rho_0+\lambda P)}{Z(\lambda)}.
\]

`lambda` indexes a source family. It is not physical time. The graph, edge set, couplings, source support and plotting embedding are inputs of the example, not derived spacetime.

The code also checks the exact reparameterization

\[
(\lambda,P)\mapsto(\lambda/a,aP),
\]

which leaves `lambda P` and therefore `rho_lambda` unchanged.

## 2. BKM information-response metric

For a faithful one-site state with eigenvalues `p_m` and Pauli generators `A_a`, the implementation uses the logarithmic mean

\[
L(p_m,p_n)=\frac{p_m-p_n}{\log p_m-\log p_n},\qquad L(p,p)=p,
\]

and the Kubo-Mori covariance

\[
K_{ab}=\Re\sum_{mn}L(p_m,p_n)(A_a)_{mn}(A_b)_{nm}
-\langle A_a\rangle\langle A_b\rangle.
\]

This gives a positive local information-response metric `K_i` on the sampled faithful stratum. BKM is a declared information-geometric choice, not a uniqueness result; downstream objects depending on `K` are metric-dependent.

## 3. Pair correlation and polar transport

For an edge `i-j`,

\[
C_{ij}^{ab}=\langle\sigma_a\otimes\sigma_b\rangle_{ij}
-\langle\sigma_a\rangle_i\langle\sigma_b\rangle_j.
\]

The raw nearest orthogonal factor from the SVD is

\[
Q_{ij}=UV^T\in O(3).
\]

The executable model then imposes a proper-rotation convention: if `det(Q_ij)<0`, the last singular vector is flipped before constructing

\[
O_{ij}\in SO(3).
\]

### Polar-determinant audit

The canonical 25-frame scan contains `25 x 8 = 200` edge/frame factors. All 200 unconstrained raw polar factors have

\[
\det Q_{ij}=-1.
\]

Thus the `SO(3)` transport is an explicit orientation-preserving projection in this example, not a rare numerical repair and not a uniquely derived consequence of the raw polar decomposition. All loop-holonomy statements below are conditional on this declared projection.

## 4. Metric mismatch and SO(3) loop holonomy

The finite state-dependent metric mismatch is

\[
M_{ij}=K_j-O_{ij}^{T}K_iO_{ij}.
\]

For a closed graph cycle `C`,

\[
H_C=\prod_{(ij)\in C}O_{ij}.
\]

Before clipping, the code now records

\[
x_C=\frac{\operatorname{Tr}H_C-1}{2}.
\]

The plotted group angle is

\[
\theta_C=\cos^{-1}[\operatorname{clip}(x_C,-1,1)].
\]

### Pre-clip audit

The canonical run contains eight `theta_C=pi` events. The maximum excess outside `[-1,1]` is approximately

\[
2.22\times10^{-16},
\]

well below the declared `10^{-12}` audit threshold. The pi events are therefore adjudicated as genuine within numerical tolerance of the chosen SO(3) construction, not as meaningful clipping artifacts.

These are finite group-angle diagnostics. The code does not identify them with Riemann curvature, sectional curvature, a Regge deficit angle, or a continuum curvature density.

## 5. Source-family response diagnostics

Finite differences across the source family estimate

\[
\partial_\lambda M_{ij},\qquad \partial_\lambda O_{ij}.
\]

The combined response-jet norm is a diagnostic with respect to `lambda_source`; it is not a time derivative and presently has no universal physical normalization.

## 6. Balanced graph source/current witness

An oriented graph incidence matrix `B` gives

\[
BJ=s,\qquad \sum_i s_i=0.
\]

With cycle basis `Z_cyc`,

\[
J=J_0+Z_{\rm cyc}a,\qquad BZ_{\rm cyc}=0.
\]

The demo resolves cycle coefficients relative to a declared weighted response aperture. This is a conditional graph-current witness. It is not a derived `T_{\mu\nu}` and no Lorentzian coframe is derived in this artifact.

## 7. Central homogeneity lemma / projective obstruction

At a fixed state/tangent point, hold the graph, incidence matrix, cycle basis and state-point geometry fixed. The selection rule uses

\[
J_0=B^+s,
\]

and, schematically,

\[
a_* = \arg\min_a\left\|R(J_0+Z_{\rm cyc}a)-y\right\|.
\]

Under positive rescaling

\[
(s,y)\mapsto(c s,c y),\qquad c>0,
\]

linearity and homogeneity give

\[
J_0\mapsto cJ_0,\qquad a_*\mapsto ca_*,\qquad J\mapsto cJ.
\]

Thus any coupled-source representative constructed from these degree-one quantities obeys

\[
\Sigma\mapsto c\Sigma.
\]

The frozen selection rules therefore determine at most the ray

\[
[\Sigma]=\{c\Sigma:c>0\},
\]

not its nonzero magnitude.

This is the theorem-level result of v13.27. The machine-level direction-drift number is only an implementation check of the algebra.

The lemma does **not** claim that changing `P` at fixed `lambda` leaves `rho_lambda`, `K`, `O`, or `M` invariant. It concerns homogeneity of the source-selection rules at a fixed state/tangent point.

## 8. Represented q and DeWitt-like quadratic-form diagnostic

The demo defines

\[
A_i=K_i+\epsilon I,\qquad q_i=A_i^{-1}.
\]

For symmetric `X`,

\[
\operatorname{tr}_qX=\operatorname{Tr}(q^{-1}X),\qquad
X_{TF}=X-\frac{\operatorname{tr}_qX}{3}q,
\]

and evaluates

\[
D(X;q)=\operatorname{Tr}(q^{-1}X_{TF}q^{-1}X_{TF})
-\frac12(\operatorname{tr}_qX)^2.
\]

For the declared controls in three dimensions,

- `X=q` gives `D=-4.5`;
- `X=sqrt(q) diag(1,-1,0) sqrt(q)` gives `D=2`.

These values are algebraic identities / implementation controls for the chosen quadratic form. They are not emergent dynamics. The model contains no map from the six `q_i` to a spatial three-metric, no lapse, no shift, no Hamiltonian constraint, no diffeomorphism constraint, and no ADM constraint algebra.

The path-dependent scalar `D(q,dq/dlambda)` is retained only as a finite diagnostic on represented variables.

## 9. Toy block-underdetermination control

The code compares two hand-declared `3 x 3` matrix blocks and records their Frobenius separation. The canonical distance is approximately

\[
0.4135214626.
\]

This is deliberately a **toy block-underdetermination control**. It demonstrates an algebraic possibility of differing unobserved blocks; it is not a reconstruction or nonuniqueness theorem for physical stress-energy.

## 10. Executed canonical envelope

For the canonical 25-frame scan, the stable headline results include:

- minimum global-state eigenvalue: `~3.7185e-05`;
- minimum local BKM eigenvalue: `~0.567313`;
- source-balance residual: machine precision;
- declared cycle-response aperture: full rank on cycle space;
- raw polar reflections: `200 / 200` samples;
- pi holonomy events: `8`;
- holonomy clip events above `1e-12`: `0`;
- maximum clip excess: `~2.22e-16`;
- projective coupled-source status: `RAY_ONLY__MAGNITUDE_NOT_DERIVED`;
- physical Einstein closure: `OPEN`.

The authoritative portable fingerprint and archival raw telemetry hash are frozen in `EXPECTED_RESULTS.json` after cross-run certification.

## 11. What the path establishes — and what it does not

The scientifically interesting object is the **path architecture**:

\[
\text{finite quantum states}
\to \text{information geometry}
\to \text{declared relational transport}
\to \text{metric mismatch / loop diagnostics}
\to \text{balanced source-current structure}
\to \text{projective coupling obstruction}.
\]

No Newtonian kernel and no Einstein equation is used as a selector.

That makes the construction a concrete, falsifiable route worth investigating. It does not make it a gravity derivation.

The next lawful question is whether an existing ontology-native pairing can fix the source-to-geometry map and magnitude without target fitting. The allowed outcomes are `DERIVED`, `OBSTRUCTED`, or `REQUIRES_NEW_AXIOM`. A no-go **or** a repair that succeeds only by inserting a freely chosen dimensionful scale counts as failure of the target-blind derivation at that point.
