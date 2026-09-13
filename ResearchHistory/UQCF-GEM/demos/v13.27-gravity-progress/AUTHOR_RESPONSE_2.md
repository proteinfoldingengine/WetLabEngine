# Author response to peer review round 2 — UQCF-GEM v13.27

**Scope:** Response to `REVIEW_2.md` concerning whether the first author response has actually been executed in the public artifact.  
**Claim status:** No scientific claim is upgraded by this response.

## Overall response

We accept the second referee disposition.

The first author response is satisfactory as a scientific rescoping statement, but the public artifact has **not yet been fully revised to match that statement**. In particular, the README and dashboard language still contain labels that are too suggestive relative to what the executable six-qubit model establishes.

The referee is therefore correct to distinguish:

\[
\boxed{\text{author response: satisfactory}}
\]

from

\[
\boxed{\text{artifact revision: incomplete}}
\]

The central scientific result remains the projective source-coupling obstruction. The dashboard, DeWitt-sign controls, holonomy visualization, and graph-current construction are methods context and diagnostics; they are not independent evidence for a gravity derivation.

## 1. Clarification of the homogeneity lemma

We accept the referee's correction that the weight-zero geometry statement is a **fixed-state / fixed-tangent-point statement**.

The intended theorem is not that the complete family `rho_lambda` is invariant under arbitrary rescaling of the source generator. In general,

\[
P\rightarrow cP \quad\text{at fixed }\lambda
\]

changes the state and therefore can change

\[
K_i,\quad O_{ij},\quad M_{ij}.
\]

Likewise, moving to a different value of `lambda` changes the state-point geometry.

The obstruction is instead a theorem about the **positive homogeneity of the retained selection rules once the state point and its degree-zero geometric data are fixed**.

### Fixed-state projective source-coupling lemma

Fix a faithful state \(\rho_*\) and its associated degree-zero data

\[
\mathcal G_*=(B,Z_{\rm cyc},K_*,O_*,M_*,R_*),
\]

where:

- \(B\) is the graph incidence matrix;
- \(Z_{\rm cyc}\) is a cycle-space basis;
- \(K_*,O_*,M_*\) are the state-point information metric, transport, and metric-mismatch data;
- \(R_*\) is the declared response aperture constructed from the fixed state-point data.

Let \(\xi\) denote a first-order source tangent and suppose the retained source observables are linear in that tangent:

\[
s(c\xi)=c\,s(\xi),\qquad y(c\xi)=c\,y(\xi),\qquad c>0.
\]

The minimum-norm balanced current satisfies

\[
J_0(cs)=cJ_0(s).
\]

For the conditional cycle selection

\[
a_*=\arg\min_a\left\|R_*\bigl(J_0+Z_{\rm cyc}a\bigr)-y\right\|,
\]

positive rescaling gives

\[
a_*(cs,cy)=c\,a_*(s,y),
\]

and hence

\[
J_*(cs,cy)=c\,J_*(s,y).
\]

Therefore any coupled source package \(\Sigma\) assembled only through these degree-one source quantities obeys

\[
\Sigma(c\xi)=c\,\Sigma(\xi).
\]

The frozen selection rules determine, at most,

\[
\boxed{[\Sigma]}
\]

rather than a unique nonzero magnitude.

This is the exact obstruction claim. It is **not** a claim that the entire source-state family has a scale symmetry.

## 2. Revised failure criterion

We accept the referee's point that the previous criterion was too conjunctive.

The corrected stop rule is disjunctive:

> **The target-blind source-to-geometry derivation fails if either:**
>
> 1. a no-go theorem rules out the required covariant pairing within the frozen ontology; **or**
> 2. every successful repair introduces an externally free coupling scale rather than deriving it from retained data.

Either outcome is sufficient.

The second case is operationally equivalent to inserting a coupling calibration such as \(G\). Such a calibration may still define a useful effective theory, but it is not a derivation of the absolute gravitational coupling from the frozen pre-time stack.

We will not respond to either failure mode by introducing another unconstrained “missing-law” name.

## 3. Notation

Accepted.

The cycle-space basis will be written as

\[
Z_{\rm cyc}
\]

or an equivalent non-Pauli symbol in any paper-facing revision. The Pauli operator will remain \(\sigma_z\) or \(Z_{\rm P}\). The current code-level overload is harmless but not suitable for a manuscript.

## 4. BKM dependence versus obstruction independence

Accepted.

The distinction should be explicit:

### Metric-dependent constructions

The following depend on choosing the BKM/Petz information metric used in this artifact:

\[
K_i,\qquad M_{ij},\qquad q_i=(K_i+\varepsilon I)^{-1},
\]

and all diagnostics downstream of those specific objects.

The current artifact does **not** establish that BKM is uniquely selected by the ontology.

### Metric-independent obstruction

The projective-coupling obstruction is more general. It follows from positive homogeneity of the source/current selection rules and therefore does not depend on the particular Petz metric, provided the geometric/aperture data used in the selection are degree zero at the fixed tangent point.

That separation will be retained in any methods note.

## 5. v13.28 is an audit, not a scheduled derivation

Accepted.

The next gate should no longer be phrased as “derive RGCL.”

The correct question is:

> **Does any member of a named, target-blind class of source-to-geometry pairings already available in the frozen ontology fix a nonzero coupling magnitude and tensor/coframe type?**

Each candidate must be adjudicated as one of:

\[
\boxed{\text{DERIVED}}
\]

\[
\boxed{\text{OBSTRUCTED}}
\]

\[
\boxed{\text{REQUIRES NEW AXIOM / CALIBRATION}}
\]

Candidate classes to audit include only structures already present before any Einstein residual is consulted, for example:

- BKM / Kubo-Mori dual pairings;
- retained solder/coframe pairings already defined elsewhere in the program;
- source-grade / retained-measure pairings;
- relative-entropy or recoverability response functionals;
- exact QMAR source-response tensors where a covariant dual object already exists.

A new action, volume form, or dimensionful coefficient may not be introduced and then retrospectively called derived.

## 6. Public artifact rescope

We accept that the public artifact must be changed before the first response can be called an **executed revision**.

The internal folder name may remain for Git provenance, but the reader-facing title should be changed to something close to:

> **Finite Quantum-Relational Methods Model with a Projective Source-Coupling Obstruction**

The minimum revision patch is now binding:

1. **README title and opening:** replace “Full-Stack Gravity Progress Simulation” as the scientific presentation with the methods / obstruction framing.
2. **Remove “ADM-like sector” language:** from README prose, dashboard/panel labels, and `X_UPDATE.md`. The permitted description is a **DeWitt-like quadratic-form sign diagnostic on represented `q`**.
3. **Promote the theorem:** place the fixed-state homogeneity lemma before fingerprints and numerical telemetry.
4. **Relabel the stress control:** the two hand-declared 3x3 matrices are a **toy block-underdetermination control**, not a stress-energy completion result.
5. **Add two inexpensive audits:**
   - raw determinant of the unconstrained orthogonal polar factor before enforcing `SO(3)`;
   - raw pre-clip holonomy argument \((\mathrm{Tr}H-1)/2\), including whether any values actually leave `[-1,1]` numerically and whether \(\theta=\pi\) is intrinsic or clipping-induced.

Until those changes land, the README/dashboard should be treated as stale relative to the two author-response documents.

## 7. Raw polar-determinant audit to be added

The current implementation computes an SVD

\[
C=U S V^T
\]

and first forms

\[
Q=UV^T\in O(3).
\]

If \(\det Q<0\), the final singular vector is flipped so the stored transport satisfies

\[
O\in SO(3).
\]

The missing audit is therefore straightforward and should report, over every edge and source-family frame:

- \(\det Q\) before correction;
- count and fraction with \(\det Q<0\);
- singular values of \(C\), especially near degeneracy where the polar representative may be nonunique or numerically unstable.

This will answer whether reflection removal is rare, generic, or concentrated near singular correlation tensors.

## 8. Pre-clip holonomy audit to be added

The current plotted angle uses

\[
x_C=\frac{\mathrm{Tr}H_C-1}{2},
\qquad
\theta_C=\arccos(\operatorname{clip}(x_C,-1,1)).
\]

The revision should report the raw \(x_C\) distribution before clipping:

- minimum and maximum \(x_C\);
- count outside \([-1,1]\) by more than floating-point tolerance;
- cycle-by-cycle and source-family distribution of \(\theta_C\);
- whether values equal to \(\pi\) come from \(x_C\approx-1\) intrinsically or from clipping.

Until that audit is complete, \(\max\theta_C=\pi\) is unadjudicated and should not be given geometric significance.

## 9. Controls that may wait for the next revision note

We agree these are valuable but not required before the documentation rescope:

### Nonhomogeneous sharpness control

Introduce an explicitly labeled nonhomogeneous selector, solely as a control, to demonstrate that the projective obstruction disappears once a scale-setting term is inserted. This would show that the theorem is sharp rather than merely restating normalization algebra.

Such a control must be marked **NOT ONTOLOGY-NATIVE** and must not be interpreted as a repair.

### Null / simpler-state controls

Run the same diagnostics on at least:

- a product state;
- a classical mixture of product states;
- a simple unfrustrated chain or commuting model.

The purpose is to determine which finite information-geometric/holonomy diagnostics require genuine correlations and which survive as generic properties of the extraction machinery.

### Parameter/support robustness

Audit qualitative behavior under:

- broader source support;
- \(\beta\to0\) where the state approaches maximally mixed;
- larger \(\beta\) toward a low-temperature regime;
- alternate generic coupling/modulation choices.

These tests concern robustness of the methods model. They do not change the theorem-level coupling obstruction.

## 10. Revised referee-facing status

We accept the referee table in full:

| Item | Current author position |
|---|---|
| Homogeneity lemma | **Accepted as the central result** |
| DeWitt/current/holonomy/graph relabeling | **Accepted; artifact patch still required** |
| RGCL go/no-go / free scale | **Accepted** |
| Conservative public abstract | **Accepted** |
| Claim upgrade | **None** |
| Current public artifact | **Not yet fully revised** |
| Physical gravity / Einstein closure | **Open** |

## 11. Binding public abstract

For the journal-facing artifact, the preferred abstract remains:

> We implement a reproducible six-qubit thermal family and extract BKM metrics, polar transports, discrete nonmetricity, SO(3) holonomy, and a balanced graph current without inserting Einstein or Newton equations. At a fixed state/tangent point, the retained source-selection rules are positively homogeneous, so the coupled source is determined only up to positive scale. Absolute gravitational coupling and physical Einstein closure are not obtained.

The fixed-state qualifier is added in response to this second review.

## Final response

The second review improves the work by separating three things that had still been too close together:

\[
\boxed{\text{methods laboratory}}
\]

\[
\boxed{\text{projective obstruction theorem}}
\]

\[
\boxed{\text{open physical-gravity program}}
\]

Only the second is the central scientific result of this artifact.

We therefore accept the referee's current disposition:

\[
\boxed{\text{RESPONSE ROUND 1: SATISFACTORY}}
\]

\[
\boxed{\text{PUBLIC ARTIFACT RESCOPE: STILL REQUIRED}}
\]

The next repository change should execute the five-item minimum patch above before beginning any new source-to-gravity claim work.
