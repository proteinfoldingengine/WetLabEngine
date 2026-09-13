# v15.05 — Frozen Composition-Law Audit / Monoidal Non-Selection and Log-Selector Boundary

**Status:** CLOSED / measured on branch; archive binding and final exact-SHA certification pending  
**Primary outcome:** `FROZEN_COMPOSITION_LAWS_DO_NOT_SELECT_SPECTRAL_RESPONSE`  
**Secondary outcome:** `LOG_SHAPE_REQUIRES_NEW_FUNCTIONAL_CALCULUS_ASSUMPTION`  
**Major structural result:** `true`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

v15.04 classified every local qubit source law compatible with independent local-unitary covariance as

\[
F_{\rm tr}(\rho)=a(r)\left(\rho-\frac12I\right),
\qquad r=|\mathbf r|.
\]

The remaining question was whether an **already-frozen composition law** removes the freedom in \(a(r)\), without choosing a response because it improves a later PGRL, ADM, Einstein, cosmology, or empirical score.

The answer is

\[
\boxed{\texttt{FROZEN\_COMPOSITION\_LAWS\_DO\_NOT\_SELECT\_SPECTRAL\_RESPONSE}}.
\]

A stronger state-to-source composition principle can select the logarithmic shape, but that principle is **not present in the frozen ontology**. It is therefore a candidate new axiom or new derivation target, not a result that may be retroactively attributed to the current stack.

---

# I. FROZEN COMPOSITION / NATURALITY AUDIT

The audit binds the archived dependencies by Git blob SHA and separates their typed roles.

## v13.04 — polar tensor naturality

The frozen exact identity

\[
\operatorname{polar}(C_1\otimes C_2)
=
\operatorname{polar}(C_1)\otimes\operatorname{polar}(C_2)
\]

is a theorem about **polar transport** on independent tensor products. It does not define a state-to-source map \(\rho\mapsto F(\rho)\), and therefore cannot constrain \(a(r)\).

## v13.22 — quantum refinement naturality

The frozen lawful family is

\[
R_\tau(\rho)=\rho\otimes\tau,
\qquad
C=\operatorname{Tr}_{\rm anc},
\]

with ETL/PGRL source naturality

\[
P\longmapsto P\otimes I.
\]

This is important, but the typing is decisive: \(P\) is already an independent supplied source variable. The law tells how an existing \(P\) embeds under refinement. It does **not** define

\[
P=F(\rho)
\]

and does not assert a state-to-source equation such as

\[
F(\rho\otimes\tau)
=
F(\rho)\otimes I+I\otimes F(\tau).
\]

The exact identity

\[
\log(\rho\otimes\tau)
=
\log\rho\otimes I+I\otimes\log\tau
\]

used in v13.22 proves naturality of the **PGRL exponential family once a source has already been supplied**. It does not prove that the source itself must be \(\log\rho\).

## v13.23 — QRSL branch stop

The canonical quantum refinement selector remains irreducible relative to the current frozen ontology. No hidden-refinement selection principle recovered there supplies the stronger state-to-source law required here.

## v13.26 — source-scale freedom

PGRL retains the exact reparameterization

\[
P\to aP,
\qquad
t\to t/a,
\]

so absolute source normalization is not selected by the state family.

## v14.03 — projective source ray

A supplied positive projective support source ray \([P]_+\) conditionally selects the hidden response / first-contact / dual-ray chain. Its origin remains upstream. v14.03 therefore consumes a source ray; it does not derive the spectral state-to-source function.

## v15.03 — anti-circularity rule

The frozen stop rule explicitly forbids privileging `log rho` merely because PGRL is written in logarithmic coordinates.

## v15.04 — exact remaining freedom

Local covariance leaves

\[
F_{\rm tr}(\rho)=a(r)(\rho-I/2)
\]

with no unique \(a(r)\).

Therefore the frozen dependency audit is

\[
\boxed{\texttt{NO\_FROZEN\_STATE\_TO\_SOURCE\_COMPOSITION\_SELECTOR}}.
\]

---

# II. LABELED MONOIDAL COMPOSITION DOES NOT SELECT \(a(r)\)

There is a stronger negative result than a simple archive search.

Suppose the tensor factors are already labeled and a local covariant source law \(F_a\) has already been chosen. Define its source on a product state by the standard local sum

\[
\mathcal M_a(\rho_1\otimes\cdots\otimes\rho_n)
=
\sum_i
I\otimes\cdots\otimes F_a(\rho_i)\otimes\cdots\otimes I.
\]

For **every** local response function \(a(r)\), this construction is:

- associative under regrouping of labeled factors;
- natural under permutation/swap of factors;
- covariant under independent local unitaries.

These properties follow from tensor algebra, not from a special choice of \(a(r)\).

Therefore

\[
\boxed{
\text{monoidal composition of already-chosen local sources}
\;\not\Rightarrow\;
\text{selection of the local source law}
}.
\]

Equivalently,

\[
\boxed{\texttt{LABELED\_MONOIDAL\_COMPOSITION\_PRESERVES\_ARBITRARY\_LOCAL\_SPECTRAL\_RESPONSE}}.
\]

### Executed witnesses

The audit used three v15.04-lawful local responses:

\[
a_{\rm lin}(r)=1,
\]

\[
a_{\log}(r)=\frac{2\operatorname{artanh}(r)}{r},
\]

and

\[
a_{\rm poly}(r)=1+r^2.
\]

For deterministic faithful qubits with radii approximately \(0.15\) and \(0.72\), all three monoidal constructions passed:

```text
max local covariance error = 8.588717521894646e-16
max associativity error    = 2.3551386880256624e-16
max swap-naturality error  = 0.0
```

Yet the resulting two-site source rays remained pairwise distinct:

```text
linear vs log        = 0.04038732286659571
linear vs polynomial = 0.06600014410325687
log vs polynomial    = 0.025621359948040462
```

The minimum pairwise separation was

`0.025621359948040462`.

Thus composition does not accidentally collapse the v15.04 nonuniqueness.

The numerical witnesses validate the implementation. The theorem itself is algebraic.

---

# III. WHAT STRONGER LAW WOULD SELECT THE LOGARITHMIC SHAPE?

Although the frozen laws do not select \(a(r)\), there is a mathematically clean stronger condition that does.

Assume, as an additional principle, that there is one dimension-independent continuous scalar function

\[
f:(0,1)\to\mathbb R
\]

acting by ordinary functional calculus on every faithful finite-dimensional density operator, with centered source map

\[
F_d(\rho)
=
f(\rho)-\frac{\operatorname{Tr}f(\rho)}{d}I_d.
\]

Now additionally require the state-derived source itself to obey the centered tensor derivation law

\[
\boxed{
F_{mn}(\rho\otimes\sigma)
=
F_m(\rho)\otimes I_n
+
I_m\otimes F_n(\sigma)
}.
\]

This is qualitatively stronger than v13.22. It no longer says how an independently supplied \(P\) embeds. It constrains the **function that generates \(P\) from the state**.

## Exact functional-equation consequence

Diagonalize \(\rho\) and \(\sigma\). Taking the difference between two diagonal entries with the same \(\sigma\)-eigenvalue \(y\) cancels all centering constants and gives

\[
f(xy)-f(zy)=f(x)-f(z).
\]

Hence, for fixed \(y\),

\[
f(xy)-f(x)=c(y)
\]

is independent of \(x\). Applying this twice gives

\[
c(yz)=c(y)+c(z).
\]

The density-normalization constraint does not obstruct this conclusion: any two \(x,z\in(0,1)\) with \(x+z<1\) can occur in one faithful finite-dimensional spectrum, and arbitrary pairs can be connected through a sufficiently small intermediate eigenvalue. Likewise any \(y\in(0,1)\) can occur in a faithful spectrum.

Continuity reduces the multiplicative Cauchy equation to

\[
c(y)=\alpha\log y.
\]

Therefore

\[
\boxed{
f(x)=\alpha\log x+\beta}.
\]

The additive constant \(\beta\) vanishes under centering, so the noncentral projective source shape is

\[
\boxed{[F(\rho)]=[\log\rho]}
\]

for \(\alpha>0\). The tensor equation alone does not fix the sign of \(\alpha\); positive-projective orientation requires \(\alpha>0\).

Thus the exact conditional classification is

\[
\boxed{
\texttt{CONTINUOUS\_UNIVERSAL\_SCALAR\_FUNCTIONAL\_CALCULUS\_PLUS\_CENTERED\_TENSOR\_DERIVATION\_SELECTS\_LOG\_SHAPE}
}.
\]

### Executed controls

On the deterministic faithful pair:

```text
centered log tensor error    = 1.6421465606029517e-15
centered linear tensor error = 0.3716732435890426
centered cubic tensor error  = 0.5553605272997411
```

So the implemented finite controls distinguish the logarithmic law exactly as the analytic functional equation predicts.

---

# IV. WHY THIS DOES NOT YET DERIVE `log rho`

The crucial boundary is the premise.

v15.04 classified the general conjugation-equivariant map as a permutation-equivariant spectral assignment. That class is broader than applying one scalar function independently to every eigenvalue in every dimension.

Therefore the assumptions

1. one universal dimension-independent scalar functional calculus;
2. continuity;
3. centered tensor derivation for a state-derived source;

are **additional structure**.

The frozen archive currently contains no theorem deriving those assumptions from Genesis provenance, global compatibility, recoverability order, source grading, PGRL, or the quantum refinement law.

So the correct secondary adjudication is

\[
\boxed{\texttt{LOG\_SHAPE\_REQUIRES\_NEW\_FUNCTIONAL\_CALCULUS\_ASSUMPTION}}.
\]

This is a useful target, not a license to insert `log rho` silently.

---

# V. INTERPRETATION

v15.05 localizes the missing source principle one level further.

The hierarchy is now:

\[
\text{local unitary covariance}
\Rightarrow
\text{spectral blocks/direction},
\]

but not spectral response values;

\[
\text{labeled monoidal composition}
\Rightarrow
\text{consistent composition of an already-chosen local law},
\]

but still not the choice of that law;

while

\[
\text{universal scalar functional calculus}
+
\text{centered tensor derivation}
+
\text{continuity}
\Rightarrow
\log\rho\text{ shape}.
\]

This clarifies the research target. The missing ingredient is not generic tensor-product consistency. It must be a principle strong enough to say that the local state-to-source response is generated by one universal spectral scalar law—or an alternative ontology-native principle of comparable strength.

That principle must be justified upstream. It may not be chosen because the logarithm is convenient for BKM geometry or because it later performs well against gravity.

---

# VI. CLAIM BOUNDARY

v15.05 does **not** derive:

- `log rho` as the frozen Genesis/provenance source law;
- the new universal scalar-functional-calculus premise;
- a unique absolute source normalization;
- an exact retained-node-to-quantum-site factorization;
- a natural graph-site-to-compatibility-parent map;
- physical stress-energy;
- a source-to-coframe/solder law;
- physical metric or spacetime;
- an absolute gravitational coupling;
- Einstein equations;
- physical time;
- Pillar 3 closure.

No downstream gravity/ADM/Einstein/cosmology score was used as a selector. No entropy, pruning, or physical time was used as a pre-pruning source selector.

---

# VII. ADJUDICATION

Primary:

\[
\boxed{\texttt{FROZEN\_COMPOSITION\_LAWS\_DO\_NOT\_SELECT\_SPECTRAL\_RESPONSE}}
\]

Secondary:

\[
\boxed{\texttt{LOG\_SHAPE\_REQUIRES\_NEW\_FUNCTIONAL\_CALCULUS\_ASSUMPTION}}
\]

This is a **major structural result**, not a broad scientific breakthrough.

`scientific_breakthrough = false`  
`Pillar_3 = OPEN`

---

# Stop rule / next lawful question

Do not adopt the centered tensor-derivation equation merely because it selects `log rho`.

The next lawful question is:

> Does the already-earned ontology independently justify a universal scalar functional-calculus state-to-source map, or some alternative state-to-source principle strong enough to select the spectral response, without consulting downstream gravitational behavior?

If no such origin exists, the spectral source response remains irreducible relative to the current frozen ontology and any selected law must be declared **NEW ASSUMPTION**.

## CI evidence before final archive binding

TDD RED:

- checker commit `1bd2ec2fa354b4c2d158edc9884d219a517a503b`
- workflow-bearing RED head `8faeb5165b7a5b54f1dd89e934ab7159a490aa64`
- run `34764847993`
- job `103743883168`
- intended failure: `ModuleNotFoundError: No module named 'composition_selector_audit'`

First GREEN:

- SHA `9eddc0f6cfce26dbbf0b2a30a7e8b2559f5d81b1`
- run `34764922064`
- job `103744080214`
- SUCCESS

Final exact-SHA certification follows frozen-summary binding and frontier updates.
