# UQCF-GEM v14.04 — Provenance Representation / Intertwiner Gate

**Date:** 2026-09-12  
**Adjudication:** `REQUIRES_NEW_REPRESENTATION_LINK`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Executive result

v14.03 established a conditional source-selection chain for a **supplied** positive projective Hermitian support-space source ray:

\[
[P]_+
\longrightarrow
[\Pi_{\rm hid}\dot X_P]
\longrightarrow
X_*(P)
\longrightarrow
[g(P)].
\]

v14.04 asks whether the frozen Genesis/provenance stack itself naturally supplies the required typed object

\[
[P]_+,
\qquad
P\in\mathrm{Herm}(25),
\qquad
P\sim aP+bI,\ a>0.
\]

The combined answer is:

\[
\boxed{\texttt{REQUIRES\_NEW\_REPRESENTATION\_LINK}}.
\]

The result has two layers.

First, an exact representation-theoretic sub-theorem closes the gauge-trivial provenance case:

\[
\boxed{
\text{support-gauge-trivial provenance}
\Longrightarrow
[P]_+=[I]
\Longrightarrow
\dot X_P=0.
}
\]

Second, the frozen archive does contain nontrivial provenance carriers, including the archived 6-D Genesis field representation and retained graph source/current structure. But the audited frozen artifacts do not certify a natural representation/intertwiner from those carriers into the fixed 25-dimensional v14.03 support.

Explicitly supplying such an intertwiner is sufficient to generate a valid noncentral v14.03 chain, but different admissible supplied intertwiners produce strongly inequivalent projective source rays and strongly inequivalent hidden-contact/dual selections. Therefore the relative representation link is genuine missing information rather than a dispensable coordinate convention.

This is a **major upstream representation no-go / branch-stop result relative to the audited frozen ontology**, not a broad scientific breakthrough.

---

# I. Theorem

## 1. Source and target types

Let \(D_{\rm prov}\) denote provenance information that carries no certified action of the support-coordinate gauge group \(U(25)\).

The v14.03 consumer requires a positive projective Hermitian source class

\[
[P]_+,
\qquad P=P^\dagger\in\mathrm{Herm}(25),
\]

with equivalence

\[
P\sim aP+bI,
\qquad a>0.
\]

Because the support coefficient basis is gauge, a natural map from gauge-trivial provenance must satisfy, at projective level,

\[
[UPU^\dagger]_+=[P]_+
\qquad\forall U\in U(25).
\]

Thus for every \(U\), there exist real \(a_U>0\) and \(b_U\) with

\[
UPU^\dagger=a_U P+b_UI.
\]

The right-hand side commutes with \(P\), so every support-gauge conjugate would have to commute with \(P\).

If \(P\) is noncentral, choose a unitary that mixes two distinct eigenspaces of \(P\). Then generically

\[
[P,UPU^\dagger]\ne0,
\]

contradicting the projective naturality condition.

Hence

\[
\boxed{P=\lambda I}.
\]

This is the **Support-Gauge Projective Centrality Theorem** for the audited type assignment.

## 2. PGRL-null consequence

v14.03 uses the normalized exponential-family source response

\[
X_s(P)=
\frac{\exp(\log X_0+sP)}
{\mathrm{Tr}\exp(\log X_0+sP)}.
\]

For

\[
P=\lambda I,
\]

the scalar exponential cancels in normalization, so

\[
X_s(\lambda I)=X_0
\]

for all \(s\), and therefore

\[
\boxed{\dot X_{\lambda I}=0}.
\]

The executable control over

```text
lambda = [-3.5, -1.0, 0.2, 2.0, 11.0]
```

gives

```text
max identity-source PGRL tangent norm = 5.900100316503041e-16
```

under the unchanged v14.03 Fréchet tangent implementation.

So gauge-trivial provenance cannot produce a nontrivial v14.03 source direction through a natural map into the support carrier.

---

# II. Reproducible computation

## 3. Exact Heisenberg–Weyl 1-design control

The analytic theorem does not depend on sampling. Nevertheless, the implementation includes a deterministic full finite twirl regression using the complete 25-dimensional Heisenberg–Weyl unitary 1-design:

\[
\frac1{25^2}
\sum_{a,b=0}^{24}
W_{ab}PW_{ab}^\dagger
=
\frac{\mathrm{Tr}P}{25}I.
\]

All

```text
25^2 = 625
```

Weyl operators are used; this is not a Monte Carlo approximation.

For two deterministic noncentral Hermitian probes:

```text
max Weyl-twirl relative error = 2.0899933776153146e-14
```

A fixed Hadamard plane-mixing unitary and the discrete Fourier unitary were also used as orbit controls. The smallest residual after fitting

\[
UPU^\dagger\approx aP+bI,\qquad a>0,
\]

was

```text
0.02773234285516979
```

which is far from projective equivalence.

The central control remains invariant to

```text
4.26351937961921e-15.
```

These numbers are regression controls for the exact theorem, not its proof.

## 4. Frozen provenance-carrier inventory

The executable type audit inspected four frozen candidate classes tied to concrete archived artifacts.

### 4.1 Genesis ledger / source-origin identity

Artifact:

```text
Tmp/TOE/Einstein 6/v1172_full_stack_package/
    v1172_6d_gpu_full_stack_genesis_provenance_engine.py
```

SHA-256:

```text
659a1489b9c2a46a56440808a0ac19e3f1be8bd44ffb70cfbab575ea1bd95e93
```

Type:

```text
hash/root/event/witness append-only ledger
```

This carries source-origin and ordered-lineage identity but no certified \(U(25)\) support representation.

Status:

```text
NONE_CERTIFIED
```

for a natural map to the v14.03 support.

### 4.2 Genesis 6-D field carrier

The same frozen v1172 artifact also contains a nontrivial real 6-D Genesis/pruning field on its own grid carrier.

This is a genuine nontrivial carrier, but its certified transformations are model-specific grid/pruning transformations. The archived file contains no certified natural map from that carrier to the fixed 25-dimensional compatibility support used by v14.03.

Status:

```text
NONE_CERTIFIED
```

### 4.3 Protected retained source grade

Artifact:

```text
ResearchHistory/UQCF-GEM/v13/v13.26/REPORT.md
```

SHA-256:

```text
3677e07ab0ea9c40b5f9615673736027834d93260d149419605535aa14996858
```

Type:

```text
retained scalar/extensive source grade
```

This is support-gauge-trivial scalar information and therefore falls under the Class-A centrality obstruction if used by itself.

### 4.4 Retained graph source/current carrier

The same frozen v13.26 source package also carries the nontrivial graph source/current structure

\[
BJ=s.
\]

This is a different representation space with its own graph balance/covariance structure. No frozen natural intertwiner from that graph/source-current carrier to the v14.03 support carrier is certified in the audited artifact.

### Inventory result

```text
candidate classes audited               = 4
missing frozen artifacts                = 0
nontrivial provenance carriers          = 2
certified natural links into Herm(25)   = 0
```

This is an archive result scoped to the audited frozen candidates. It is not a theorem that no future provenance representation can exist.

---

## 5. Supplied-intertwiner positive/ambiguity control

To distinguish

```text
"the target representation is impossible"
```

from

```text
"the missing information is the relative representation link"
```

v14.04 includes a declared-intertwiner control.

A small 3-dimensional Hermitian provenance-carrier fixture

\[
P_{\rm prov}\in\mathrm{Herm}(3)
\]

is mapped into the fixed support by explicitly supplied isometries

\[
J_i:\mathbb C^3\rightarrow\mathbb C^{25},
\qquad
J_i^\dagger J_i=I_3.
\]

Three predeclared deterministic seeds were sufficient:

```text
14041
14042
14043
```

All three supplied isometries satisfy their constraint, with

```text
max isometry error = 4.621011054697887e-16.
```

For each,

\[
P_i=J_iP_{\rm prov}J_i^\dagger
\]

was passed through the unchanged v14.03 pipeline.

All three produced:

```text
NONZERO_HIDDEN_COMPONENT
simple first PSD contact
rank-1 / RAY intrinsic normal
non-null oriented dual representative
```

So a declared representation link is sufficient to make the downstream v14.03 machinery operative.

But the three links are not equivalent.

Minimum pairwise support-source projective residual:

```text
0.99873115934039
```

Maximum hidden-direction separation:

```text
1.2767684478604349
```

Maximum first-contact boundary separation:

```text
0.023756216192420524
```

Maximum dual-ray separation:

```text
1.036259217478033
```

Pairwise records:

```text
J(14041) vs J(14042):
  projective residual       = 0.9990295589466225
  hidden separation        = 1.2767684478604349
  boundary separation      = 0.023756216192420524
  dual separation          = 1.0001584873919889

J(14041) vs J(14043):
  projective residual       = 0.99873115934039
  hidden separation        = 1.0319608247920389
  boundary separation      = 0.01699612972933345
  dual separation          = 1.036259217478033

J(14042) vs J(14043):
  projective residual       = 0.9987603452271447
  hidden separation        = 1.1872546201546992
  boundary separation      = 0.021272160805405275
  dual separation          = 0.9822467325272016
```

This is **not** evidence that Genesis chooses any of these three intertwiners. It proves the opposite architectural point: holding the provenance-side input and the compatibility fiber fixed while changing only the supplied relative embedding materially changes the physical candidate source ray and its downstream selections.

Therefore the relative representation link is genuine missing information.

---

# III. Interpretation

## 6. What the obstruction means

After v14.03, the unresolved upstream arrow was

\[
\text{Genesis/provenance}
\;?\;\longrightarrow
[P]_+.
\]

v14.04 now resolves what kind of object is missing.

Gauge-trivial provenance cannot select a nontrivial support ray because full support naturality collapses it to the center:

\[
\text{gauge-trivial provenance}
\rightarrow
P\propto I
\rightarrow
\text{PGRL-null}.
\]

Richer provenance structures do exist, but they live in other representation spaces. To use one as a v14.03 source requires a relative representation map/intertwiner

\[
J:\mathcal K_{\rm prov}\rightarrow\mathcal H_{\rm supp}.
\]

The current frozen ontology does not select that \(J\).

Thus the upstream architecture is now

\[
\boxed{
\text{Genesis/provenance}
\rightarrow
\text{nontrivial provenance carrier}
\xrightarrow{\;\text{missing natural }J\;}
[P]_+
\rightarrow
X_*
\rightarrow
[g].
}
\]

This is more precise than a generic statement that the source lift is unknown. The missing object is now localized as a **representation/intertwiner law** between two already-existing typed structures.

## 7. Why this is not just a coordinate choice

v14.03 already proved covariance under a simultaneous support-coordinate transformation of

```text
X0, hidden modes, P, boundary, and dual representative.
```

That is a gauge change.

v14.04 instead varies \(J\) while holding the fixed compatibility support structure unchanged. This changes the **relative orientation of the provenance carrier inside the support carrier**. The strong pairwise downstream differences therefore cannot be removed by simply relabeling the support coordinates.

That is exactly why the missing intertwiner is structural information rather than gauge bookkeeping.

---

# IV. Unresolved physical claims and preserved results

## 8. Preserved results

Nothing in v14.04 retracts the prior stack.

### v14.03 remains valid

Conditional on supplied \([P]_+\):

\[
[P]_+
\rightarrow
[\Pi_{\rm hid}\dot X_P]
\rightarrow
X_*(P)
\rightarrow
[g(P)]
\]

remains certified.

### v14.02 remains valid

A specified smooth first-contact boundary carries an objective-independent local intrinsic dual ray in the frozen audited compatibility fibers.

### v14.01 remains valid

Arbitrary state-weighted source→higher-incidence maps remain nonunique under the frozen rules.

### v13.26 remains valid

Absolute retained-to-observer source calibration is not derived. v14.04 is fully projective and does not attempt to fix source magnitude.

### v13.28 remains valid

Absolute downstream source→geometry coupling remains stopped pending a new axiom or independent calibration.

## 9. Not derived

v14.04 does **not** derive:

- a natural Genesis/provenance → v14.03 support-source intertwiner;
- absolute source magnitude or observer calibration;
- a physical statement that PGRL evolution reaches the radial boundary;
- source-to-solder/coframe response;
- stress-energy;
- absolute source→geometry coupling;
- physical metric or spacetime;
- Einstein equations;
- Pillar 3 closure.

## 10. Scientific classification

The exact theorem is:

\[
\boxed{
\text{support-gauge-trivial provenance}
\Longrightarrow
\text{central projective support source}
\Longrightarrow
\text{PGRL-null}.
}
\]

The reproducible archive/computation result is:

```text
nontrivial frozen provenance carriers exist                  YES
certified natural provenance→25D support link found          NO
supplied isometry/intertwiner can produce valid v14.03 chain YES
different supplied intertwiners give inequivalent outputs    YES
```

Therefore:

\[
\boxed{\texttt{REQUIRES\_NEW\_REPRESENTATION\_LINK}}.
\]

This is a **major structural no-go and branch-stop result relative to the audited frozen ontology**, not a broad scientific breakthrough.

```text
scientific_breakthrough = false
Pillar_3 = OPEN
```

---

# V. Stop rule

Do **not** open the next gate by trying another arbitrary embedding.

Specifically prohibited as a continuation of this frozen branch:

- reshaping provenance arrays into `25x25` matrices;
- choosing a Fourier transform merely because dimensions can be matched;
- PCA/SVD-based alignment;
- random or hand-picked isometries;
- optimizing the representation against the v14.03 dual ray;
- fitting against ADM/Einstein residuals or gravitational observables.

A continuation is lawful only if one of the following occurs:

1. a genuinely new representation axiom is proposed, independently motivated, explicitly labeled **NEW ASSUMPTION**, and user-approved;
2. a previously frozen artifact is discovered that already defines the required natural intertwiner; or
3. an independently motivated information-theoretic/quantum structure canonically identifies the provenance carrier and compatibility support without consulting the desired downstream result.

Until then the provenance→support representation branch is stopped.
