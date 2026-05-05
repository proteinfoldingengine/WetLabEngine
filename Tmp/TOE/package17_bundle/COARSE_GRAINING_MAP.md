# COARSE_GRAINING_MAP.md

# Coarse-Graining Map
## Candidate discrete-to-continuum map for the affine GEM Bridge framework

## Status
**Live derivation target. First coarse-graining pass. Not yet covariantly closed.**

This file attacks the critical continuum seam:

\[
(\{G_e\},\{R_e\},\{\phi_e\})
\longmapsto
(g_{\mu\nu},R_{\mathrm{eff}},\phi_{\mathrm{eff}}).
\]

The immediate goal is narrower than full emergent GR:

> prove or falsify whether the retained-memory scalar used in `CONTINUUM_LIMIT.md` can be identified with the block-level loading ratio from `CHI_FIXED_POINT.md`.

That is:

\[
R_{\mathrm{eff}}\sim\Lambda
=
\frac{\mathcal M}{\mathcal G}.
\]

This file does **not** derive the Lorentzian metric from the microscopic law. It defines the first inspectable coarse-graining prescription and makes its failure conditions explicit.

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

Prior files established the following chain:

```text
CHI_FIXED_POINT.md
        ↓
MICRO_TO_BLOCK_ACTION.md
        ↓
DISCRETE_MEMORY_ACTION.md
        ↓
COEFFICIENT_DERIVATION.md
        ↓
CONTINUUM_LIMIT.md
```

The remaining bottleneck is the coarse-graining map.

The scalar-density continuum action assumes a field:

\[
R_{\mathrm{eff}}(x).
\]

The coefficient derivation assumes:

\[
R_{\mathrm{eff}}\sim\Lambda.
\]

This file asks:

> can \(\Lambda\) be produced as a stable block scalar from the discrete variables?

---

# 2. Discrete input variables

## Definition 1
Let \(\mathcal C\) be the discrete causal/block lattice.

Each microscopic or fine-grained element \(e\in\mathcal C\) carries:

\[
G_e
\]

for geometry-channel weight,

\[
R_e^{(s)},\quad R_e^{(f)}
\]

for slow and fast retained-memory amplitudes, and:

\[
\phi_e
\]

for matter variables.

The total retained-memory magnitude is:

\[
M_e=w_sR_e^{(s)}+w_fR_e^{(f)}.
\]

## Assumption 1
At the block level, \(G_e\) is positive in the continuum regime:

\[
G_e>0.
\]

This is necessary because the loading scalar is normalized by geometry.

## Failure condition 1
If coarse-grained geometry weights can vanish or change sign in the continuum regime, the scalar loading map becomes singular.

---

# 3. Block map for memory loading

## Definition 2
Let \(B(x)\) be a coarse-graining block associated with continuum point \(x\).

Define:

\[
\mathcal G_B
=
\frac{1}{|B|}
\sum_{e\in B}G_e,
\]

\[
\mathcal M_B
=
\frac{1}{|B|}
\sum_{e\in B}M_e.
\]

Then define the block loading scalar:

\[
\Lambda_B
=
\frac{\mathcal M_B}{\mathcal G_B}.
\]

The first-pass continuum retained-memory scalar is:

\[
R_{\mathrm{eff}}(x)
=
\Lambda_B.
\]

## Lemma candidate 1
If:

\[
\mathcal G_B>0,
\]

and both \(\mathcal G_B,\mathcal M_B\) remain finite under block refinement, then:

\[
R_{\mathrm{eff}}(x)=\Lambda_B
\]

is a finite scalar field candidate.

This lemma is structural, not yet covariant.

---

# 4. Matter coarse-graining

## Definition 3
The matter field is block-averaged:

\[
\phi_{\mathrm{eff}}(x)
=
\frac{1}{|B|}
\sum_{e\in B}\phi_e.
\]

For stress-energy sources, the corresponding block-level matter observable is:

\[
\mathcal O_{\mathrm{mat}}(x)
=
\frac{1}{|B|}
\sum_{e\in B}\mathcal O_{\mathrm{mat},e}.
\]

## Derivation target A
Specify which matter scalar \(\mathcal O_{\mathrm{mat}}\) enters the memory action:
- trace-like source,
- density-like source,
- scalar-field energy density,
- or another invariant matter observable.

---

# 5. Geometry coarse-graining target

## Definition 4
The geometry coarse-graining target is:

\[
\{G_e\}
\longmapsto
g_{\mu\nu}(x),
\]

with derived connection and curvature:

\[
\nabla_\mu,\qquad
R_{\mu\nu},\qquad
R.
\]

At first pass, this file does not derive the full metric. It only requires that the same block structure used to define \(R_{\mathrm{eff}}\) is compatible with a future metric map.

## Derivation target B
Construct a metric candidate from:
- block adjacency,
- causal distance,
- discrete curvature measures,
- Regge-like deficit data,
- or averaged geometry weights \(G_e\).

## Failure condition 2
If \(R_{\mathrm{eff}}\) can be block-averaged but no compatible metric map exists on the same blocks, then the scalar memory sector may exist but not as part of a GR continuum limit.

---

# 6. Stability of the scalar coarse-graining map

## Definition 5
The loading scalar is stable under block coarse-graining if the coefficient of variation:

\[
\mathrm{CV}(\Lambda_B)
=
\frac{\mathrm{Std}(\Lambda_B)}{|\mathrm{Mean}(\Lambda_B)|}
\]

remains bounded and decreases or stabilizes under block refinement.

## First-pass criterion
For the structural verifier, require:

\[
\mathrm{CV}(\Lambda_B)<0.5.
\]

This numerical bound is not fundamental. It is a diagnostic threshold for whether the block scalar is well-defined enough to support the continuum ansatz.

## Failure condition 3
If \(\mathrm{CV}(\Lambda_B)\) remains large or grows under coarse-graining, then \(R_{\mathrm{eff}}\sim\Lambda\) is not a stable scalar continuum field.

---

# 7. Locality and nonlocal contamination

## Definition 6
The scalar-density Class A route assumes the retained-memory field is approximately local in the weak-memory regime.

Let \(\nu_{\mathrm{nl}}\) denote a nonlocal contamination strength, measuring how much \(M_B\) is dominated by global or distant blocks rather than local memory loading.

## Admissibility condition
For Class A to survive:

\[
\nu_{\mathrm{nl}}
\ll 1
\]

or at least:

\[
\nu_{\mathrm{nl}}
\]

must remain controlled enough that a local scalar-density approximation is valid.

## Failure condition 4
If retained memory is dominated by nonlocal kernel contributions, then Class A is not the right continuum memory sector and the theory must pivot to Class C:

\[
S_{\mathrm{mem}}^{(C)}
=
\int d^4x\,d^4y\sqrt{-g(x)}\sqrt{-g(y)}
K(x,y)\mathcal O_R(x)\mathcal O_R(y).
\]

---

# 8. Coarse-graining theorem candidate

## Theorem candidate 1
Suppose:

1. block geometry weights satisfy \(\mathcal G_B>0\);
2. retained-memory magnitudes \(\mathcal M_B\) are finite;
3. the loading scalar \(\Lambda_B=\mathcal M_B/\mathcal G_B\) has bounded block variation;
4. nonlocal contamination is controlled;
5. the same block structure supports an emergent metric map.

Then:

\[
R_{\mathrm{eff}}(x)=\Lambda_B
\]

is an admissible retained-memory scalar for the scalar-density continuum action.

This theorem is **not yet proved**, because condition 5 — the emergent metric map — remains open.

---

# 9. Verifier implementation

## Status
**Implemented as `coarse_graining_map_verifier.py`. Execution log captured.**

The verifier tests the structural part of the map:

\[
G_B=\langle G_e\rangle_B,
\]

\[
M_B=\langle M_e\rangle_B,
\]

\[
R_{\mathrm{eff}}=\Lambda_B=\frac{M_B}{G_B}.
\]

It checks:

1. \(G_B>0\);
2. \(M_B\) finite;
3. \(\Lambda_B\) finite;
4. block scalar coefficient of variation below a diagnostic threshold;
5. nonlocal contamination not dominant.

It does not derive \(g_{\mu\nu}\).

## Captured verifier output

```text
Coarse-graining map verifier
==================================================
Map tested:
G_block = <G_e>_B
M_block = <M_e>_B
R_eff   = Lambda_block = M_block / G_block
phi_eff = <phi_e>_B [proxy only]

Sweep results:
PASS: 99.48
SOFT_FAIL: 0.01
HARD_FAIL: 0.51
Lambda_mean_median: 0.5119507072320512
Lambda_cv_median: 0.08170381235391694
R_eff_std_median: 0.040957517533984786
Lambda_mean_min: 0.2740981074470208
Lambda_mean_max: 2.573909536317794
```

---

# 10. What this file establishes

### Established at current proof level

1. A concrete block map for \(R_{\mathrm{eff}}\) is defined.
2. The identification \(R_{\mathrm{eff}}\sim\Lambda\) is no longer purely verbal.
3. The verifier checks whether block-averaged memory loading behaves like a stable scalar.
4. Failure conditions are explicit:
   - singular geometry denominator,
   - unstable block scalar,
   - uncontrolled nonlocality,
   - no compatible metric map.

### Not yet proved

1. The metric \(g_{\mu\nu}\) is not derived.
2. The block structure is not yet shown to be Lorentzian or generally covariant.
3. The diagnostic CV threshold is not fundamental.
4. Nonlocality is modeled only by a proxy.
5. The map is not yet connected to actual Regge/causal-set geometry.

---

# 11. Updated proof-chain status

With this file, the seam chain becomes:

```text
MICROSCOPIC_LAW.md
        ↓
OPERATOR_THEOREM.md
        ↓
CHI_FIXED_POINT.md
        ↓
MICRO_TO_BLOCK_ACTION.md
        ↓
DISCRETE_MEMORY_ACTION.md
        ↓
COEFFICIENT_DERIVATION.md
        ↓
COARSE_GRAINING_MAP.md
        ↓
CONTINUUM_LIMIT.md
```

The next hard seam is no longer \(R_{\mathrm{eff}}\sim\Lambda\) alone.

It is now:

\[
\{G_e\}
\longmapsto
g_{\mu\nu}.
\]

---

# 12. Next derivation target

The next file should be:

```text
EMERGENT_METRIC_MAP.md
```

Its job:

\[
\{G_e,\text{ adjacency/causal data}\}
\longmapsto
g_{\mu\nu},\nabla_\mu,R_{\mu\nu},R.
\]

This is the hardest part of seam 3.

---

# Honest status line

> `COARSE_GRAINING_MAP.md` defines the first concrete block map from discrete geometry and retained-memory variables to \(R_{\mathrm{eff}}\sim\Lambda\), and verifies that this scalar map is structurally viable under sampled local regimes. It does not derive the emergent metric or prove covariance. The next bottleneck is the metric map.

**End of file.**
