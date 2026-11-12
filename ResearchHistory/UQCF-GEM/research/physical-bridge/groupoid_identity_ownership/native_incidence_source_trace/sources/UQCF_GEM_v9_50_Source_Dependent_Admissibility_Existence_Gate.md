# UQCF-GEM v9.50 — Source-Dependent Admissibility Deformation Existence Gate

## Status

**Theorem-first branch audit. No ensemble simulation was released.**

Certified classification:

\[
\boxed{
\texttt{NONTRIVIAL\_SOURCE\_DEPENDENT\_ADMISSIBILITY\_REQUIRES\_A\_NEW\_KINEMATIC\_PRIMITIVE}
}
\]

This is an exact statement about the frozen finite-dimensional UQCF-GEM admissibility architecture. It is not a theorem that gravity cannot exist before pruning.

---

## 1. Frozen architecture

Let

\[
\mathcal H_G=\bigotimes_{i\in V}\mathcal H_i,
\qquad
\mathcal D_G=\{X=X^\dagger:X\succeq0,\ \operatorname{Tr}X=1\},
\]

and let

\[
\mathsf M_E:\mathcal D_G\longrightarrow
\prod_{e\in E}\mathcal D(\mathcal H_e)
\]

be the fixed edge-marginal map. The compatibility arena is

\[
\mathcal A_G=\mathsf M_E(\mathcal D_G).
\]

The gate asks whether a source label \(s\) can produce a nonconstant family

\[
\mathcal A_G(s)
\]

without adding a source-dependent state cone, global constraint, Hilbert-space structure, tensor factorization, marginal/gluing map, or selection law.

---

## 2. Fixed-image theorem

### Theorem 1 — Parameter-absence / fixed-image theorem

If \(\mathcal D_G\) and \(\mathsf M_E\) are fixed, then the set of globally compatible visible data is fixed:

\[
\boxed{\mathcal A_G=\mathsf M_E(\mathcal D_G).}
\]

An external label \(s\) that has no representation in either the domain or the map cannot change this image.

### Proof

The image of a fixed set under a fixed map is a fixed set. A nonconstant source-indexed image must therefore have the form

\[
\mathcal A_G(s)=\mathsf M_{E,s}(\mathcal D_{G,s}),
\]

with at least one of \(\mathcal D_{G,s}\) or \(\mathsf M_{E,s}\) nonconstant, or else it is not a deformation of the frozen compatibility construction. \(\square\)

This elementary theorem is decisive because all current source constructions act on states, weights, objectives, or selected fibers while retaining \(\mathcal D_G\) and \(\mathsf M_E\).

---

## 3. Exhaustive classification inside the frozen architecture

Let \(s\) enter a construction while \(\mathcal D_G\) and \(\mathsf M_E\) remain fixed.

### 3.1 Source-conditioned predicate

For a predicate \(P_s(X)\), define

\[
\mathcal D_{G|s}=\{X\in\mathcal D_G:P_s(X)\},
\qquad
\mathcal A_{G|s}=\mathsf M_E(\mathcal D_{G|s}).
\]

Then

\[
\mathcal A_{G|s}\subseteq\mathcal A_G.
\]

This is state selection or conditioning. The compatibility arena has not changed; a subset has been chosen. Treating this subset as the new arena adds the predicate \(P_s\) as a hard source-dependent constraint.

### 3.2 State transformation

For any map \(T_s:\mathcal D_G\to\mathcal D_G\),

\[
\mathcal R_s=\mathsf M_E(T_s(\mathcal D_G))\subseteq\mathcal A_G.
\]

This is a reachable set inside the existing arena. It is not a deformation of global compatibility. v9.49 additionally proved that a deterministic trace-preserving operation localized to a source subsystem leaves the entire exterior reduced state unchanged.

### 3.3 Reweighting or measure change

A density \(w_s(X)\) changes probabilities on \(\mathcal D_G\). If it has full support, the support of compatible visible data remains \(\mathcal A_G\). If it has smaller support, it implements selection. No new arena follows from weighting alone.

### 3.4 Objective change

Replacing an objective \(J(X)\) by \(J_s(X)\) changes a preferred optimizer, not feasibility:

\[
\operatorname*{argmin}_{X\in\mathcal D_G}J_s(X)
\quad\text{versus}\quad
\mathcal D_G.
\]

An energy term, completion burden, Hodge action, or other selector cannot become an admissibility law unless a new rule declares nonoptimizers forbidden.

### Classification theorem

Within the frozen architecture, all source-indexed constructions of these types reduce to:

\[
\boxed{
\text{selection},\quad
\text{reachability},\quad
\text{reweighting},\quad
\text{or objective choice}.
}
\]

None is a nontrivial deformation of \(\mathcal A_G\).

---

## 4. Covariance cannot supply the missing source law

Covariance constrains a source-dependent construction after a source action has been specified. It does not create that action.

Suppose a symmetry group \(K\) acts on the kinematic data and on source labels. A covariant family would obey schematically

\[
\mathcal A_G(k\cdot s)=k\cdot\mathcal A_G(s).
\]

To obtain a nonconstant family, the theory still needs:

1. a representation of source labels;
2. a seed deformation or source-indexed constraint;
3. an action on the feasible global states or the compatibility map.

These are additional data. Covariance can reject arbitrary additions, but cannot derive a nonzero deformation from a label absent from the frozen kinematics.

---

## 5. Can sourcehood be a defect of global realizability?

This is the strongest constructive alternative suggested by v9.49.

### 5.1 Absolute compatibility defect

For visible data \(y\), the intrinsic feasibility question is

\[
y\in\mathcal A_G\quad\Longleftrightarrow\quad
\exists X\in\mathcal D_G:\mathsf M_E(X)=y.
\]

The metric-free obstruction is binary:

\[
\delta_G(y)=
\begin{cases}
0,&y\in\mathcal A_G,\\
1,&y\notin\mathcal A_G.
\end{cases}
\]

Every visible configuration produced by a valid global state has \(\delta_G=0\). Therefore a nonzero absolute compatibility defect cannot simultaneously be a property of a globally compatible realization in the frozen theory.

Quantitative distance from \(\mathcal A_G\) additionally requires a norm, divergence, or cost. A dual infeasibility witness certifies exterior data that have no global realization; it does not by itself define a physical source inside a valid realization.

### 5.2 Relative defect

A nonzero defect inside \(\mathcal A_G\) can be defined relative to a stricter reference class \(\mathcal C_0\subsetneq\mathcal D_G\):

\[
\delta_{\mathcal C_0}(y)=0
\quad\Longleftrightarrow\quad
y\in\mathsf M_E(\mathcal C_0).
\]

But \(\mathcal C_0\), its metric or obstruction theory, and the rule identifying its defect with sourcehood are new primitives unless independently derived.

### 5.3 Fiber singularity and topology

The realization fiber

\[
\mathfrak F(y)=\{X\in\mathcal D_G:\mathsf M_E(X)=y\}
\]

can have intrinsic rank strata, isotropy, dimension, singularities, or topology. These may define genuine global invariants. They still do not supply a source label or a source-composition law by themselves. Calling a particular fiber feature a source requires a derived equivalence between that feature, a local signature, and a rule for combining multiple defects.

### Defect-source adjudication

The current theory can define incompatibility and fiber structure. It cannot derive **sourcehood** as a nonzero defect of a compatible state without introducing a reference class, extended state object, altered gluing law, or defect variable.

Thus the proposed reversal

\[
\text{global defect}\to\text{local source signature}\to\text{global response}
\]

is logically viable only after the first arrow is supplied by new mathematics. It is not presently a consequence of \((\mathcal D_G,\mathsf M_E)\).

---

## 6. Minimal new primitive

The weakest mathematically honest addition is a **source representation on admissibility data**.

Let \((\mathsf S,\oplus,0)\) be a source-composition monoid. A source law must assign

\[
s\longmapsto \mathfrak K_s,
\qquad
\mathfrak K_s=(\mathcal H_{G,s},\mathcal C_{G,s},\mathcal D_{G,s},\mathsf M_{E,s}),
\]

with

\[
\mathcal A_G(s)=\mathsf M_{E,s}(\mathcal D_{G,s}),
\qquad
\mathfrak K_0=\mathfrak K.
\]

At least one nontrivial component is necessary:

| Possible addition | What it changes | Main burden |
|---|---|---|
| Source-indexed global constraint \(\mathcal D_{G,s}\subseteq\mathcal D_G\) | Allowed global realizations | Must not be disguised conditioning |
| Source-indexed positive cone \(\mathcal C_{G,s}\) | Meaning of positivity/physical state | Must preserve probability and composition |
| Source-indexed marginal or gluing map \(\mathsf M_{E,s}\) | How global and local data correspond | Must be canonical and subsystem-consistent |
| Source-indexed factorization \(\mathcal H_{G,s}\) | Subsystem structure | Must derive local identities and comparison maps |
| Extended global object \((X,z)\) with defect variable \(z\) | Adds latent compatibility data | Must derive observables and eliminate arbitrary gauge |

The logically smallest addition is a source-indexed feasible global set plus a principled composition law. The physically stronger option is a source action on the gluing/compatibility structure from which those sets follow.

---

## 7. Composition gate

A one-source deformation is insufficient. Independent sources need a coherent composition rule. Minimally:

\[
\mathfrak K_0=\mathfrak K,
\qquad
\mathfrak K_{s\oplus t}\simeq
\mathfrak K_s\star\mathfrak K_t,
\]

where \(\star\) must be associative and covariant, and should be symmetric for operationally independent sources.

Examples illustrate the burden:

- Hard independent constraints suggest \(\mathcal D_{s\oplus t}=\mathcal D_s\cap\mathcal D_t\), but this is idempotent and does not automatically represent additive source strength.
- Channel composition gives \(T_{s\oplus t}=T_s\circ T_t\), but v9.49 shows local CPTP actions do not deform exterior compatibility.
- Map or cone deformation can be nontrivial, but requires a canonical rule for composing deformations and comparing their domains.

Therefore source composition is not a later phenomenological detail. It is part of the missing primitive's definition.

---

## 8. Gate adjudication

| Gate | Requirement | Result |
|---|---|---|
| A | Nonconstant \(\mathcal A_G(s)\) from fixed \(\mathcal D_G,\mathsf M_E\) | **FAIL — exact fixed-image theorem** |
| B | Not state selection or conditioning | **FAIL for source level sets and pure-fiber slices** |
| C | Not state reweighting or objective change | **FAIL for measure/action constructions** |
| D | Not merely operational reachability | **FAIL for state channels** |
| E | Sourcehood derived from absolute compatibility defect | **FAIL — compatible realizations have zero defect** |
| F | Intrinsic multi-source composition from current primitives | **FAIL — no source representation/action exists** |

Final classification:

\[
\boxed{
\texttt{NONTRIVIAL\_SOURCE\_DEPENDENT\_ADMISSIBILITY\_REQUIRES\_A\_NEW\_KINEMATIC\_PRIMITIVE}
}
\]

---

## 9. Scientific meaning

The completed canary program has located a precise missing object.

The frozen theory already contains:

- global positivity;
- marginal compatibility;
- pure-realization fibers;
- hidden completion geometry;
- source observables and selective/nonselective instruments;
- conditional pruning maps.

It does **not** contain a source representation that acts on the rules of global realizability. Consequently, it cannot derive a source-dependent compatibility arena.

This result prevents a source-conditioned subset, preferred optimizer, probability bias, or local quantum operation from being renamed a pre-pruning gravity law.

It also refines the constructive target. If sourcehood is to emerge from global admissibility, the theory needs an extended compatibility structure in which a defect is nonzero while the enlarged global object remains valid, the defect has a canonical local restriction, and independent defects compose.

---

## 10. Claim boundaries and stopping rule

### Exact theorem

With fixed \(\mathcal D_G\) and fixed \(\mathsf M_E\), the compatibility image is fixed. Predicates, channels, measures, and objectives produce selection, reachability, weighting, or optimization, not a new arena.

### Structural conclusion

A nontrivial pre-pruning source law requires an additional kinematic primitive: a source-indexed feasible set, cone, gluing map, factorization, or extended defect-bearing global object, together with a composition law.

### Not established

- that nature contains such a primitive;
- that any candidate primitive is gravity;
- that a compatibility defect produces mass, attraction, geometry, or Einstein dynamics;
- that pruning or physical time already occurs pre-pruning.

### Stopping rule

Do not run another ensemble on the frozen source constructions. The next legitimate task is **axiom synthesis and uniqueness**, not numerical mining:

\[
\boxed{
\text{Find the minimal covariant, compositional extension in which sourcehood is a global defect.}
}
\]

Any proposed extension must state explicitly which frozen primitive it changes and must recover the source-free architecture at \(s=0\).
