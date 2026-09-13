# Peer review: UQCF-GEM v13.27 gravity-progress simulation

**Manuscript / artifact.** Executable 6-qubit pipeline plus `CLAIM_BOUNDARIES.md`, `MATH_AND_PHYSICS.md`, `CHECKER.py`, `EXPECTED_RESULTS.json`  
**Reviewer stance.** Methods and claims only. I reran the packaged tests and 25-frame checker; fingerprints matched. This is not a review of the whole UQCF-GEM program, only of what this demo actually establishes.

## Recommendation

**Revise and rescope.**  
The artifact is a legitimate finite-model laboratory with unusually good claim hygiene. It is not a gravity paper and should not be framed as “gravity progress” except internally. The publishable core is a negative / obstruction result: the frozen operations are homogeneous, so they select a projective source ray and cannot select a coupling magnitude. That result is interesting if restated in standard language and separated from definitional numerical controls.

## Summary of the work

A fixed 6-qubit XYZ Hamiltonian on an 8-edge graph generates a faithful thermal state \(\rho_0\). A one-parameter family \(\rho_\lambda \propto \exp(\log\rho_0+\lambda P)\) is scanned. From one- and two-site reductions the code builds:

- local BKM metrics \(K_i\)
- pair-correlation tensors and nearest \(\mathrm{SO}(3)\) factors \(O_{ij}\)
- discrete nonmetricity \(M_{ij}=K_j-O_{ij}^T K_i O_{ij}\)
- loop holonomy \(H_C=\prod O_{ij}\)
- graph balance \(BJ=s\) with a response-weighted cycle fix
- regularized \(q=(K+\varepsilon I)^{-1}\) and a DeWitt-sign diagnostic
- a ledger that marks RGCL and Einstein closure as missing

No Newtonian kernel and no Einstein residual is used as a selector. That part is correctly implemented.

## Major comments

### 1. The central result is conceptual, not numerical

v13.27’s actual theorem is:

> Every retained constraint used to build \((s,J)\) and the first-order response is homogeneous of degree one under \(\Sigma\to c\Sigma\), \(c>0\). Therefore the stack determines at most a ray \([\Sigma]\).

That is true, and it is the right place to stop. It is also elementary once the operations are written down. The reported projective drift \(3.38\times 10^{-16}\) does not add evidence. `projective_scale_control` only checks that normalizing \(c\mathbf{x}\) recovers the direction of \(\mathbf{x}\). Please move that number to an implementation appendix and state the obstruction as a lemma about the axiom set.

### 2. Two advertised “ADM / DeWitt controls” are identities

For the implemented diagnostic

\[
D(X;q)=\mathrm{Tr}(q^{-1}X_{\mathrm{TF}}q^{-1}X_{\mathrm{TF}})-\tfrac12(\mathrm{tr}_q X)^2
\]

in three dimensions:

- \(X=q\Rightarrow D=-4.5\)
- \(X=\sqrt{q}\,\mathrm{diag}(1,-1,0)\sqrt{q}\Rightarrow D=2\)

These values appear for any invertible \(q\). They certify the formula, not an emergent DeWitt supermetric or ADM constraint algebra. The only model-dependent DeWitt number in the run is the path average \(D(q,\partial_\lambda q)\approx-0.129\). That is a plotted scalar on an information-metric inverse. It is not ADM evolution: there is no lapse, shift, diffeomorphism constraint, or Hamiltonian constraint.

**Request.** Relabel the panel “sign structure of a DeWitt-like quadratic form on represented \(q\).” Do not call it an ADM-like sector without writing the constraint functions and showing they close, or fail to close, on this model.

### 3. Geometry is assigned to a pre-drawn graph

Node coordinates are a regular 6-gon. Edges are hardcoded. \(\lambda\) is an exponential-family parameter. The code itself says the embedding is not physical space and \(\lambda\) is not time. Good. Then the narrative chain “pre-time quantum relations \(\to\) geometry \(\to\) ADM-like structure” overreaches. What is derived is state-dependent tensors on a fixed abstract graph. Please distinguish:

- **derived:** \(K_i(\rho_\lambda),\ O_{ij}(\rho_\lambda),\ M_{ij},\ H_C,\ (s,J)\)
- **assumed:** vertex set, edge set, plotting embedding, source support on qubits 0 and 3, \(\beta\), couplings

Without a limit in which the graph or the embedding is selected by the state, this is not spacetime emergence.

### 4. Holonomy is an \(\mathrm{SO}(3)\) proxy, and \(\max\theta_C=\pi\) needs explanation

\[
\theta_C=\cos^{-1}\mathrm{clip}\left(\frac{\mathrm{Tr}H_C-1}{2}\right)
\]

is the angle of an \(\mathrm{SO}(3)\) element. It is not a Riemann component, sectional curvature, or deficit angle of a metric simplex. The executed maximum is exactly \(\pi\). That can mean a genuine \(180^\circ\) transport or saturation of the clip. Either way it is a large discrete defect on a 3-cycle of a tiny graph. If the paper wants “curvature,” it needs a density, a continuum comparison, or at least a demonstration that \(\theta_C\) scales as area rather than as a raw group angle.

### 5. The selected current is not \(T_{\mu\nu}\)

\[
BJ=s
\]

plus

\[
J=J_0+Za,\qquad a=\arg\min\lVert R(J_0+Za)-y\rVert
\]

is a weighted Kirchhoff lift. \(R=\mathrm{diag}(1+|M_e|)\) is a modeling choice. The ledger correctly marks this conditional. The surrounding text still slides toward “source/current flow” as if a conservation law on spacetime had been derived. It has not. There is no Lorentzian coframe, no \(T^{0\mu}\) vs \(T^{ij}\) split derived from the quantum state, and the spatial-stress completion distance \(0.414\) is explicit evidence that \(\rho,j\)-like projections do not determine a unique stress block.

### 6. RGCL is a name for a missing axiom, not a result

After v13.27, “derive RGCL next” is the only remaining gravitational move. A referee will ask whether RGCL is:

- a uniqueness theorem inside the frozen ontology,
- a new variational principle,
- or an extra scaleful input (essentially \(G\)).

If it is the third, the program should say so and stop claiming a target-blind bridge. If it is the first, state the candidate pairing now (BKM pairing, solder, volume form, relative entropy response) and show it either fixes a magnitude or fails. Do not defer the only load-bearing law to v13.28 while titling v13.27 as gravity progress.

### 7. Novelty is overstated by private vocabulary

BKM metrics, polar transports, discrete nonmetricity, holonomy products, incidence currents, and DeWitt signature are standard objects. The combination in one fingerprinted 6-qubit script is uncommon. The objects are not. A journal version should cite Petz/BKM, metric-affine gravity, discrete connections, and the information-geometry-to-gravity literature, then say what is left after those citations.

## Minor comments

1. `seed: 1327` is stored in config but the default model is deterministic. Drop or use it.
2. Fingerprint ignores \(\varepsilon\)-residuals but includes `source_scale`. Good. Also include graph edges in any public hash you treat as scientific (you already do).
3. `max_qmar_jet_norm \approx 16` has no units and no baseline. Normalize by \(\lVert M\rVert\) or \(\lVert O-I\rVert\) so the number is comparable across \(\lambda\).
4. Edge modulation \(1+0.07\cos(0.9(e+1))\) and source operator coefficients look tuned for a faithful, well-conditioned path. State the selection rule or freeze them as “one generic example.”
5. Tests are fast and well aimed. Add one test that a non-homogeneous rule would change the ray magnitude if introduced, so the obstruction is shown to be sharp.
6. The four-panel figure is a dashboard, not evidence. Keep it in a demo; do not let it stand in for a theorem.

## What I accept as shown

On this frozen example:

- \(\rho_\lambda\) stays faithful (\(\lambda_{\min}(\rho)\sim 3.7\times10^{-5}\)).
- Local BKM metrics stay positive-definite on the scanned path.
- \(BJ=s\) holds at \(\sim10^{-16}\).
- The declared response aperture has full rank on cycle space.
- PGRL reparameterization \((\lambda,P)\mapsto(\lambda/a,aP)\) closes numerically.
- The packaged claim ledger is consistent with the code.
- Einstein closure is not obtained.

That is enough for a methods / negative-result note. It is not enough for a gravity derivation.

## Clarifying questions

Please answer these in a revision. Short answers are better than new jargon.

### Ontology and scope

1. What, precisely, is a “retained” structure? Which objects are frozen axioms, which are derived, and which are visualization?
2. What does “pre-time” exclude? Is there any ordered structure in the demo other than the scan parameter \(\lambda\)?
3. Is the 6-node graph part of the ontology or an example? If the edge set were changed, which theorems survive?

### Information geometry

4. Why BKM rather than another Petz metric? Is any later claim metric-dependent?
5. Are the local \(K_i\) computed on one-site reductions only? If yes, why is inter-site information not part of the local metric?
6. For pair state \(\rho_{ij}\), is \(C_{ij}^{ab}\) the connected Bloch tensor, and is the polar factor unique when two singular values coincide?
7. Does \(O_{ij}\in\mathrm{SO}(3)\) rather than \(\mathrm{O}(3)\) discard physically relevant reflections? How often does the closest orthogonal factor have \(\det=-1\)?

### Nonmetricity and holonomy

8. In continuum MAG, nonmetricity is \(\nabla g\). Why is \(K_j-O^T K_i O\) the correct discretization rather than a finite difference of \(K\) along an embedded edge?
9. Please report the distribution of \(\theta_C\) over cycles and \(\lambda\), not only the max. Is \(\pi\) generic or a clip artifact?
10. Can you exhibit a state family with \(M_{ij}=0\) but \(H_C\neq I\), and the reverse, so torsion-like and nonmetricity-like defects are separated?

### Sources and currents

11. Why is \(s\) defined as the mean-subtracted \(\partial_\lambda\langle Z_i\rangle\)? What privileges \(Z\) over a BKM-gradient or energy-density proxy?
12. The response weights \(R=I+\mathrm{diag}(|M_e|)\) are a choice. Which theorems depend on that choice?
13. What is the exact definition of the “spatial-stress completion” tensors that sit a Frobenius distance \(0.414\) apart? Same \(\rho,j\) projections with respect to which coframe?
14. You report that a supplied calibration \(z=q^T\Sigma\) recovers \(c\). Is there any candidate \(z\) built only from \(\{K_i,O_{ij}\}\) that you have already ruled out?

### ADM / DeWitt

15. What is the map from \(\{q_i\}\) on six vertices to a 3-metric on a spatial slice? Without that map, what does “ADM-like” mean?
16. Will you agree that \(D=-4.5\) and \(D=2\) are not model results?
17. Is there a discrete diffeomorphism action on the graph under which \(D\) transforms as a DeWitt supermetric scalar?

### Coupling and RGCL

18. Write the strongest homogeneity lemma as a displayed statement: list every constraint, the scaling weight of each field, and the conclusion \([\Sigma]\) only.
19. Is \(\kappa\) allowed to be a state-dependent functional, or must it be a universal constant? Those are different RGCL targets.
20. If v13.28 finds no pairing inside the frozen stack, do you treat RGCL as a new axiom? If so, how is that different from inserting \(G\)?
21. What would count as a failure of the program rather than a new missing-law name?

### Validation

22. Besides self-hashing, what third-party observable would falsify the pipeline (not the ledger text)?
23. Have you run a control with a product state, a classical mixture of product states, or a 1D unfrustrated chain, to show which geometric diagnostics disappear?
24. How much of the qualitative dashboard survives if \(P\) is supported on all sites, or if \(\beta\to0\) or \(\beta\to\infty\)?

## Suggested public abstract

> We implement a reproducible 6-qubit thermal family and extract BKM metrics, polar transports, discrete nonmetricity, \(\mathrm{SO}(3)\) holonomy, and a balanced graph current without inserting Einstein or Newton equations. On this axiom set the coupled source is determined only up to positive scale. Absolute gravitational coupling and physical Einstein closure are not obtained.

That is accurate. “Gravity-progress simulation” is not, except as an internal milestone name.

---

*Archived in the repository on 2026-09-12. Markdown normalization only; substantive review content preserved.*
