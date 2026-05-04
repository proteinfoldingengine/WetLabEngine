# Round 15 Methods and Math

## 1. Source locking
The first principle of the Round 15 workflow is that a result cannot be scored until the source anchor is explicit.

For each system, define:
- source PDF
- page number
- observable role

This gives a mapping:
\[
S = (	ext{pdf}, 	ext{page}, 	ext{role})
\]

A source is not usable merely because it mentions the target cluster. It must expose a scoreable observable: profile, map, contour, or table.

## 2. Shared-grid profile scoring (Tier 1)
Let
- \(g(R)\) be the gas-side or X-ray-side proxy
- \(m(R)\) be the lensing / mass-side proxy

Round 15 used a finite grid of radii:
\[
R_1, R_2, \dots, R_N
\]

with extracted values:
\[
g_i = g(R_i), \qquad m_i = m(R_i)
\]

Normalize separately:
\[
	ilde g_i = rac{g_i}{\max_j g_j}
\]
\[
	ilde m_i = rac{m_i}{\max_j m_j}
\]

Pointwise absolute gap:
\[
\Delta_i = |	ilde g_i - 	ilde m_i|
\]

Mean absolute normalized gap:
\[
ar\Delta = rac{1}{N} \sum_{i=1}^{N} \Delta_i
\]

Maximum local gap:
\[
\Delta_{\max} = \max_i \Delta_i
\]

### Prototype classification
\[
	ext{positive_signal} \iff ar\Delta < 0.10
\]
\[
	ext{neutral} \iff 0.10 \le ar\Delta < 0.25
\]
\[
	ext{destructive_failure} \iff ar\Delta \ge 0.25
\]

This is a ranking / gate metric, not a cosmological likelihood.

## 3. Offset scoring (Tier 2)
For each merger component, extract gas and mass peak coordinates in the same frame:
\[
(x_g, y_g), \qquad (x_m, y_m)
\]

Then compute the Euclidean separation:
\[
D = \sqrt{(x_g - x_m)^2 + (y_g - y_m)^2}
\]

If table values are published in angular coordinates, convert them using scale factors:
\[
x_{m kpc} = x_{m arcmin} \cdot s_x
\]
\[
y_{m kpc} = y_{m arcmin} \cdot s_y
\]

Then:
\[
D_{m kpc} = \sqrt{(x_{g,m kpc} - x_{m,m kpc})^2 + (y_{g,m kpc} - y_{m,m kpc})^2}
\]

### Prototype classification
Round 15 used a simple interpretive gate:
- `positive_signal` if both major components show clear nonzero offsets
- `neutral` if only one is compelling
- `destructive_failure` if the extraction collapses or the geometry fails

## 4. Evidence hardening
A result was considered stronger when it advanced from:
- rough manual pass
- to densified pass
- to better manual pass
- to page-locked / table-calibrated pass

This is not a Bayesian hierarchy. It is an evidence-quality ladder.

## 5. Round 15 closeout logic
A round win was justified when all of the following held:
- at least one positive Tier 1 signal
- no catastrophic failures in Tier 1
- at least one positive Tier 2 signal
- Tier 2 evidence hardened beyond the loosest prototype pass
- scaffold stayed frozen

That logic produced the Round 15 decision:
**conditional hardened prototype win**.
