# CONTINUUM_LIMIT.md

# Continuum Limit
## Candidate derivation program for the GR limit of the affine GEM Bridge framework

## Status
**Blueprint for closure. Not yet closed.**

This file has received the Option A scalar-density tightening pass, the tightened Bianchi lemma, and a runnable verifier scaffold. Seam 3 is now theorem-shaped with:
- a concrete candidate memory action,
- an explicit candidate memory stress tensor,
- controlled total conservation via a transfer current \(Q_\nu\),
- and a structural verifier for weak-memory decoupling.

This file still does **not** claim that a controlled continuum GR limit has been derived from the microscopic law.

The unresolved closure targets remain:
1. derive the coefficient functions \(Z_R(\chi)\), \(V(R_{\mathrm{eff}};\chi,\varepsilon^*)\), and \(\lambda_{\mathrm{int}}(\chi)\) from the microscopic pruning law;
2. construct a covariant coarse-graining map;
3. derive the emergent metric and compatible connection;
4. prove Bianchi-compatible conservation from the microscopic/discrete level;
5. verify that the scalar-density class is forced, rather than merely admissible.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal of this file

The package already contains:
- a microscopic collapse/pruning law candidate,
- a conditional affine bridge theorem,
- and a candidate fixed-point/loading reduction for the bridge coefficient \(\chi\).

Those results are still discrete/coarse-grained unless they can be embedded into a continuum effective theory.

The purpose of this file is to answer the next question:

> can the microscopic bridge framework be represented by a discrete action whose coarse-grained limit yields an effective covariant field theory, and does that theory reduce to Einstein gravity in the appropriate weak-memory regime?

This is the seam between:
- a discrete bridge program,
and
- a candidate continuum theory.

---

# 2. What must be shown

For the continuum-limit seam to count as closed, the package must ultimately supply:

1. an explicit discrete action or equivalent variational object,
2. an admissible memory-action term \(S_{\mathrm{mem}}\),
3. a controlled coarse-graining procedure,
4. an emergent metric/connection construction,
5. effective field equations,
6. a clean weak-memory/GR-decoupling limit,
7. explicit conservation/Bianchi consistency,
8. and a microscopic derivation of the continuum memory coefficients.

Anything less than that should be described honestly as:
- a continuum-limit candidate,
- a variational ansatz,
- or a partially organized derivation program.

---

# 3. Discrete action target

## Definition 1
The discrete action is assumed to have the form
\[
S_{\mathrm{disc}}
=
S_{\mathrm{geom}} + S_{\mathrm{mat}} + S_{\mathrm{mem}}.
\]

Here:
- \(S_{\mathrm{geom}}\) is the discrete geometric sector,
- \(S_{\mathrm{mat}}\) is the matter sector,
- \(S_{\mathrm{mem}}\) is the retained-memory / bridge sector.

## Assumption 1
The microscopic collapse/pruning law is not itself automatically the action. Rather, the action is an effective discrete variational object whose stationary/coarse-grained behavior should reproduce the same admissible bridge dynamics at leading order.

## Derivation target A
Specify the exact relation between:
- the microscopic update law,
- the bridge operator,
- the retained-memory recursion,
- and the discrete action.

Without this, the action remains a motivated effective object rather than a derived variational principle.

---

# 4. Candidate geometric sector

## Definition 2
The discrete geometric sector is a Regge-like or causal-set-like curvature functional:
\[
S_{\mathrm{geom}} = \sum_{e\in\mathcal C} \mathcal L_{\mathrm{geom}}(e),
\]
or, more explicitly in Regge-style notation,
\[
S_{\mathrm{geom}} \sim \sum_h A_h\,\delta_h,
\]
where:
- \(h\) labels hinges/simplices/discrete curvature supports,
- \(A_h\) is the corresponding measure element,
- \(\delta_h\) is the deficit-angle or equivalent curvature measure.

## Assumption 2
The continuum limit of \(S_{\mathrm{geom}}\) alone is required to reproduce the Einstein-Hilbert action or its standard discrete approximation:
\[
S_{\mathrm{EH}}
=
\frac{1}{16\pi G}\int d^4x\,\sqrt{-g}\,R.
\]

This is the baseline. If the geometric sector itself cannot approach Einstein-Hilbert structure, the memory sector cannot rescue the continuum limit.

## Failure condition 1
If no admissible \(S_{\mathrm{geom}}\) with a known or controlled GR limit can be identified, the continuum program fails before memory is even added.

---

# 5. Candidate matter sector

## Definition 3
The matter sector is assumed to take a standard discrete covariant form:
\[
S_{\mathrm{mat}} = \sum_{e\in\mathcal C} \mathcal L_{\mathrm{mat}}(\phi_e,G_e),
\]
where \(\phi_e\) denotes discrete matter variables on the causal lattice.

## Assumption 3
The coarse-grained limit of \(S_{\mathrm{mat}}\) should reproduce the standard matter action
\[
S_{\mathrm{mat}}^{\mathrm{cont}}
=
\int d^4x\,\sqrt{-g}\,\mathcal L_{\mathrm{mat}}(\phi,g).
\]

This assumption is not special to the bridge theory; it is the normal consistency requirement for any discrete-to-continuum model.

## Derivation target B
Write the exact matter sector for at least one test class:
- scalar field,
- dust/fluid sector,
- or baryonic effective matter source.

---

# 6. Candidate memory sector

This is the central seam of the file.

## Definition 4
The retained-memory sector enters the discrete action as
\[
S_{\mathrm{mem}}
=
\sum_{e\in\mathcal C}
\mathcal L_{\mathrm{mem}}
(R_e,G_e,\phi_e;\chi,\varepsilon^*,\alpha_s,\alpha_f,\dots).
\]

It must encode:
- the existence of a retained-memory degree of freedom,
- the bridge coefficient \(\chi\),
- the threshold structure associated with seam activation,
- and the slow/fast memory decomposition at effective level.

## Assumption 4
At leading order, the memory sector is not allowed to destroy:
- background covariance,
- weak-memory decoupling,
- or the existence of a well-defined stress-energy interpretation.

This is the admissibility requirement for \(S_{\mathrm{mem}}\).

---

# 7. Admissible classes of memory action

This file organizes the main candidates.

## Class A: scalar-density memory action
\[
S_{\mathrm{mem}}^{(A)}
=
\int d^4x\,\sqrt{-g}\,
\mathcal F(R_{\mathrm{eff}},\nabla R_{\mathrm{eff}},\chi,\varepsilon^*,\dots).
\]

Interpretation:
- the memory sector behaves like an effective scalar or scalar-density field,
- possibly with a self-interaction or thresholded potential.

### Advantage
Simplest path to a covariant effective stress-energy tensor.

### Risk
May be too weak to encode the bridge structure if memory is inherently nonlocal.

## Class B: stress-like local memory action
\[
S_{\mathrm{mem}}^{(B)}
=
\int d^4x\,\sqrt{-g}\,
\mathcal F_{\mu\nu}(R_{\mathrm{eff}},g,\chi,\dots)\,g^{\mu\nu}.
\]

Interpretation:
- the memory sector behaves like an effective local stress correction,
- coupled directly to the metric sector.

### Advantage
Natural route to a tensorial \(T_{\mu\nu}^{\mathrm{mem}}\).

### Risk
Can easily overfit or introduce extra tensor structure not justified by the microscopic law.

## Class C: nonlocal kernel memory action
\[
S_{\mathrm{mem}}^{(C)}
=
\int d^4x\,d^4y\,
\sqrt{-g(x)}\sqrt{-g(y)}
K(x,y;\chi,\varepsilon^*,\dots)
\mathcal O_R(x)\mathcal O_R(y).
\]

Interpretation:
- retained memory is fundamentally nonlocal,
- and the continuum memory sector retains this via a kernel.

### Advantage
Most faithful to retained coherence and long-memory influence.

### Risk
Much harder to control:
- covariance,
- locality limit,
- causality,
- and Bianchi consistency are all nontrivial.

## Derivation target C
Determine which of Classes A–C, or which hybrid variant, is actually compatible with:
- the operator theorem,
- the fixed-point role of \(\chi\),
- and the microscopic pruning law.

At present this remains open.

---

# 8. Admissibility conditions for the memory sector

The memory action is admissible only if it satisfies all of the following.

## C1. Background equivariance / covariance
The effective memory action must not break the symmetries preserved by the isotropic background unless the breaking is already justified by explicit state content.

## C2. Weak-memory decoupling
There must exist a regime in which
\[
S_{\mathrm{mem}}\to0
\quad\text{or}\quad
\delta S_{\mathrm{mem}}
\text{ becomes higher order},
\]
so that Einstein gravity is recovered at leading order.

## C3. Variational well-definedness
The metric variation of \(S_{\mathrm{mem}}\) must exist and define a meaningful effective stress-energy contribution:
\[
T_{\mu\nu}^{\mathrm{mem}}
:=
-\frac{2}{\sqrt{-g}}
\frac{\delta S_{\mathrm{mem}}}{\delta g^{\mu\nu}}.
\]

## C4. No uncontrolled extra degrees of freedom
The memory sector must not secretly introduce unconstrained propagating fields that were not present in the microscopic law or bridge theorem.

## C5. Controlled total conservation
If the memory sector exchanges energy-momentum with matter, the exchange must be covariant, finite, and suppressed or controlled in the weak-memory regime:
\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mat}} = Q_\nu,
\qquad
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}} = -Q_\nu.
\]

## Failure condition 2
If \(S_{\mathrm{mem}}\) cannot satisfy C1–C5 simultaneously, the continuum-limit program fails.

---

# 9. Coarse-graining map

## Definition 5
Let \(\mathcal C\) be the discrete causal lattice. A coarse-graining map is a rule
\[
\mathcal G_{\mathrm{cg}}:
(\{G_e\},\{R_e\},\{\phi_e\})
\longmapsto
(g_{\mu\nu},R_{\mathrm{eff}},\phi_{\mathrm{eff}}),
\]
sending discrete variables to continuum effective fields.

## Assumption 5
The coarse-graining map is:
- symmetry-compatible,
- approximately local in the weak-memory regime,
- and stable under block rescaling.

## Derivation target D
Write an explicit coarse-graining prescription for at least one test class:
- block averages,
- RG blocking,
- or variational projection.

## Failure condition 3
If no explicit coarse-graining map can be written, the continuum limit remains verbal rather than mathematical.

---

# 10. Emergent metric and connection problem

## Definition 6
The continuum limit requires an emergent metric \(g_{\mu\nu}\) and compatible connection, or equivalent geometric data, such that the effective action can be written in covariant continuum form.

## Assumption 6
The coarse-grained geometry sector defines a Lorentzian metric field at leading order in the continuum regime.

This is a strong assumption, but it is the minimum needed to state the GR limit.

## Derivation target E
Show how:
- discrete geometry observables,
- block curvature measures,
- or averaged causal distances

produce:
\[
g_{\mu\nu},\qquad
\nabla_\mu,\qquad
R_{\mu\nu},\qquad
R.
\]

Without this step, the phrase “continuum GR limit” is premature.

---

# 11. Effective action and field equations

## Definition 7
If coarse-graining succeeds, the continuum effective action should take the form
\[
S_{\mathrm{eff}}[g,\phi,R_{\mathrm{eff}}]
=
S_{\mathrm{EH}}[g]
+
S_{\mathrm{mat}}^{\mathrm{eff}}[g,\phi]
+
S_{\mathrm{mem}}^{\mathrm{eff}}[g,R_{\mathrm{eff}},\phi;\chi,\dots].
\]

Varying with respect to \(g^{\mu\nu}\) gives the candidate effective field equations
\[
G_{\mu\nu}
=
8\pi
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right).
\]

## Theorem candidate E
Suppose:
1. the discrete action is admissible,
2. the coarse-graining map is explicit and covariant,
3. the memory sector satisfies C1–C5,
4. and the weak-memory regime exists.

Then the coarse-grained effective field equations reduce to Einstein gravity at leading order:
\[
G_{\mu\nu}
=
8\pi T_{\mu\nu}^{\mathrm{mat}}
+
O(\eta_{\mathrm{mem}}),
\]
where \(\eta_{\mathrm{mem}}\to0\) in the weak-memory limit.

This theorem is **not yet proved**.

---

# 12. Weak-memory regime

This is the key decoupling seam.

## Definition 8
The weak-memory regime is a limit in which the effective retained-memory amplitude is small:
\[
R_{\mathrm{eff}} \sim O(\eta_{\mathrm{mem}}),
\qquad
\eta_{\mathrm{mem}}\to0,
\]
or in which memory variations are sufficiently suppressed relative to geometric curvature.

## Assumption 7
In this regime:
\[
T_{\mu\nu}^{\mathrm{mem}} \to 0
\quad\text{or}\quad
T_{\mu\nu}^{\mathrm{mem}} = O(\eta_{\mathrm{mem}})
\]
while the geometry and matter sectors remain finite.

Then the field equations become
\[
G_{\mu\nu}
=
8\pi T_{\mu\nu}^{\mathrm{mat}}
+
O(\eta_{\mathrm{mem}}).
\]

## Derivation target F
Define \(\eta_{\mathrm{mem}}\) explicitly in terms of:
- retained-memory amplitudes,
- bridge coefficient,
- pruning threshold,
- or coarse-grained loading ratio.

This is still open.

---

# 13. Bianchi consistency and conservation

## Definition 9
Any admissible continuum effective theory must satisfy covariant total conservation:
\[
\nabla^\mu
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
=
0.
\]

## Assumption 8
Either:
1. the matter and memory sectors are separately conserved, or
2. they exchange energy-momentum through a controlled transfer current \(Q_\nu\):
\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mat}} = Q_\nu,
\qquad
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}} = -Q_\nu.
\]

## Derivation target G
Show that the continuum limit of the discrete action is compatible with the contracted Bianchi identity:
\[
\nabla^\mu G_{\mu\nu}=0.
\]

## Failure condition 4
If the memory sector violates Bianchi consistency or requires ad hoc nonconservation, the GR-limit claim fails.

---

# 14. First integrated proof draft for seam 3

## Status
**Live derivation target. First integrated proof pass. Not yet fully closed.**

This section attacks the central continuum-limit question:

> can the affine bridge and its fixed-point coefficient \(\chi\) be embedded into a discrete variational framework whose coarse-grained weak-memory limit reproduces Einstein gravity?

The result of this first pass is:
- the discrete action structure is explicit,
- admissible memory-action classes are separated,
- the weak-memory regime is isolated,
- the effective field-equation target is written down,
- and the failure modes are inspectable.

But no explicit microscopic \(S_{\mathrm{mem}}\), no covariant coarse-graining map, and no emergent metric construction have yet been derived.

So seam 3 is theorem-shaped, but not closed.

---

# 15. First executable tightening pass: minimal scalar-density memory action

## Status
**Live derivation target. First explicit candidate. Not yet microscopically derived.**

We now select the least structurally invasive admissible class, Class A, and write the minimal local scalar-density form that can encode the bridge coefficient \(\chi\), retained-memory loading, and pruning-threshold effects.

## Definition 10
The minimal scalar-density memory action is
\[
S_{\mathrm{mem}}^{(A)}
=
\int d^4x\,\sqrt{-g}\,
\left[
-\frac{1}{2}Z_R(\chi)\,
\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
V(R_{\mathrm{eff}};\chi,\varepsilon^*)
+
\lambda_{\mathrm{int}}(\chi)
R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right].
\]

Here:
- \(R_{\mathrm{eff}}\) is the coarse-grained retained-memory amplitude, or a normalized loading field related to \(\Lambda\);
- \(Z_R(\chi)\) is the kinetic coefficient for the memory field;
- \(V(R_{\mathrm{eff}};\chi,\varepsilon^*)\) is the effective potential encoding pruning-threshold effects;
- \(\lambda_{\mathrm{int}}(\chi)\) is the interaction strength with ordinary matter;
- \(\mathcal O_{\mathrm{mat}}\) is a local matter operator, such as a trace-like scalar built from the matter sector.

This is the cleanest first executable object for seam 3.

## Assumption D1
The coefficient functions are smooth and finite near the fixed-point bridge value:
\[
\chi \approx 0.2667.
\]

## Derivation target H
Derive the explicit functional forms of
\[
Z_R(\chi),\qquad
V(R_{\mathrm{eff}};\chi,\varepsilon^*),\qquad
\lambda_{\mathrm{int}}(\chi)
\]
from the two-mode retained-memory recursion and \(\chi\) fixed-point loading map.

Currently they remain parametric.

---

# 16. Explicit candidate stress-energy tensor for \(S_{\mathrm{mem}}^{(A)}\)

## Definition 11
The metric variation yields the memory stress-energy tensor:
\[
T_{\mu\nu}^{\mathrm{mem}}
=
-\frac{2}{\sqrt{-g}}
\frac{\delta S_{\mathrm{mem}}^{(A)}}{\delta g^{\mu\nu}}.
\]

For the scalar kinetic and potential terms, the canonical contribution is
\[
T_{\mu\nu}^{\mathrm{mem,local}}
=
Z_R(\chi)
\left(
\nabla_\mu R_{\mathrm{eff}}\nabla_\nu R_{\mathrm{eff}}
-
\frac{1}{2}g_{\mu\nu}
\nabla^\rho R_{\mathrm{eff}}\nabla_\rho R_{\mathrm{eff}}
\right)
-
g_{\mu\nu}V(R_{\mathrm{eff}};\chi,\varepsilon^*).
\]

The matter-coupling contribution depends on the exact choice of \(\mathcal O_{\mathrm{mat}}\). Schematic form:
\[
T_{\mu\nu}^{\mathrm{mem,int}}
=
-\lambda_{\mathrm{int}}(\chi)
\left[
R_{\mathrm{eff}}
\frac{2}{\sqrt{-g}}
\frac{\delta(\sqrt{-g}\mathcal O_{\mathrm{mat}})}{\delta g^{\mu\nu}}
\right].
\]

Thus
\[
T_{\mu\nu}^{\mathrm{mem}}
=
T_{\mu\nu}^{\mathrm{mem,local}}
+
T_{\mu\nu}^{\mathrm{mem,int}}.
\]

This is an explicit candidate stress tensor, derived from the candidate action. It is not yet microscopically derived.

---

# 17. Weak-memory scaling

## Lemma candidate 1
Assume the weak-memory regime
\[
R_{\mathrm{eff}} = O(\eta_{\mathrm{mem}}),
\qquad
\eta_{\mathrm{mem}}\to0,
\]
with finite smooth coefficient functions \(Z_R(\chi)\) and \(\lambda_{\mathrm{int}}(\chi)\).

If
\[
V(0;\chi,\varepsilon^*)=0,
\]
then
\[
T_{\mu\nu}^{\mathrm{mem}}
=
O(\eta_{\mathrm{mem}})
\quad\text{or}\quad
O(\eta_{\mathrm{mem}}^2),
\]
provided the matter-coupling term is also proportional to \(R_{\mathrm{eff}}\) or higher powers of \(R_{\mathrm{eff}}\).

### Proof sketch
- Kinetic term:
  \[
  \nabla R_{\mathrm{eff}}\nabla R_{\mathrm{eff}}
  =
  O(\eta_{\mathrm{mem}}^2).
  \]
- Potential term:
  if \(V(0)=0\), then
  \[
  V(R_{\mathrm{eff}})
  =
  V'(0)R_{\mathrm{eff}}
  +
  O(R_{\mathrm{eff}}^2)
  =
  O(\eta_{\mathrm{mem}})
  \]
  or higher.
- Interaction term:
  \[
  \lambda_{\mathrm{int}}R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
  =
  O(\eta_{\mathrm{mem}})
  \]
  if \(\mathcal O_{\mathrm{mat}}\) remains finite.

Therefore the field equations reduce to
\[
G_{\mu\nu}
=
8\pi T_{\mu\nu}^{\mathrm{mat}}
+
O(\eta_{\mathrm{mem}}).
\]

A stronger stationary-memory-vacuum condition would require
\[
V'(0;\chi,\varepsilon^*)=0,
\]
but this is stronger than weak-memory GR decoupling. It should not be conflated with the minimal decoupling condition.

This lemma is structurally established for smooth finite scalar-density candidates, but it is not a microscopic derivation.

---

# 18. Bianchi consistency for the minimal candidate

## Lemma candidate 2
If the total effective action
\[
S_{\mathrm{eff}}
=
S_{\mathrm{EH}}
+
S_{\mathrm{mat}}
+
S_{\mathrm{mem}}^{(A)}
\]
is a diffeomorphism-invariant scalar-density functional of
\[
(g_{\mu\nu},\phi,R_{\mathrm{eff}}),
\]
then the total stress-energy tensor satisfies the on-shell conservation law:
\[
\nabla^\mu
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
=
0.
\]

If the matter-memory interaction
\[
\lambda_{\mathrm{int}}(\chi)R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\]
is nonzero, then matter and memory are not required to be separately conserved. Instead, the admissible structure is:
\[
\nabla^\mu T_{\mu\nu}^{\mathrm{mat}} = Q_\nu,
\qquad
\nabla^\mu T_{\mu\nu}^{\mathrm{mem}} = -Q_\nu,
\]
for a controlled exchange current \(Q_\nu\).

### Proof sketch
The contracted Bianchi identity gives:
\[
\nabla^\mu G_{\mu\nu}=0.
\]

Therefore the effective field equations require:
\[
\nabla^\mu
\left(
T_{\mu\nu}^{\mathrm{mat}}
+
T_{\mu\nu}^{\mathrm{mem}}
\right)
=
0.
\]

For any local diffeomorphism-invariant action, this follows on shell from the variational symmetry of the total action. However, the interaction term may transfer energy-momentum between the matter and memory sectors. Therefore the correct admissibility requirement is not separate conservation, but controlled total conservation.

This satisfies the Bianchi consistency target only if \(Q_\nu\) is finite, covariant, and suppressed or otherwise controlled in the weak-memory regime.

---

# 19. What this tightening pass actually proves

### Established at current proof level
- Seam 3 now possesses its first explicit, variational, computable object:
  \[
  S_{\mathrm{mem}}^{(A)}.
  \]
- An explicit candidate \(T_{\mu\nu}^{\mathrm{mem}}\) is written from the candidate action.
- Weak-memory decoupling is structurally established under the conditions:
  \[
  V(0)=0,
  \qquad
  Z_R(\chi)<\infty,
  \qquad
  \lambda_{\mathrm{int}}(\chi)<\infty.
  \]
- Bianchi consistency is correctly phrased as controlled total conservation, not necessarily separate conservation.
- The seam now has a direct verifier target.

### Not yet proved
- that the coefficient functions descend from the microscopic pruning law;
- that this scalar-density functional form is forced rather than merely admissible;
- that the coarse-graining map actually produces \(R_{\mathrm{eff}}\);
- that the emergent metric/connection construction is complete;
- that the exchange current \(Q_\nu\) is microscopically derived or uniquely controlled.

So seam 3 remains **not closed**, but it now has a concrete mathematical handle for further derivation or falsification.

---

# 20. Updated failure modes after Option A

Seam 3 now fails if any of the following occur, in addition to the original list:

5. the minimal scalar-density coefficients cannot be derived from the microscopic law;
6. \(Z_R(\chi)\) or \(\lambda_{\mathrm{int}}(\chi)\) become singular near \(\chi\approx0.2667\);
7. the potential contains a residual constant term:
   \[
   V(0;\chi,\varepsilon^*)\neq0,
   \]
   producing an unsuppressed cosmological-constant-like residue;
8. the interaction term introduces uncontrolled energy transfer that violates weak-memory scaling;
9. the verifier finds no viable coefficient region satisfying decoupling and controlled conservation;
10. the scalar-density class fails to reproduce the retained-memory recursion under coarse-graining.

---

# 21. Verifier target for the scalar-density memory action

## Status
**Live verifier target. Runnable scaffold required.**

This section defines the minimal verifier for the candidate \(S_{\mathrm{mem}}^{(A)}\). It must confirm that the action is structurally safe — decoupling plus controlled conservation — before investing in microscopic coefficient derivation or coarse-graining maps.

## Definition 12
Set
\[
R_{\mathrm{eff}}(x)=\eta r(x),
\]
where:
- \(\eta\ll1\) is the small memory-loading parameter,
- \(r(x)\) is an \(O(1)\) smooth test function.

## Verifier requirements
The harness must symbolically or numerically verify, for smooth choices of the coefficient functions:
\[
Z_R(\chi),\qquad
V(R;\chi,\varepsilon^*),\qquad
\lambda_{\mathrm{int}}(\chi),
\]
that:

1. **Decoupling scaling**
   \[
   T_{\mu\nu}^{\mathrm{mem}}
   =
   O(\eta)
   \quad\text{or}\quad
   O(\eta^2),
   \]
   so that:
   \[
   G_{\mu\nu}
   =
   8\pi T_{\mu\nu}^{\mathrm{mat}}
   +
   O(\eta).
   \]

2. **Failure-case detection**
   - \(V(0)\neq0\): residual \(O(1)\) cosmological-constant-like term.
   - \(Z_R(\chi)\to\infty\): kinetic decoupling failure.
   - \(\lambda_{\mathrm{int}}(\chi)\to\infty\): interaction decoupling failure.
   - non-suppressed \(Q_\nu\): controlled Bianchi compatibility failure.

3. **Optional stronger vacuum test**
   Test whether:
   \[
   V'(0)=0.
   \]
   This is **not required** for weak-memory GR decoupling, but it is required if \(R_{\mathrm{eff}}=0\) is intended to be a stationary memory vacuum.

## Derivation target I
Implement the verifier and report:
- symbolic leading-order expansion,
- numerical coefficient-family sweep,
- pass/soft-fail/hard-fail classification,
- and explicit failure modes.

---

# 22. Verifier implementation: scalar-density weak-memory decoupling

## Status
**Live verifier implementation. Runnable scaffold provided. Execution log captured.**

The standalone verifier lives in:

```text
continuum_limit_verifier.py
```

A first execution log is captured in:

```text
continuum_limit_verifier_run.log
```

## Classification rules

### PASS
The coefficient family satisfies:
\[
V(0)=0,
\qquad
Z_R(\chi)<\infty,
\qquad
\lambda_{\mathrm{int}}(\chi)<\infty,
\]
and therefore:
\[
T_{\mu\nu}^{\mathrm{mem}}
=
O(\eta)
\quad\text{or smaller.}
\]

### SOFT FAIL
Weak-memory decoupling holds, but an optional stronger condition fails, such as:
\[
V'(0)=0.
\]

This means the candidate may still recover GR at leading order, but the memory vacuum may not be stationary without additional dynamics.

### HARD FAIL
A residual \(O(1)\) term survives as \(\eta\to0\), or a coefficient becomes singular. Examples:
\[
V(0)\neq0,
\qquad
Z_R(\chi)\to\infty,
\qquad
\lambda_{\mathrm{int}}(\chi)\to\infty.
\]

## First captured execution

```text
Symbolic weak-memory expansions
========================================

general:
v0 + eta*(Tmat*lam*r + r*v1) + eta**2*(ZR*dr2/2 + r**2*v2/2) + O(eta**3)

V0_zero:
eta*(Tmat*lam*r + r*v1) + eta**2*(ZR*dr2/2 + r**2*v2/2) + O(eta**3)

V0_Vprime0_zero:
eta**2*(ZR*dr2/2 + r**2*v2/2) + eta**3*r**3*v3/6 + Tmat*eta*lam*r + O(eta**4)

Weak-memory decoupling only
========================================
{'PASS': 94.24, 'SOFT_FAIL': 0.0, 'HARD_FAIL': 5.76}

With stronger stationary-vacuum condition V'(0)=0
========================================
{'PASS': 0.0, 'SOFT_FAIL': 94.24, 'HARD_FAIL': 5.76}
```

## Interpretation

The verifier confirms the structural logic:
- \(V(0)=0\) removes the \(O(1)\) residual term;
- finite \(Z_R\) and finite \(\lambda_{\mathrm{int}}\) keep the kinetic and interaction sectors controlled;
- \(V'(0)=0\) is optional and stronger than minimal weak-memory GR decoupling;
- when the stationary-vacuum condition is required but not enforced, coefficient families move from PASS to SOFT FAIL, not HARD FAIL.

These are structural tests only. They do not derive the coefficient functions.

---

# 23. Connection to downstream files

This file sits upstream of:
- `COSMOLOGY_BACKGROUND.md`
- `COSMOLOGY_PERTURBATIONS.md`

Those files should not be treated as meaningful until this seam is at least partially stabilized, because they presuppose:
- an effective metric,
- an effective stress-energy split,
- and a controlled weak-memory limit.

The logical order remains:

1. `MICROSCOPIC_LAW.md`
2. `OPERATOR_THEOREM.md`
3. `CHI_FIXED_POINT.md`
4. `CONTINUUM_LIMIT.md`
5. `COSMOLOGY_BACKGROUND.md`
6. `COSMOLOGY_PERTURBATIONS.md`

---

# 24. Honest status line

> The first theorem pass for `CONTINUUM_LIMIT.md` is now in place, including the minimal scalar-density tightening, tightened Bianchi lemma, and runnable verifier scaffold with captured execution log. Seam 3 has its first explicit candidate action \(S_{\mathrm{mem}}^{(A)}\), an explicit candidate \(T_{\mu\nu}^{\mathrm{mem}}\), a structural decoupling target, and controlled total conservation via \(Q_\nu\). The verifier makes the scalar-density candidate immediately falsifiable. This is a real step forward, but the microscopic origin of the coefficients, the covariant coarse-graining map, and the emergent metric remain open. Seam 3 is still not closed.

---

# 25. Bottom line

Seam 3 is no longer just an organizational checklist.

It is now a variational program with:
- a concrete candidate action,
- explicit stress-energy and controlled-conservation statements,
- and a runnable verifier scaffold.

The critical path is now:
1. use the verifier log to lock the structural decoupling conditions;
2. derive \(Z_R(\chi)\), \(V(R_{\mathrm{eff}};\chi,\varepsilon^*)\), and \(\lambda_{\mathrm{int}}(\chi)\) from the microscopic pruning law;
3. construct the covariant coarse-graining map;
4. then revisit the emergent metric/connection problem.

`CONTINUUM_LIMIT.md` is updated and ready for the next derivation pass.

**End of file.**


---

# CONTINUUM_LIMIT_CL2_PATCH.md

# Patch CL-2
## Coefficient-function derivation target from the seam-2 loading fixed point

## Status
**Live derivation target. Verifier-backed candidate. Not yet microscopically closed.**

This patch adds the first coefficient-function derivation target to `CONTINUUM_LIMIT.md`.

The goal is to reduce the scalar-density coefficient functions

\[
Z_R(\chi),\qquad
V(R_{\mathrm{eff}};\chi,\varepsilon^*),\qquad
\lambda_{\mathrm{int}}(\chi)
\]

from arbitrary placeholders to explicit candidate functions tied to the seam-2 loading fixed point in `CHI_FIXED_POINT.md`.

This patch does **not** prove that the coefficient functions are derived from the microscopic pruning law. It establishes the first mathematically inspectable bridge:

\[
\text{two-mode loading map}
\quad\Rightarrow\quad
\text{scalar-density continuum coefficients}.
\]

---

# 26. Coefficient-function derivation target from retained-memory recursion

## Status
**Live derivation target. First coefficient ansatz tied to seam 2.**

Seam 2 reduced the bridge coefficient to a loading fixed point:

\[
\Lambda_{n+1}=a\Lambda_n+b,
\]

with stability condition

\[
0\le a<1,\qquad b>0.
\]

The fixed point is

\[
\Lambda_*=\frac{b}{1-a},
\]

and the bridge coefficient is

\[
\chi_*=\frac{1}{1+\Lambda_*}
=
\frac{1-a}{1-a+b}.
\]

The continuum scalar-density field is now identified at first pass as the coarse-grained loading amplitude:

\[
R_{\mathrm{eff}}\sim \Lambda.
\]

Thus the scalar memory action should possess a stable memory-loading equilibrium at

\[
R_*=\Lambda_*.
\]

---

## Definition 13
The first seam-2-tied scalar-memory potential is

\[
V(R_{\mathrm{eff}})
=
\frac{1}{2}m_R^2(\chi)
\left(R_{\mathrm{eff}}-R_*\right)^2
-
\frac{1}{2}m_R^2(\chi)R_*^2,
\]

where

\[
R_*=\Lambda_*=\frac{b}{1-a}.
\]

The subtraction is included so that

\[
V(0)=0.
\]

Therefore the weak-memory decoupling condition from the scalar-density verifier remains satisfied.

---

## Lemma candidate 3
The potential above satisfies:

\[
V(0)=0,
\]

\[
V'(R_*)=0,
\]

and

\[
V''(R_*)=m_R^2(\chi).
\]

Therefore, if

\[
m_R^2(\chi)>0,
\]

then \(R_*\) is a stable retained-memory loading equilibrium.

### Proof sketch
Direct differentiation gives:

\[
V'(R)=m_R^2(R-R_*),
\]

so

\[
V'(R_*)=0.
\]

Also,

\[
V''(R)=m_R^2.
\]

Thus the fixed point is stable if \(m_R^2>0\). The subtraction term makes \(V(0)=0\), preventing an \(O(1)\) cosmological-constant-like residue in the weak-memory limit.

---

# 27. Candidate stiffness from loading-map stability

## Definition 14
The first candidate memory stiffness is

\[
m_R^2(\chi)
=
\mu_R^2(1-a),
\]

where \(\mu_R\) is the coarse-grained memory scale.

## Interpretation
The loading-map perturbation satisfies

\[
\delta\Lambda_{n+1}=a\,\delta\Lambda_n.
\]

Thus:

- if \(a\to1\), the loading fixed point is marginal and the memory field should become soft;
- if \(a\ll1\), the loading fixed point is strongly attractive and the memory field should be stiff.

So

\[
m_R^2\propto 1-a
\]

is the minimal stability-compatible continuum identification.

## Failure condition 11
If the microscopic recursion implies a stiffness unrelated to \(1-a\), then this coefficient ansatz is only phenomenological and must be replaced.

---

# 28. Candidate kinetic coefficient

## Definition 15
The first candidate kinetic coefficient is

\[
Z_R(\chi)
=
Z_0\chi(1-\chi),
\]

where \(Z_0>0\).

## Interpretation
This coefficient:

- is finite at \(\chi\approx0.2667\);
- vanishes at pure-geometry and pure-memory endpoints;
- is largest in the mixed regime;
- uses only the bridge mixture structure and introduces no extra shape function.

This is an admissible first ansatz, not yet a microscopic derivation.

## Failure condition 12
If coarse-graining of the retained-memory recursion produces a different gradient penalty, then \(Z_R(\chi)=Z_0\chi(1-\chi)\) should be treated as a provisional regulator rather than a derived coefficient.

---

# 29. Candidate matter-memory coupling

## Definition 16
The first conservative matter-memory coupling is

\[
\lambda_{\mathrm{int}}(\chi)
=
\lambda_0\chi(1-\chi),
\]

where \(\lambda_0\ge0\).

## Interpretation
This coupling:

- shuts off at pure-geometry and pure-memory endpoints;
- is finite at \(\chi\approx0.2667\);
- suppresses uncontrolled coupling in the weak-memory limit;
- mirrors the same bridge-mixing envelope used by \(Z_R\).

A less conservative candidate would be

\[
\lambda_{\mathrm{int}}(\chi)=\lambda_0(1-\chi),
\]

but the symmetric envelope is safer for first-pass decoupling.

## Failure condition 13
If the microscopic matter-memory coupling scales only with retained-memory load and not with the geometry-memory overlap, then \(\lambda_0(1-\chi)\) may replace the symmetric candidate.

---

# 30. Updated scalar-density candidate after CL-2

Substituting the CL-2 coefficient candidates gives:

\[
S_{\mathrm{mem}}^{(A,\mathrm{CL2})}
=
\int d^4x\,\sqrt{-g}\,
\left[
-\frac{1}{2}Z_0\chi(1-\chi)
\nabla_\mu R_{\mathrm{eff}}\nabla^\mu R_{\mathrm{eff}}
-
\left(
\frac{1}{2}\mu_R^2(1-a)
(R_{\mathrm{eff}}-R_*)^2
-
\frac{1}{2}\mu_R^2(1-a)R_*^2
\right)
+
\lambda_0\chi(1-\chi)
R_{\mathrm{eff}}\mathcal O_{\mathrm{mat}}
\right],
\]

with

\[
R_*=\frac{b}{1-a},
\qquad
\chi=\frac{1-a}{1-a+b}.
\]

This is the first explicit seam-2-to-seam-3 coefficient bridge.

---

# 31. Verifier v2 target

## Status
**Implemented as `continuum_limit_verifier_v2.py`. Execution log captured.**

Verifier v2 checks:

1. stable loading:
   \[
   0\le a<1,\qquad b>0;
   \]

2. bridge range:
   \[
   0<\chi<1;
   \]

3. finite positive kinetic coefficient:
   \[
   Z_R=Z_0\chi(1-\chi)>0;
   \]

4. finite matter coupling:
   \[
   \lambda_{\mathrm{int}}=\lambda_0\chi(1-\chi)\ge0;
   \]

5. positive stiffness:
   \[
   m_R^2=\mu_R^2(1-a)>0;
   \]

6. weak-memory decoupling:
   \[
   V(0)=0;
   \]

7. fixed-point stationarity:
   \[
   V'(R_*)=0;
   \]

8. stable potential curvature:
   \[
   V''(R_*)>0.
   \]

---

# 32. Verifier v2 captured output

```text
CL-2 symbolic coefficient derivation
==================================================
Lambda_star: -b/(a - 1)
chi: (1 - a)/(-a + b + 1)
Z_R: -Z0*b*(a - 1)/(-a + b + 1)**2
lambda_int: -b*lambda0*(a - 1)/(-a + b + 1)**2
m_R2: muR**2*(1 - a)
V0: 0
Vprime_at_Rstar: 0
Vsecond_at_Rstar: muR**2*(1 - a)
Tmem_expansion: eta*(-Tmat*b*lambda0*r*(a - 1)/(-a + b + 1)**2 - b**2*muR**2*(2*a*r/b - 2*r/b)/(2*(a - 1))) + eta**2*(-Z0*b*dr2*(a - 1)/(2*(-a + b + 1)**2) - b**2*muR**2*(a*r/b - r/b)**2/(2*(a - 1))) + O(eta**3)

CL-2 numerical sweep
==================================================
PASS: 99.191
SOFT_FAIL: 0.0
HARD_FAIL: 0.809
chi_min: 0.0005766938303031946
chi_median: 0.7935310738878313
chi_max: 0.9989839526125909
Lambda_min: 0.0010170807896883022
Lambda_median: 0.260190095771037
Lambda_max: 1733.0223658613684
Z_R_median: 0.05415588182140546
lambda_int_median: 0.005391396262720907
m_R2_median: 0.39301924878618466
```

---

# 33. Interpretation of CL-2

### Established at current proof level
- The scalar-density coefficients are no longer arbitrary placeholders.
- \(V\) is tied to the seam-2 loading fixed point.
- \(m_R^2\) is tied to loading-map stability.
- \(Z_R\) and \(\lambda_{\mathrm{int}}\) are tied to the geometry-memory overlap envelope.
- The verifier confirms that the CL-2 candidate satisfies the structural continuum checks for broad sampled parameter ranges.

### Not yet proved
- \(Z_0,\lambda_0,\mu_R\) are not derived from the microscopic pruning law.
- The \(\chi(1-\chi)\) envelope is symmetry-motivated, not uniquely forced.
- The scalar field \(R_{\mathrm{eff}}\sim\Lambda\) has not yet been produced by an explicit covariant coarse-graining map.
- The emergent metric and connection are still assumed.
- The matter-memory operator \(\mathcal O_{\mathrm{mat}}\) remains unspecified.

Therefore CL-2 does **not** close seam 3. It upgrades seam 3 from:

> admissible scalar-density candidate

to:

> scalar-density candidate with coefficients structurally tied to the seam-2 loading fixed point and verifier-backed for weak-memory decoupling.

---

# 34. Updated critical path

The next derivation target is now the microscopic coefficient link:

\[
(\alpha_s,\alpha_f,\beta_s,\beta_f,c_s,c_f,\mu_G,\overline I_*^{(s)},\overline I_*^{(f)})
\quad\Rightarrow\quad
(a,b)
\quad\Rightarrow\quad
(Z_R,V,\lambda_{\mathrm{int}}).
\]

The immediate next file should be:

```text
COEFFICIENT_DERIVATION.md
```

Its job:

1. derive \(a,b\) from the two-mode recursion,
2. derive \(R_*=\Lambda_*\),
3. derive or constrain \(Z_0,\lambda_0,\mu_R\),
4. determine whether the \(\chi(1-\chi)\) envelope is forced or merely admissible,
5. identify whether Class A survives microscopic closure or must yield to the nonlocal kernel Class C.

---

# Honest status line

> Patch CL-2 ties the first scalar-density continuum coefficients to the seam-2 loading fixed point and verifies their structural safety. This is not a derivation from the microscopic pruning law, but it is a real reduction in ambiguity: the continuum memory action is now connected to the fixed-point loading machinery rather than floating as an arbitrary effective field ansatz.

**End of patch.**
