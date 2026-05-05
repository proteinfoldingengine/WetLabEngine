# MICROSCOPIC_LAW.md

# Microscopic Law
## Candidate discrete collapse/update law for the GEM Bridge program

## Status
**Blueprint for closure. Not yet closed.**

This file proposes an explicit microscopic law candidate from which the coarse-grained bridge program may be derived.

It does **not** claim that the law is correct.
It does **not** claim that the bridge has already been derived from it.
It does **not** claim that the resulting continuum theory already reproduces GR or cosmology.

Its purpose is narrower:

> to state a concrete microscopic collapse/update law clearly enough that the derivation targets in Package 17 can be attacked, verified, or falsified.

---

## Tagging rule
Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be read as a completed proof unless explicitly stated.

---

# 1. Goal of this file

The purpose of the microscopic law is to provide a bottom-up dynamical starting point for:

1. the coarse-grained geometry sector \(G_t\),
2. the retained-memory sector \(R_t\),
3. the innovation amplitude \(\xi_t\),
4. the pruning threshold \(\varepsilon^*\),
5. and eventually the bridge operator \(\Psi(G_t,R_t)\).

The law must be:

- autonomous,
- time-homogeneous,
- local at the microscopic event level,
- compatible with controlled nonlocal memory after coarse-graining,
- and sufficiently explicit that A1–A5 can be derived from it rather than merely attached to it.

---

# 2. Microscopic ontology

## Assumption 1
The underlying microstructure is a discrete causal lattice or causal set \(\mathcal{C}\) of events.

Each event \(e_t \in \mathcal{C}\) carries:
- local geometry data,
- local matter-density data,
- and adjacency/causal-order information.

No continuum manifold is assumed at the microscopic level.

## Assumption 2
The microscopic state at step \(t\) is a superposition of geometry-matter branches:
\[
|\Psi_t\rangle = \sum_i c_i(t)\,|G_i,\phi_i\rangle,
\qquad
\sum_i |c_i(t)|^2 = 1.
\]

Here:
- \(G_i\) denotes a discrete geometry branch,
- \(\phi_i\) denotes matter content on that branch,
- \(c_i(t)\in\mathbb{C}\).

## Definition 1
The pair \((G_i,\phi_i)\) will be called a **branch state**.

---

# 3. One-step microscopic evolution

## Assumption 3
Microscopic evolution over one step is split into two stages:

1. **pre-collapse propagation**
2. **gravity-induced pruning/selection**

This gives a discrete update structure:
\[
|\Psi_t\rangle
\;\xrightarrow{\;U_t\;}\;
|\widetilde{\Psi}_t\rangle
\;\xrightarrow{\;\mathcal{P}_{\varepsilon^*}\;}\;
|\Psi_{t+1}\rangle.
\]

## Definition 2
The pre-collapse propagated state is
\[
|\widetilde{\Psi}_t\rangle := U_t |\Psi_t\rangle,
\]
where \(U_t\) is a linear propagator.

At this stage, \(U_t\) may be:
- unitary,
- approximately unitary,
- or locally unitary with environmental coupling absorbed later into pruning.

## Derivation target A
Specify the exact microscopic propagator class:
- discrete Hamiltonian evolution,
- transfer matrix,
- or path-integral kernel.

Until this is done, \(U_t\) is only a placeholder.

---

# 4. Branch-separation observable

A collapse or pruning law needs a branch-separation observable.

## Definition 3
For any pair of branches \(i,j\), define the discrete gravitational branch-separation functional
\[
\Delta E_{\mathrm{grav}}(i,j).
\]

A Penrose–Diósi-inspired candidate form is:
\[
\Delta E_{\mathrm{grav}}(i,j)
=
G
\sum_{x,y\in\mathcal{C}}
\frac{\big(\rho_i(x)-\rho_j(x)\big)\big(\rho_i(y)-\rho_j(y)\big)}
{d(x,y)}
\,\Delta V_x \Delta V_y.
\]

Here:
- \(G\) is Newton’s constant,
- \(\rho_i(x)\) is the matter-density observable on branch \(i\) at site \(x\),
- \(d(x,y)\) is a discrete proper-distance surrogate,
- \(\Delta V_x\) is the local lattice volume element.

## Assumption 4
The dominant collapse-driving observable is gravitational branch separation, not arbitrary Hilbert-space distance.

This is the gravity-induced reduction hypothesis.

## Derivation target B
Make the definition of \(d(x,y)\) and \(\Delta V_x\) precise on the chosen causal lattice.

## Failure condition 1
If no lattice-consistent, finite, and covariant-enough definition of \(\Delta E_{\mathrm{grav}}\) can be supplied, the present microscopic law fails at its core.

---

# 5. Pruning law

## Definition 4
The pruning/selection weight is a thresholded function of \(\Delta E_{\mathrm{grav}}\).

A softened threshold candidate is:
\[
\mathcal{P}_{\varepsilon^*}(\Delta E)
=
\frac{1}{1+\exp[-\beta(\Delta E-\varepsilon^*\hbar/\tau)]}.
\]

Parameters:
- \(\varepsilon^* > 0\): collapse threshold,
- \(\tau > 0\): characteristic microscopic time scale,
- \(\beta > 0\): threshold sharpness.

## Assumption 5
The threshold is physical, not merely numerical:
\[
\varepsilon^*\hbar/\tau
\]
sets the effective collapse trigger scale.

## Definition 5
The pruned post-update state is:
\[
|\Psi_{t+1}\rangle
=
\mathcal{N}^{-1}
\sum_i \widetilde{c}_i(t)\,w_i(t)\,|G_i,\phi_i\rangle,
\]
where:
- \(\widetilde{c}_i(t)\) are amplitudes after pre-collapse propagation,
- \(w_i(t)\) are branch-retention weights induced by pairwise pruning,
- \(\mathcal{N}\) is normalization.

One admissible choice is:
\[
w_i(t)=\prod_{j\neq i}\mathcal{P}_{\varepsilon^*}\!\big(\Delta E_{\mathrm{grav}}(i,j)\big),
\]
or a logarithmic/additive surrogate if products are too singular.

## Derivation target C
Choose and justify the exact branch-weight aggregation rule:
- multiplicative,
- additive in log-weight,
- or extremal selection.

## Failure condition 2
If the branch-weight rule effectively presupposes the coarse-grained bridge, rather than generating it, the derivation is circular.

---

# 6. Innovation observable

The retained-memory program requires a well-defined innovation load.

## Definition 6
Let the innovation amplitude \(\xi_t\) be a coarse-grained measure of unresolved branch separation after pruning.

A candidate definition is:
\[
\xi_t
:=
\sum_{i<j}
|c_i^{\mathrm{post}}(t)c_j^{\mathrm{post}}(t)|
\,\Xi(i,j),
\]
where \(\Xi(i,j)\) is a normalized branch-separation kernel.

The simplest candidate is
\[
\Xi(i,j)=\frac{\Delta E_{\mathrm{grav}}(i,j)}{\Delta E_{\mathrm{grav}}(i,j)+E_0}
\]
for some fixed scale \(E_0\), or another bounded monotone function.

## Assumption 6
The relevant retained innovation is amplitude-like rather than phase-like, because the collapse process preferentially suppresses phase-sensitive branch interference while retaining unresolved geometric deviation.

## Derivation target D
Show that the retained-memory load function is
\[
\phi(\xi_t)=|\xi_t|
\]
or derive the correct alternative.

## Failure condition 3
If the innovation variable cannot be defined from the microscopic law without ambiguity large enough to alter the retained-memory recursion qualitatively, closure fails at the coarse-graining step.

---

# 7. Coarse-grained observables

The microscopic law must induce coarse-grained variables.

## Definition 7
Define the coarse-grained geometry sector \(G_t\) as an expectation or selected-branch statistic over the post-pruned state:
\[
G_t := \mathbb{E}_{\Psi_t^{\mathrm{post}}}[\,\mathcal{G}\,],
\]
where \(\mathcal{G}\) is a chosen geometry observable or observable set.

## Definition 8
Define the retained-memory sector \(R_t\) as a recursively accumulated statistic of past innovations:
\[
R_t = \mathcal{R}(\xi_{t-1},\xi_{t-2},\dots).
\]

At this file’s level, \(R_t\) is not yet assumed to be two-mode; that belongs to the next derivation step.

## Derivation target E
Show that the microscopic law induces a finite-dimensional retained-memory closure:
\[
X_t=(G_t,R_t,\xi_t)
\]
with no need for an infinite explicit history state.

---

# 8. Recovery of A1–A5

This section states the derivation targets that link the microscopic law to the already-developed retained-memory program.

## Theorem candidate 1
Under the microscopic law above, the induced coarse-grained process satisfies:

- **A1** finite-dimensional autonomous closure,
- **A2** time-homogeneous recursion,
- **A3** contractive forgetting,
- **A4** innovation-load memory,
- **A5** slow backbone plus fast seam.

This theorem is **not yet proved**.

### Subtarget 1: A1
Show that the coarse-grained update can be written
\[
X_{t+1}=F(X_t)
\]
or
\[
X_{t+1}=F(X_t,\eta_t)
\]
for finite-dimensional \(X_t\), where \(\eta_t\) is admissible noise if needed.

### Subtarget 2: A2
Show stationarity of the recursion coefficients under a time-homogeneous microscopic law.

### Subtarget 3: A3
Show contractivity:
\[
\|R_{t+1}-R'_{t+1}\|
\le \alpha \|R_t-R'_t\|,
\qquad 0<\alpha<1.
\]

### Subtarget 4: A4
Derive the memory load from the innovation observable:
\[
\phi(\xi_t)=|\xi_t|
\]
or replace this with the exact derived form.

### Subtarget 5: A5
Show emergence of at least two effective retention horizons:
\[
R_t = R_t^{(s)} + R_t^{(f)}.
\]

## Failure condition 4
If A5 only appears after being inserted by hand as an extra ansatz, the two-mode structure remains phenomenological rather than microscopic.

---

# 9. Two-mode retained-memory sector

This section states the target recursion, but does not yet claim derivation.

## Definition 9
The target coarse-grained two-mode recursion is:
\[
R_{t+1}^{(s)}=\alpha_s R_t^{(s)}+\beta_s |\xi_t|,
\]
\[
R_{t+1}^{(f)}=\alpha_f R_t^{(f)}+\beta_f |\xi_t|\,\Theta(|\xi_t|-\varepsilon^*),
\]
with
\[
R_t = w_s R_t^{(s)} + w_f R_t^{(f)}.
\]

Interpretation:
- \(R^{(s)}\): slow persistent backbone,
- \(R^{(f)}\): fast seam mode,
- \(\Theta\): threshold activation.

## Derivation target F
Derive this exact or equivalent two-timescale structure from the microscopic collapse law.

## Failure condition 5
If the microscopic law yields only a one-mode or infinitely many unconstrained modes without a minimal two-mode reduction, the claimed retained-memory minimality is weakened or lost.

---

# 10. Relation to the bridge operator

This file stops before the operator theorem, but it must prepare for it.

## Definition 10
The future bridge target is
\[
A_{t+1} = \Psi(G_t,R_t).
\]

## Derivation target G
Show that the microscopic law and the induced coarse-grained closure produce a well-defined admissible operator class for \(\Psi\).

This file does **not** yet claim:
\[
\Psi(G_t,R_t)=\chi G_t+(1-\chi)R_t.
\]

That belongs to `OPERATOR_THEOREM.md`.

---

# 11. Minimal consistency checks

Any proposed microscopic law must pass all of these.

## Check 1: normalization
The update must preserve total probability after pruning and renormalization.

## Check 2: threshold behavior
As \(\Delta E_{\mathrm{grav}}\ll \varepsilon^*\hbar/\tau\), pruning should be weak.
As \(\Delta E_{\mathrm{grav}}\gg \varepsilon^*\hbar/\tau\), pruning should be strong.

## Check 3: autonomy
The update at event \(t\) may depend on local structure and retained memory, but should not require externally tuned step-dependent parameters.

## Check 4: contractive memory
The induced retained-memory recursion must actually forget old innovations.

## Check 5: seam sparsity
Fast-mode activation should be sparse in the low-innovation regime and concentrated near threshold crossings.

## Failure condition 6
If the microscopic law fails any of these checks, it is not a viable starting point for Package 17.

---

# 12. What this file does not yet do

This file does **not** yet provide:

- a proof that A1–A5 follow,
- a theorem of operator uniqueness,
- a derivation of \(\chi\),
- a continuum GR limit,
- or cosmological equations.

Those are later files in the package.

This file exists only to remove the first ambiguity:
**what exact microscopic law candidate is being proposed and what would count as success or failure for it.**

---

# 13. Public interpretation rule

The correct public wording at this stage is:

> We now have a concrete microscopic collapse/update law candidate. It is explicit enough to pressure-test. It is not yet proved to generate the bridge, the GR limit, or the cosmology.

That is the honest interpretation.

---

# 14. Bottom line

This microscopic law is the first true foundational candidate in Package 17.

If it survives scrutiny, it supplies the starting point for:
- deriving A1–A5 from dynamics,
- deriving the two-mode retained-memory backbone from collapse,
- defining the admissible bridge-operator space,
- and ultimately testing the GR and cosmology limits.

If it fails, it should fail here, clearly and publicly.

That is the purpose of the file.
