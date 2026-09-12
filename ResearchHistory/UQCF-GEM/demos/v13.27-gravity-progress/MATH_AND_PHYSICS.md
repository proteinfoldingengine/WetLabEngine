# Mathematics and Physics Notes

## 1. Finite pre-time quantum model

For six qubits on a fixed relational graph,

\[
H_0=\sum_{(ij)\in E}\left(J_x X_iX_j+J_yY_iY_j+J_zZ_iZ_j\right)+\sum_i h_iZ_i,
\]

with deterministic weak edge modulation. The faithful base state is

\[
\rho_0=\frac{e^{-\beta H_0}}{\mathrm{Tr}\,e^{-\beta H_0}}.
\]

A source generator `P` defines the PGRL/ETL family

\[
\rho_\lambda=\frac{\exp(\log\rho_0+\lambda P)}{Z(\lambda)}.
\]

`lambda` indexes a family of admissible source perturbations. It is not physical time.

The code explicitly checks the parameterization gauge

\[
(\lambda,P)\mapsto(\lambda/a,aP),
\]

under which `lambda P` and therefore `rho_lambda` are unchanged.

## 2. BKM information-response metric

For a faithful one-node state with eigenvalues `p_m` and Pauli generators `A_a`, the implementation uses the logarithmic mean

\[
L(p_m,p_n)=\frac{p_m-p_n}{\log p_m-\log p_n},\qquad L(p,p)=p,
\]

and the Kubo-Mori covariance

\[
K_{ab}=\Re\sum_{mn}L(p_m,p_n)(A_a)_{mn}(A_b)_{nm}
-\langle A_a\rangle\langle A_b\rangle.
\]

This produces a positive local information-response metric `K_i` on the finite faithful stratum.

## 3. Pair correlation and polar transport

For an edge `i-j`,

\[
C_{ij}^{ab}=\langle\sigma_a\otimes\sigma_b\rangle_{ij}
-\langle\sigma_a\rangle_i\langle\sigma_b\rangle_j.
\]

The nearest proper orthogonal factor from the SVD of `C_ij` defines

\[
O_{ij}\in SO(3).
\]

This is the finite relational transport used by the visualization.

## 4. Nonmetricity and retained holonomy

The discrete metric-compatibility defect is

\[
M_{ij}=K_j-O_{ij}^{T}K_iO_{ij}.
\]

For a closed relational cycle `C`,

\[
H_C=\prod_{(ij)\in C}O_{ij},
\]

and the plotted holonomy angle is

\[
\theta_C=\cos^{-1}\!\left[\mathrm{clip}\left(\frac{\mathrm{Tr}H_C-1}{2},-1,1\right)\right].
\]

This is a finite SO(3) holonomy proxy. The script never equates it with continuum spacetime curvature.

## 5. QMAR response diagnostic

Finite differences across the source family estimate

\[
\partial_\lambda M_{ij},\qquad \partial_\lambda O_{ij}.
\]

The telemetry reports a combined norm of these retained response jets. Because the derivative is with respect to `lambda_source`, it is a source-response derivative and not a time derivative.

## 6. Retained source/current

An oriented graph incidence matrix `B` gives

\[
BJ=s,\qquad \sum_i s_i=0.
\]

The minimum-norm solution is not unique when the graph has cycles:

\[
J=J_0+Za,\qquad BZ=0.
\]

The demo includes a conditional response-selection witness that resolves the cycle coefficients relative to a declared edge-response aperture. This is intentionally labeled **CONDITIONAL** because the aperture is not yet a physical stress-energy law.

## 7. Projective coupled-source boundary

Positive scaling preserves the retained structural constraints:

\[
(s,J)\mapsto(c s,cJ).
\]

Normalized source/current direction therefore remains fixed while magnitude changes. This illustrates the v13.27 theorem that the frozen retained stack selects at most a projective coupled-source ray `[Sigma]`, not its nonzero magnitude.

## 8. Represented ADM-like variable and DeWitt sign

The demo declares the finite information metric as a directional-access proxy

\[
A_i=K_i+\epsilon I,
\qquad q_i=A_i^{-1}.
\]

For a symmetric source-response tensor `X`, with

\[
\mathrm{tr}_qX=\mathrm{Tr}(q^{-1}X),\qquad
X_{TF}=X-\frac{\mathrm{tr}_qX}{3}q,
\]

the diagnostic is

\[
D(X;q)=\mathrm{Tr}(q^{-1}X_{TF}q^{-1}X_{TF})
-\frac12(\mathrm{tr}_qX)^2.
\]

The executed controls give

- pure trace: `D=-4.5`;
- traceless control: `D=2.0`.

That reproduces the negative trace direction characteristic of the represented DeWitt sector. It is a structural correspondence result, not a physical ADM evolution equation.

## 9. Executed numerical envelope

Default 25-frame run:

- portable scientific fingerprint: `6f2830c47a877676f6ff4ad028769bb285d00f9194f33035c85dd785b3e9f5b6`;
- reference raw telemetry SHA-256: `e994538f3e04a06270b17b66c21ee29dc07730c5ceaf0805ba412f754624f945` (diagnostic only; machine-epsilon LAPACK/SVD drift is intentionally excluded from portable certification);
- minimum global-state eigenvalue: `3.7185106924494124e-05`;
- minimum local BKM eigenvalue: `0.5673128649814877`;
- maximum source-balance residual: `4.611102534756203e-16`;
- maximum positive-scale projective-ray drift: `3.380886602644082e-16`;
- PGRL reparameterization error: `9.55170005517049e-16`;
- cycle-space response rank deficit: `0` in the declared witness;
- spatial-stress completion witness distance: `0.4135214625627066`.

The last item demonstrates that fixed energy/current projections need not determine the full spatial-stress block.

## 10. What would move the simulation closer to physical gravity?

The next lawful bridge is not to tune these diagnostics until an Einstein residual looks small. It is to derive RGCL independently: a source-to-coframe or equivalent variational pairing that fixes the tensor type and coupling magnitude from retained data alone. Only then should an Einstein/ADM residual be evaluated as a heldout consequence.
