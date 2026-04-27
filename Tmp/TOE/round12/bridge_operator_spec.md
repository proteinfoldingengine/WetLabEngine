# Bridge Operator Specification — Round 12 Frozen Packet

## Purpose
This document defines the exact retained-memory Bridge operator to be used for the Round 12 pre-registered external run.

The intent is to provide a frozen, reproducible operator with no per-galaxy retuning.

## Core claim
A retained-residual + orthogonal correction operator with hidden slow/fast memory states can generate structured corrections to a pure-baryonic baseline without dark-matter halo terms.

## Operator

At each discrete radial step or ordered sample step:

\[
\delta_t = \lambda_t r_t + \xi_t
\]

with retained memory state:

\[
R_t = (1-w)m_t^{(s)} + w m_t^{(f)}
\]

\[
m_{t+1}^{(k)} = (1-\alpha_k)m_t^{(k)} + \alpha_k \phi(|\xi_t|)
\]

\[
\lambda_t = \frac{m_t^{(s)}}{m_t^{(s)} + m_t^{(f)} + \varepsilon}
\]

where:
- \(r_t\) = retained or local residual-driving term at step \(t\)
- \(\xi_t\) = orthogonal / innovation term at step \(t\)
- \(m^{(s)}\) = slow memory mode
- \(m^{(f)}\) = fast memory mode
- \(w\) = mixing weight between slow and fast memory
- \(\phi(\cdot)\) = innovation magnitude transform
- \(\lambda_t\) = adaptive memory weighting
- \(\varepsilon\) = numerical stability constant

## Frozen radial implementation used for galaxy scoring

### Inputs
Per radius \(r_i\), use baryonic components:
- \(V_{\mathrm{gas}}(r_i)\)
- \(V_{\mathrm{disk}}(r_i)\)
- \(V_{\mathrm{bul}}(r_i)\)

Construct baryonic velocity:

\[
V_{\mathrm{bar}}^2(r_i) = \max\left(\mathrm{sign}(V_{\mathrm{gas}})\,V_{\mathrm{gas}}^2 + V_{\mathrm{disk}}^2 + V_{\mathrm{bul}}^2,\ 0\right)
\]

\[
V_{\mathrm{bar}}(r_i) = \sqrt{V_{\mathrm{bar}}^2(r_i)}
\]

\[
g_{\mathrm{bar}}(r_i) = \frac{V_{\mathrm{bar}}^2(r_i)}{r_i + \varepsilon}
\]

### Geometry / component terms
Define:
- disk fraction
- bulge fraction
- component weight
- radial gradient of \(\log g_{\mathrm{bar}}\)
- curvature of \(\log g_{\mathrm{bar}}\)
- outer-gate logistic activation
- low-acceleration factor
- nonlocal smoothing kernel over radius

These produce a frozen Bridge correction term:

\[
\mathrm{corr\_raw}_i =
\beta (1-\lambda_i)\,\mathrm{rw}^{\mathrm{nonlocal}}_i\,\mathrm{low\_acc}_i\,\mathrm{outer\_gate}_i
\left[(1+\zeta\,\mathrm{component\_weight}_i)\,\mathrm{pos\_shape}_i + \eta\,\mathrm{signed\_shape}_i\right]
\]

\[
\mathrm{corr}_i = \tanh(\mathrm{corr\_raw}_i)
\]

\[
g_{\mathrm{bridge},i} = \max\left(g_{\mathrm{bar},i}(1+\mathrm{corr}_i),\ 0\right)
\]

\[
V_{\mathrm{bridge},i} = \sqrt{g_{\mathrm{bridge},i}\,r_i}
\]

## Frozen policy
- No per-galaxy parameter tuning
- No dark-matter halo terms
- No hidden post-hoc smoothing unless explicitly listed in the frozen packet
- Diagnostic ablations must be reported separately from the official frozen result

## Official Round 12 output
For each galaxy:
- baryonic baseline RMSE
- Bridge RMSE
- improvement = baryonic RMSE − Bridge RMSE
- positive improvement flag
- optional diagnostic notes
