# Author response to peer review — UQCF-GEM v13.27

**Date:** 2026-09-12  
**Scope:** Response to `REVIEW.md` for the executable six-qubit artifact only. This response does not upgrade any scientific claim.

## Overall response

We accept the recommendation to **revise and rescope**.

The reviewer has correctly identified the strongest publishable result of this artifact: the finite construction is useful as a methods laboratory, while the actual theorem-level conclusion is a **homogeneity / projective-coupling obstruction**, not a derivation of gravity.

For a journal-facing revision we will not use “gravity progress” as the scientific title. The existing folder and internal milestone name will remain for provenance, but the public scientific framing should be closer to:

> **A finite quantum-relational methods model with a projective source-coupling obstruction.**

We also accept that several labels in the demo are too suggestive relative to what the executable model actually establishes. In particular:

- the fixed six-node graph and its plotting embedding are assumed, not derived spacetime;
- the `lambda_source` coordinate is a source-family parameter, not time;
- the loop angle is an SO(3) holonomy diagnostic, not a Riemann curvature scalar;
- the selected graph current is not stress-energy;
- the `D=-4.5` and `D=2` controls are algebraic identities / implementation checks, not emergent model results;
- the current artifact has no lapse, shift, Hamiltonian constraint, diffeomorphism constraint, or constraint-algebra closure;
- therefore the phrase “ADM-like sector” should not be used for this demo without substantial additional structure;
- RGCL is currently a **name for the missing source-to-geometry law**, not a derived law.

The strongest current result should be stated before any numerical dashboard:

## Homogeneity lemma / projective obstruction

Let the frozen graph, incidence matrix, cycle basis and state-dependent geometry be degree-zero objects under a positive rescaling of the source tangent:

\[
B\mapsto B,\qquad Z\mapsto Z,\qquad K\mapsto K,\qquad O\mapsto O,\qquad M\mapsto M,\qquad R(M)\mapsto R(M).
\]

Let the first-order source observables have weight one,

\[
s\mapsto c s,\qquad y\mapsto c y,\qquad c>0,
\]

where in the packaged witness

\[
s=\Pi_0\,\partial_\lambda\langle Z_i\rangle,
\]

and `y` is the edge-response tangent used by the declared response aperture. The minimum-norm current

\[
J_0=B^+s
\]

has weight one. With

\[
J=J_0+Za_*,
\qquad
 a_* = \arg\min_a\lVert R(J_0+Za)-y\rVert,
\]

the least-squares problem rescales homogeneously, so

\[
a_*\mapsto c a_*,\qquad J\mapsto cJ.
\]

Therefore the frozen balance and response-selection relations are invariant in form under

\[
(s,y,J)\mapsto c(s,y,J).
\]

Any degree-one coupled-source object built only from those homogeneous data inherits

\[
\Sigma\mapsto c\Sigma.
\]

Hence, **without an independent nonhomogeneous calibration or a separately derived scale-bearing law, these constraints determine at most the projective class**

\[
\boxed{[\Sigma]}
\]

and not its nonzero magnitude.

The numerical `projective_scale_control` is only an implementation check of this algebra and should be moved out of the evidentiary foreground.

## Response to major comments

### 1. Central result is conceptual, not numerical — ACCEPT

Agreed. The projective-drift value near machine precision is not independent evidence for the obstruction. It verifies the implementation of positive rescaling. The revised presentation should lead with the homogeneity lemma above and place the numerical drift in an implementation / regression appendix.

### 2. DeWitt controls are identities — ACCEPT

Agreed. In the implemented three-dimensional quadratic form, the two controls were deliberately chosen so that `X=q` gives `-4.5` and the constructed traceless test gives `2` for any positive invertible `q`. They test the code path and sign convention.

They are **not evidence that a DeWitt supermetric, ADM phase space, or ADM constraint algebra emerged from the quantum model**.

The model-dependent plotted quantity is the scalar diagnostic evaluated on the represented path, schematically

\[
D(q,\partial_\lambda q),
\]

and even that should be described only as a **DeWitt-like quadratic-form sign diagnostic on a represented information-metric inverse**. We accept the requested relabeling and will remove “ADM-like sector” from the demo-facing scientific claim unless actual constraint functions and their closure are introduced and tested.

### 3. Geometry is assigned to a pre-drawn graph — ACCEPT

Agreed. The executable model derives **state-dependent tensors on a frozen abstract graph**. It does not derive the graph, its dimension, its plotting embedding, or spacetime.

The revision will separate:

**Frozen inputs / modeling choices**

- six tensor factors;
- eight graph edges;
- XYZ Hamiltonian coefficients and edge modulation;
- `beta`;
- source generator and support;
- Pauli frame;
- BKM metric choice;
- proper-SO(3) polar convention;
- selected cycles;
- response aperture;
- represented `q=(K+epsilon I)^-1` map.

**Derived from the state family given those choices**

- one- and two-site reductions;
- local BKM matrices;
- connected pair-correlation tensors;
- proper polar transports;
- edge metric-compatibility defects;
- loop holonomies;
- source-family response tangents;
- balanced source proxy and conditional graph current;
- represented quadratic-form diagnostic.

**Visualization only**

- regular-hexagon node positions;
- vertical lifts / warping used in the dashboard;
- colors, line widths and panel layout.

No spacetime-emergence claim follows from this artifact.

### 4. SO(3) holonomy and the pi maximum — ACCEPT

Agreed. The loop observable is a raw SO(3) group angle. It is not a Riemann tensor component, sectional curvature, Regge deficit angle, or curvature density.

The exact `pi` maximum is currently insufficiently diagnosed. The implementation clips the arccos argument to `[-1,1]` for numerical safety, but the artifact does not currently report the unclipped argument, the distribution of angles, singular-value conditioning of each transport, or whether the `pi` value is robust across perturbations.

A revision should add those audits before using the word “curvature” except as “holonomy / curvature proxy.” A continuum claim would additionally require a scaling object such as loop area and a controlled refinement limit, which this demo does not possess.

### 5. Selected current is not stress-energy — ACCEPT

Agreed. The current is a graph current satisfying a Kirchhoff-type balance law with a conditional cycle-space selection rule. It is not `T_munu` and should not be narrated as a spacetime conservation law.

The reviewer also identifies an overstatement in the current “spatial-stress completion” control. The code presently places two different symmetric 3x3 matrices side by side and reports their Frobenius distance. It **does not** construct a Lorentzian coframe or prove that they are two completions of the same derived `(rho,j)` projections. That control is only an algebraic toy illustrating underdetermination of an unobserved symmetric block. The revision should relabel it accordingly or remove it until a coframe and projection map exist.

### 6. RGCL is a missing axiom/law name — ACCEPT, with a go/no-go rule

Agreed. RGCL is not itself a result. The result is the obstruction that motivates asking whether such a law can be derived.

The next gate must distinguish three outcomes explicitly:

1. **Derived:** a unique or sufficiently constrained source-to-geometric pairing follows from already-frozen objects and fixes a nonzero magnitude without using the target field equation.
2. **Obstructed:** the frozen ontology admits no such pairing, or admits a scale family that cannot be broken internally.
3. **New axiom / scale input:** the bridge is added rather than derived.

If the third outcome is merely a free dimensionful constant multiplying the source, with no independent origin or prediction, then at this level it is operationally equivalent to inserting a gravitational coupling such as `G`. We will label it that way rather than call it a target-blind derivation.

### 7. Standard objects and novelty — ACCEPT

Agreed. BKM/Kubo-Mori metrics, monotone information metrics, polar decomposition, discrete transport/holonomy, graph incidence currents, metric-affine nonmetricity, and DeWitt-type quadratic forms are standard mathematical constructions. The novelty claim, if any, must concern a specific theorem, obstruction, composition, or prediction—not renamed standard objects.

A journal revision needs standard citations for Petz/BKM information geometry, discrete connections/holonomy, metric-affine gravity, DeWitt superspace, and information-theoretic approaches to geometry/gravity before stating what is actually new here.

## Response to minor comments

1. **Unused seed:** accepted. The default model is deterministic; the seed should be removed unless stochastic controls are added.
2. **Fingerprint graph content:** agreed. Graph edges are already part of the scientific fingerprint and should remain so.
3. **QMAR jet norm:** accepted. The raw norm near 16 is scale- and convention-dependent and should not be advertised without normalization/baseline.
4. **Hamiltonian/source coefficients:** accepted. They should be described as one frozen generic example unless a selection rule is supplied. No universality claim should depend on those numerical choices without robustness sweeps.
5. **Sharpness control:** accepted. A nonhomogeneous positive control should be added to demonstrate precisely what kind of added law can break the scale symmetry.
6. **Dashboard:** accepted. It is a visualization / diagnostic dashboard, not theorem evidence.

# Answers to clarifying questions

## Ontology and scope

### 1. What is a “retained” structure?

In this demo, “retained” should be read operationally, not metaphysically: an object computed from the frozen state family and then carried forward to later finite constructions without using an Einstein/Newton target to choose it.

- **Frozen axioms/inputs:** graph, Hilbert-factorization, Hamiltonian/source-family definition, beta, Pauli frame, BKM choice, polar convention, cycles, response aperture and represented-q rule.
- **Derived:** reductions, `K_i`, `C_ij`, `O_ij`, `M_ij`, loop products, response tangents, balanced source proxy, conditional current and the represented quadratic-form scalar.
- **Visualization:** regular-hexagon coordinates and graphical deformation.

The word should not imply that all of these are ontology-native or unique.

### 2. What does “pre-time” exclude?

It excludes a physical clock variable, Hamiltonian time evolution interpreted as spacetime time, lapse, shift, causal foliation, or a derived temporal metric in this artifact.

The only ordered continuous coordinate in the executable demo is `lambda`, the exponential-family source parameter. The sequence of frames is numerical ordering of that scan. It is **not** claimed to be emergent time.

### 3. Is the six-node graph ontology or example? Which results survive changing it?

For this artifact it is a **frozen example**, not a derived ontological graph.

For another connected finite graph, the following algebraic structures survive under their stated regularity assumptions:

- local BKM construction for faithful one-site states;
- incidence balance `BJ=s` for balanced `s`;
- cycle-space decomposition `J=J0+Za`;
- the homogeneity/projective obstruction for a fixed degree-zero response aperture;
- state-dependent correlation/polar/metric-compatibility constructions on whatever edges are supplied.

Numerical holonomies, cycle dimensions, response rank, conditioning and all dashboard morphology are graph-dependent.

## Information geometry

### 4. Why BKM rather than another Petz metric? Is anything metric-dependent?

BKM was chosen because the source family is log/exponential (`rho_lambda proportional to exp(log rho0 + lambda P)`), and the Kubo-Mori/Bogoliubov pairing is the natural Hessian/tangent metric associated with such exponential families.

That is a motivation, not a uniqueness theorem. The downstream `K`, `M`, represented `q`, and therefore the numerical geometric dashboard are metric-dependent. The graph-balance algebra and the abstract homogeneity obstruction do not require BKM specifically, provided the replacement geometry enters the selection aperture with scaling weight zero.

### 5. Are `K_i` one-site only? Why exclude inter-site information?

Yes. `K_i` is computed from the one-site reduced density matrix using the local Pauli basis. Inter-site information enters separately through the connected pair tensor `C_ij` and its polar factor.

This separation is a modeling choice, not a theorem. A revision should test pair-conditioned or larger-patch information metrics rather than imply that one-site BKM is uniquely local geometry.

### 6. Is `C_ij` the connected Bloch tensor, and is the polar factor unique?

Yes. The code computes

\[
C_{ij}^{ab}=\langle\sigma_a\otimes\sigma_b\rangle-\langle\sigma_a\rangle\langle\sigma_b\rangle.
\]

For nonsingular `C`, the orthogonal polar factor is unique even if an SVD representation contains degenerate singular subspaces; the product defining the polar factor is invariant. If `C` becomes rank-deficient, the polar action on the nullspace is not unique. The current demo does not report rank/singular-gap conditioning, so that audit should be added.

The proper-rotation correction introduces an additional convention when the closest unconstrained orthogonal factor has negative determinant.

### 7. Does restricting to SO(3) discard reflections? How often is raw det negative?

Yes. The implementation explicitly forces a proper rotation: after `U V^T`, if the determinant is negative it flips the last singular vector. Thus reflections are discarded by construction.

The present telemetry does **not** report how often the unconstrained closest orthogonal factor has `det=-1`. We therefore cannot claim that the SO(3) restriction is innocuous. A revision should log that frequency and compare O(3) and SO(3) results.

## Nonmetricity and holonomy

### 8. Why `K_j-O^T K_i O`?

Because the plotting embedding is not physical, the construction was not intended as an embedded finite difference. It is a discrete **transport-compatibility defect**: transport the metric at node `i` into node `j`’s frame and compare it with `K_j`.

That is a standard graph-connection style comparison. We agree it should not be presented as *the* discretization of continuum MAG nonmetricity without a discrete-to-continuum derivation. “Discrete metric-compatibility defect” is the safer primary name.

### 9. What is the theta distribution, and is pi a clip artifact?

The packaged artifact currently reports frame/cycle angles in telemetry but the manuscript-style summary foregrounds only the maximum. It does not yet provide the requested distributional analysis or raw pre-clip arccos argument.

Therefore the correct current answer is: **unadjudicated**. `pi` may correspond to an actual near-180-degree SO(3) product or may reflect saturation at the clip boundary. The revision should report all cycle/frame values, pre-clip arguments and conditioning before interpreting it.

### 10. Can metric mismatch and holonomy be separated?

Yes algebraically, and the demo should add explicit controls.

- `M_ij=0` with `H_C != I` is possible when the local metrics are invariant under the edge transports (for example, equal isotropic metrics) while the product of transports around a loop is nontrivial.
- `H_C=I` with `M_ij != 0` is possible when the edge transports multiply to identity but local metrics differ across edges.

Those examples show that transport holonomy and metric compatibility are logically distinct. The current default state family does not constitute a systematic separation study.

## Sources and currents

### 11. Why mean-subtracted `d<Z>/dlambda`?

The default source generator is dominated by local `Z` terms on qubits 0 and 3, so local `Z` response is a simple source-sensitive observable. Mean subtraction projects it onto the balanced subspace required by graph incidence (`sum_i s_i=0`).

Nothing in the current ontology proves that `Z` is the physical source variable. It should be called a **balanced source proxy**. BKM-gradient, modular-response, or energy-density-like source definitions are legitimate alternatives and should be compared.

### 12. Which results depend on `R=diag(1+|M_e|)`?

The chosen cycle component of `J`, its response residual, and any visualization based on that selected `J` depend on the aperture.

The following do not depend on that particular weight choice:

- `BJ=s` for the selected current;
- the dimension of the graph cycle space;
- the existence of the affine family `J0+Za`;
- the homogeneity/projective obstruction for any fixed or degree-zero aperture `R` with a linear least-squares selection rule.

Thus the current-selection *witness* is aperture-dependent; the scale obstruction is broader.

### 13. What exactly are the spatial-stress completion tensors?

The reviewer is correct to press this point. In the current code they are simply two hand-declared symmetric 3x3 matrices whose Frobenius separation is reported. The demo does not construct a Lorentzian coframe, a 4-tensor, or common derived `(rho,j)` projections from which these are proven alternative completions.

Therefore the existing wording is too strong. The number `0.4135...` is only a **toy symmetric-block nonuniqueness control**. It should not be cited as evidence about physical stress completion until a coframe/projection map exists.

### 14. Has any `z` built only from `{K_i,O_ij}` been exhaustively ruled out?

No. The current gates rule out scale selection by the frozen homogeneous constraints and several specific normalization routes; they do **not** constitute an exhaustive theorem over every nonlinear functional of `{K_i,O_ij}`.

Testing whether a natural geometric pairing or scalar can supply an independent calibration is exactly the substantive content required of the next gate. Any candidate must be defined before comparison with an Einstein residual.

## ADM / DeWitt

### 15. What maps `{q_i}` to a spatial 3-metric?

No such map exists in this demo. Each `q_i=(K_i+epsilon I)^-1` is a 3x3 inverse local information-response matrix at one graph vertex. The six matrices are not assembled into a metric field on a spatial slice.

Therefore, for this artifact, “ADM-like” should be replaced by **represented DeWitt-like quadratic-form diagnostic**. Any stronger ADM claim requires a slice, constraint variables and their algebra.

### 16. Are `D=-4.5` and `D=2` model results?

No. We agree. They are algebraic controls that hold for the deliberately chosen test tensors for any positive invertible `q`. They verify implementation/sign convention only.

### 17. Is there a discrete diffeomorphism action under which `D` has the required transformation law?

No. The current demo defines no such discrete diffeomorphism group/action and proves no corresponding covariance of `D` as a DeWitt supermetric scalar.

## Coupling and RGCL

### 18. Strongest homogeneity lemma

The displayed lemma at the top of this response is the strongest claim we currently defend for the demo. Scaling weights are:

| Object | Weight under positive source-tangent scaling |
| --- | ---: |
| `B`, `Z` | 0 |
| state-point geometry `K`, `O`, `M` | 0 |
| fixed/degree-zero response aperture `R(M)` | 0 |
| source tangent `s` | 1 |
| edge-response tangent `y` | 1 |
| minimum-norm current `J0` | 1 |
| cycle coefficient `a*` | 1 |
| selected current `J` | 1 |
| degree-one coupled source `Sigma` | 1 |

Conclusion: the homogeneous constraints determine only `[Sigma]` unless an independent scale-bearing rule is supplied.

### 19. May kappa be state-dependent?

Those are different research targets and should not be conflated.

For a gravity-like universal coupling claim, our default target is a universal constant or a universal scale determined by deeper theory, not an arbitrary state-by-state fitting functional. A state-dependent `kappa[rho]` would require separate covariance, locality/nonlocality, composition and universality principles; otherwise it can trivially absorb the missing scale.

The next gate should freeze this distinction before testing candidates.

### 20. If no internal pairing exists, is a new RGCL axiom different from inserting G?

If the new axiom is only “multiply the source by a free dimensionful constant chosen externally,” then **no**: operationally, at this level, that is equivalent to inserting a gravitational coupling constant. We would label the bridge as an added calibration, not an emergent result.

A genuinely different outcome would require the new law to be independently motivated and to produce additional nontrivial, falsifiable structure beyond choosing a scale.

### 21. What counts as failure rather than another missing-law name?

We adopt the following stop criteria.

The target-blind gravity-derivation program fails within the frozen ontology if:

1. a no-go theorem shows no nonzero covariant source-to-geometric pairing can be selected from the frozen objects; **and**
2. every successful repair requires a target-calibrated or freely inserted coupling scale.

More broadly, a candidate bridge fails if it cannot survive independent covariance/composition/refinement controls or if its claimed physical predictions require fitting the same observable used to define the bridge.

We should not respond to such a failure by merely renaming the missing object.

## Validation

### 22. What third-party observable currently falsifies this pipeline?

None yet. This artifact is an internal mathematical / computational consistency model, not a calibrated physical theory. Its present falsifiers are mathematical and reproducibility based, not astronomical or laboratory observables.

A future physical-gravity claim must produce at least one held-out observable from an independently fixed bridge. Until then the absence of a third-party observable is a limitation that should be stated explicitly.

### 23. Product, classical-mixture and 1D-chain controls?

Not in the packaged v13.27 demo. They should be added.

In particular, a product-state control is important because connected pair correlations vanish; the polar transport then becomes rank-deficient/nonunique, exposing the domain on which the transport construction is meaningful. A separable classically correlated mixture and a simple unfrustrated chain would help distinguish generic correlation structure from genuinely nontrivial loop diagnostics.

### 24. Robustness to all-site `P` and beta limits?

Not yet systematically tested in this package.

Expected mathematical domain behavior already suggests useful controls:

- as `beta -> 0`, the state approaches maximal mixing, connected correlations tend to vanish, and the correlation-derived polar transport can become ill-defined/nonunique;
- as `beta` becomes large, near-purity can reduce faithfulness and make BKM/logarithmic-mean numerics ill-conditioned;
- all-site `P` changes the source-response pattern and must be tested to determine which dashboard features are specific to the chosen two-site support.

Those are robustness questions, not settled results.

# Revision commitments before journal-style use

Before presenting this artifact as a methods / negative-result note, we will treat the following as required revisions:

1. lead with the homogeneity lemma, not projective-drift numerics;
2. rescope the title away from a gravity-derivation implication;
3. replace “ADM-like sector” with “DeWitt-like quadratic-form diagnostic” for this demo;
4. explicitly tabulate frozen inputs, derived quantities and visualization-only choices;
5. call `M_ij` a discrete metric-compatibility defect unless/until a continuum MAG limit is established;
6. add polar rank/singular-gap and raw determinant diagnostics;
7. add the full loop-angle distribution and pre-clip audit;
8. add independent holonomy-vs-metric-compatibility controls;
9. relabel `s` as a balanced source proxy and `J` as a conditional graph current;
10. remove or relabel the current stress-completion number as a toy block-under\-determination control;
11. add a nonhomogeneous positive control showing how scale symmetry can actually be broken;
12. add product-state, separable-mixture and 1D-chain controls;
13. add source-support and beta robustness sweeps;
14. normalize or de-emphasize the raw QMAR jet norm;
15. add standard literature citations and sharply delimit any novelty claim;
16. freeze v13.28 as a **go/no-go source-to-geometry pairing test**, not as permission to introduce another undefined bridge name.

# Accepted public abstract

We accept the reviewer’s proposed abstract, with only minor formatting changes:

> We implement a reproducible six-qubit thermal family and extract BKM metrics, polar transports, discrete metric-compatibility defects, SO(3) holonomy, and a balanced graph current without inserting Einstein or Newton equations. On this axiom set the coupled source is determined only up to positive scale. Absolute gravitational coupling and physical Einstein closure are not obtained.

# Status after review

\[
\boxed{\text{artifact reproducibility: preserved}}
\]

\[
\boxed{\text{projective homogeneity obstruction: preserved and promoted to central result}}
\]

\[
\boxed{\text{ADM / emergent-spacetime language: rescope required}}
\]

\[
\boxed{\text{RGCL: still missing; not itself a result}}
\]

\[
\boxed{\text{physical Einstein closure: open}}
\]

No broad scientific breakthrough is claimed by this review response. The review improves the claim boundary and sharpens the next falsifiable gate.
