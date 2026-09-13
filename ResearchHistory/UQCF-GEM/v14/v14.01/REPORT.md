# UQCF-GEM v14.01 — Canonical Source-Dependent Global Admissibility Gate

**Date:** 2026-09-12

## Adjudication

The frozen pre-pruning/global-consistency architecture does **not** select a unique nonzero source-dependent admissibility deformation within the audited construction class.

The gate outcome is:

`NONUNIQUE`

and this source→higher-incidence/admissibility branch is stopped pending either:

1. one explicit, independently motivated source→higher-incidence/admissibility axiom; or
2. one independently calibrated physical cross-domain observable that selects the deformation.

No Newtonian law, Einstein/ADM residual, physical time/entropy primitive, fitted coupling, or downstream gravity target was used.

This is not a theorem that no deeper nonlinear global law can generate source-dependent admissibility. It is a canonicality obstruction for the present frozen architecture and the audited incidence/state-weighted/PSD-positivity class.

## 1. Source action is not law deformation

The current global-compatibility architecture can be written schematically as

\[
\mathcal A_G(b)=\{X_{\rm aff}(b)+H:\;H\in\ker O_G,\;X_{\rm aff}(b)+H\succeq0\}.
\]

Changing a state or visible datum \(b\) while keeping the observation/compatibility map \(O_G\), its hidden kernel, and the positivity rule fixed moves the realization within a fixed admissibility architecture. It does not, by itself, derive a source-dependent law

\[
\mathcal A_G\to\mathcal A_G(s).
\]

A genuine law-level deformation requires the source to enter the defining higher-incidence/constraint structure through some map of the schematic type

\[
\eta:S\to P.
\]

v14.01 asks whether the frozen architecture selects such an \(\eta\) canonically.

## 2. Incidence-Only Cycle-Defect No-Go

Let \(B\) be the oriented node-edge incidence matrix of a connected graph, and define the orthogonal cycle-space projector

\[
P_{\rm cyc}=I-B^T(BB^T)^+B.
\]

The canonical incidence map sends a node source to the exact edge 1-cochain \(B^Ts\). Since

\[
\operatorname{im}B^T=(\ker B)^\perp,
\]

the cycle projection vanishes exactly:

\[
\boxed{P_{\rm cyc}B^T=0.}
\]

Therefore graph incidence alone cannot turn a node source into a nonzero global cycle defect.

On the deterministic 5-node / 7-edge control, the executed Frobenius leakage was

`1.245468636882555e-15`.

This is numerical confirmation of the exact linear-algebra identity, not the basis of the theorem.

## 3. Relational weighting creates nonzero defects — but not canonically

A frozen edge scalar \(\chi_e\) can be fed through a positive scalar functional to produce

\[
W_f=\operatorname{diag}(f(\chi_e)),
\]

and hence a candidate map

\[
\eta_f=P_{\rm cyc}W_fB^TC,
\]

where

\[
C=I-\frac{11^T}{n}
\]

centers arbitrary node coordinates into the balanced source subspace.

The audit tested three positive functionals of the same edge scalar:

\[
f_1(x)=1+x,
\qquad
f_2(x)=e^x,
\qquad
f_3(x)=1+x^2.
\]

All three produce nonzero operators:

- `linear_positive`: Frobenius norm `0.9317680326490423`;
- `exponential_positive`: Frobenius norm `1.1006383303926504`;
- `quadratic_positive`: Frobenius norm `0.3273241321687114`.

Their flattened operator family has

`rank = 3`.

Across 256 balanced source trials, all `768` candidate outputs were nonzero. The largest separation between normalized candidate directions was

`0.9960669843187823`.

Thus this is not merely an overall normalization ambiguity. Different equally admissible scalar functional choices can send the same source toward substantially different cycle-space defect directions.

These three functionals are witnesses of nonuniqueness. They are not asserted to be physical laws.

## 4. Covariance and source linearity do not remove the ambiguity

The audit applied random vertex permutations together with signed edge permutation/orientation transformations. Under

\[
B' = VBE^T,
\qquad
W'=EWE^T,
\qquad
s'=Vs,
\]

the candidate operators transform covariantly.

Maximum relative covariance error:

`1.3482796731097804e-14`.

Under source scales

`[0.2, 0.5, 2.0, 5.0, 11.0]`,

the maximum relative source-linearity error was

`7.993866358511362e-16`.

So relabeling covariance and degree-one source behavior are compatible with the entire inequivalent family. They do not select one member.

## 5. Global positivity does not rescue uniqueness

A possible loophole is that the positive cone might itself select one deformation.

### 5.1 Faithful interior

A positive-definite center lies in the interior of the PSD cone. Therefore every finite collection of bounded Hermitian directions remains positive for a sufficiently small common perturbation radius.

For the control embedding used here, all 768 candidate perturbations remained positive at one common

`epsilon = 0.1443693458628246`,

with minimum eigenvalue margin

`0.75`.

The 7→`Sym(4)` embedding used for this test is only an injective control representation. It is not a physical coframe, stress tensor, or spacetime map.

The result establishes the relevant geometric fact: faithful positivity is a feasibility condition with an open neighborhood and cannot distinguish among these bounded directions locally.

### 5.2 Boundary

At the simple boundary point

\[
X_b=\operatorname{diag}(0,1,1,1),
\]

first-order PSD feasibility along a symmetric perturbation \(\Delta\) requires

\[
e_0^T\Delta e_0\ge0.
\]

`Sym(4)` has dimension 10. The equality lineality space

\[
e_0^T\Delta e_0=0
\]

has dimension

`9`.

Thus the boundary supplies an inequality / normal-cone condition, not a unique source deformation.

The frozen classification is therefore:

`INEQUALITY_FILTER_NOT_CANONICAL_SOURCE_MAP`.

Positivity can reject directions. It does not, by itself in this audited construction, generate the unique source→higher-incidence law that is missing.

## 6. State-Weighted Admissibility Canonicality Obstruction

Combine the previous results.

1. The purely canonical incidence construction gives zero global cycle defect:

\[
P_{\rm cyc}B^T=0.
\]

2. Nonzero source-dependent cycle defects can be generated after introducing a relational weighting operator \(W\).

3. Covariance and source linearity permit multiple inequivalent \(W_f\) constructions.

4. Faithful positivity accepts all sufficiently small bounded candidates; a representative PSD boundary supplies an inequality cone rather than a unique source direction.

Therefore, within the audited class,

\[
\boxed{
\text{nonzero source-dependent admissibility deformations exist, but the frozen rules do not select one canonically.}
}
\]

This is why the correct adjudication is `NONUNIQUE`, not `NO_NATIVE_DEFORMATION`.

The missing content is now upstream and precise: some additional principle must select the source→higher-incidence / admissibility coupling, rather than merely act on a state inside the already-fixed admissible arena.

## 7. Additional coefficient ambiguity

Even after choosing one functional \(f\), the family

\[
\eta\mapsto c\eta,
\qquad c>0,
\]

preserves source linearity and covariance.

No frozen rule in this gate selects that coefficient either.

This resembles the scale issue found downstream in v13, but it is a logically different question: here the ambiguity is already present at the upstream source→global-defect law itself.

## 8. Added-law positive control

To prove the gate can recognize uniqueness when it is actually supplied, the positive control explicitly declares

- the weighting functional `exponential_positive`; and
- coefficient `2.7`.

The reconstructed declared map agrees exactly in the deterministic control:

`positive_control_reconstruction_error = 0.0`.

This is labeled

`ADDED_LAW_POSITIVE_CONTROL`.

It demonstrates sufficiency of an explicit selector. It is not evidence that the frozen ontology derives that selector.

## 9. Relation to the v13 branch stop

v14.01 does not reopen the downstream v13.28 source→geometry coupling branch.

v13.28 showed that the frozen downstream geometry/source machinery does not derive an absolute coupling magnitude. v14.01 moved upstream and tested whether global relational consistency already contained a canonical source-dependent admissibility deformation that could supply genuinely new input.

Within the audited native class, it does not select one.

What survives is the finite quantum/global-compatibility architecture, hidden-completion structure, source-current balance, the projective coupled-source result, and the broader research possibility that a deeper global law exists outside the present frozen class.

## Status

- source action under fixed admissibility architecture: **DISTINGUISHED FROM LAW DEFORMATION**
- incidence-only source→cycle defect: **ZERO EXACTLY**
- nonzero relationally weighted source→cycle defects: **EXIST**
- covariance/source linearity as selector: **NO**
- positivity as selector: **NO IN THE AUDITED INTERIOR/BOUNDARY CONTROLS**
- canonical nonzero source→higher-incidence map: **NOT DERIVED**
- v14.01 adjudication: **NONUNIQUE**
- branch status: **STOPPED PENDING NEW SOURCE→HIGHER-INCIDENCE AXIOM OR INDEPENDENT CALIBRATION**
- physical gravity claim: **NONE**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major source→higher-incidence canonicality obstruction**. It sharpens the research frontier: if the program is to obtain universal source-dependent global admissibility, the selecting principle is not supplied by incidence, covariance, source linearity, or positivity alone in the class audited here.
