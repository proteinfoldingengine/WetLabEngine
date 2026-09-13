# Claim Boundaries — UQCF-GEM v13.27 Methods / Obstruction Revision

This package is a finite quantum-relational laboratory for testing a possible route toward gravitationally relevant geometric and source-coupling structure. It does **not** claim that gravity, spacetime, ADM dynamics, or Einstein equations have been derived.

## Central result

At a fixed state/tangent point, the frozen source-selection rules are positively homogeneous. With the graph, incidence matrix, cycle basis and state-point geometry held fixed,

\[
(s,y)\mapsto(c s,c y),\qquad c>0,
\]

implies

\[
J_0\mapsto cJ_0,\qquad a_*\mapsto ca_*,\qquad J\mapsto cJ,
\]

and hence any coupled-source representative scales as

\[
\Sigma\mapsto c\Sigma.
\]

Therefore the construction selects at most the projective class `[Sigma]`; it does not determine the nonzero magnitude of `Sigma`.

This is a homogeneity theorem about the **selection rules at a fixed state/tangent point**. It is not a claim that the full state family `rho_lambda` or its geometry is invariant when `P` is arbitrarily rescaled at fixed `lambda`.

## What the executable model computes

- an exact faithful six-qubit thermal state and exact exponential source family;
- exact one- and two-qubit reduced states;
- local BKM information-response metrics;
- connected pair-correlation tensors;
- raw closest O(3) polar factors and an explicitly imposed proper-rotation projection into SO(3);
- a discrete state-dependent metric mismatch `M_ij = K_j - O_ij^T K_i O_ij`;
- finite SO(3) loop holonomy diagnostics;
- source-family finite-difference response diagnostics;
- balanced graph equations `BJ=s` and cycle-space freedom;
- a conditional response-selected graph-current witness;
- represented `q=(K+epsilon I)^-1` variables and a DeWitt-like quadratic-form sign diagnostic;
- a toy block-underdetermination control;
- the projective source-coupling obstruction.

## What is assumed rather than derived

The six vertices, eight edges, couplings, source support, beta, and plotting coordinates are inputs of the example. The graph embedding is not physical space. `lambda_source` is an exponential-family source parameter, not physical time.

The BKM metric is a declared information-geometric choice. Quantities built from `K`, including the metric mismatch and represented `q`, are therefore metric-dependent. The positive-scale obstruction does not rely on BKM uniqueness.

## Transport audit boundary

The raw closest orthogonal polar factor of each connected pair-correlation tensor is audited before enforcing proper orientation.

In the canonical 25-frame scan there are 25 × 8 = 200 edge/frame samples, and all 200 raw O(3) polar factors have determinant `-1`.

Therefore the SO(3) edge transport used by the visualization is an **explicit orientation-preserving projection choice**. It is not uniquely forced by the raw polar decomposition. Any holonomy statement in this package is conditional on that declared projection.

## Holonomy audit boundary

For each chosen SO(3) loop product `H_C`, the code records the raw argument

\[
x_C=\frac{\operatorname{Tr}H_C-1}{2}
\]

before clipping and records any clip excess.

The canonical scan contains nine `theta_C = pi` events. The maximum clip excess is `4.440892098500626e-16`, below the declared `1e-12` audit threshold. Thus the observed pi events are not adjudicated as clipping artifacts. They remain finite group-angle diagnostics, not Riemann curvature, deficit angles of a derived metric simplex, or continuum curvature density.

## Source/current boundary

The response-selected `J` is a graph-current witness satisfying `BJ=s` relative to a declared response aperture. It is **not** physical stress-energy. There is no derived Lorentzian coframe and no derived `T_{mu nu}` decomposition in this artifact.

The formerly named “spatial-stress completion” scalar is now explicitly a **toy block-underdetermination control**: two hand-declared matrix blocks can share selected lower-order projections while differing in the unobserved block. It is not a stress-energy reconstruction.

## DeWitt-like diagnostic boundary

The package evaluates

\[
D(X;q)=\operatorname{Tr}(q^{-1}X_{TF}q^{-1}X_{TF})-\frac12(\operatorname{tr}_q X)^2.
\]

The `D=-4.5` pure-trace and `D=2` traceless controls are algebraic identities / implementation checks for the declared formula in three dimensions. They are not emergent model results.

There is no map from the six vertex-local `q_i` to a spatial three-metric, no lapse, no shift, no Hamiltonian constraint, no diffeomorphism constraint, and no demonstrated ADM constraint algebra.

## What remains open

The physically important unresolved question is whether the existing ontology can produce a target-blind source→geometry pairing that fixes an appropriate source type and a non-arbitrary coupling magnitude.

`RGCL` is only a name for that missing requirement; it is not a derived law.

For the next gate, the allowed outcomes are:

- `DERIVED` — an existing, independently motivated pairing fixes the required structure without fitting Einstein/Newton targets;
- `OBSTRUCTED` — the named pairing class cannot do so;
- `REQUIRES_NEW_AXIOM` — success requires genuinely new structure.

A no-go inside the frozen ontology **or** a repair that works only by inserting a freely chosen dimensionful scale counts as failure of the target-blind derivation at that point.

## Allowed public claim

> We implement and test a concrete finite quantum-relational path from exact quantum states to information-geometric, transport, holonomy, and graph source/current structures without using Newtonian or Einstein dynamics as a selector. At a fixed state/tangent point, the source-selection rules are positively homogeneous and therefore determine at most a projective coupled-source class. The construction does not determine an absolute gravitational coupling and does not derive physical Einstein equations.

It is fair to call the path **novel and worth investigating**. It is not fair to shorten the result to “gravity derived from quantum information.”
