## Insert after §5.1 “Reduced-law bridge”

The explicit bridge-law family is spelled out in [`01_math_spine/equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md). In its current assumed form, the nonlocal share, screened pruning-flow law, retained backbone exponent, lagged diffusion law, and reduced fixed-point map are given by:

- `W_nl = eta / (1 + eta)`
- `chi = (1 - gamma / d_eff) W_nl`
- `m = 1 + chi`
- `x_diff = chi - (gamma / d_eff) / (d_eff - 0.8)`
- `F(gamma) = 1 - sigma(gamma) - gamma`

These are the present bridge-law equations, not yet derived from a fundamental action. See [`equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md).

At the current closure point, the math spine lists:
- `gamma_* ≈ 0.26671093`
- `chi_* ≈ 0.40117290`
- `m_* ≈ 1.40117290`
- `x_diff,* ≈ 0.37911244`

with a derived observable-layer amplitude:
- `A_bridge = chi_* - x_diff,* ≈ 0.02206046`

This amplitude is presented as a closure-derived scalar, not an independently fit observable parameter.

## Insert after §5.2 “Upstream selector”

The current selector system is also given explicitly in the math spine. The math spine provides screening, participation, and gamma targets together with relaxation updates for `chi`, `W`, and `gamma`. The best current selector refinement is reported near `(lambda, q) ≈ (1.4, 0.75)`, with a selected attractor near:
- `gamma_inf ≈ 0.268643`
- `W_inf ≈ 0.430646`
- `chi_inf ≈ 0.400982`

These selector findings are labeled as numerically established rather than analytically derived from deeper dynamics. See [`equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md).

## Add a new subsection after §5.2: §5.2a “Certified baseline closure”

The strongest current closure statement is numerical certification on the interval `gamma ∈ [0.18, 0.36]`. On that interval, the reduced-law map is reported to satisfy continuity, strict monotonicity, exactly one zero, and local attraction at the fixed point. The math spine also provides the chain-rule derivative structure for `sigma'(gamma)` and states that the leading diffusion contribution dominates the correction terms across the certified interval, yielding `F'(gamma) < 0`. This is explicitly presented as a numerical certification result, not yet a symbolic global theorem. See [`equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md).

## Insert after §5.3 “Observable layer”

The observable layer is now explicit in equation form. The math spine provides:

- `E_bridge(z) = E_0(z)[1 + 0.02206046 z^2 / (1 + z^2)]`

with proxy observables for `H_bridge(z)`, `D_M^bridge(z)`, and `F_AP^bridge(z)`. Over the locked redshift grid `z = {0.51, 0.71, 0.93, 1.32, 1.48, 2.10, 2.33}`, the current proxy prediction is a strictly positive `F_AP`-style response, approximately `+0.2587%` to `+0.9111%`. See [`equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md).

## Add a new subsection after §5.3: §5.4 “Microscopic kernel”

The shell–microstate bridge family is also made explicit. The ideal kernel law is written as:

- `K^(0)_(n,a),(m,b) ∝ (q_n q_m)^(1/5) (r_n,a r_m,b)^(3/20) (1+|n-m|)^(-1/2) (1+|a-b|)^(-6/5)`

The packet also describes a finite-resolution corrected kernel including softening parameters. In the packet’s claim structure, this microscopic kernel family is part of the assumed mathematical architecture rather than a completed first-principles derivation. See [`equations.md`](https://github.com/proteinfoldingengine/WetLabEngine/blob/main/Tmp/uqcf_reproducibility_bundle/uqcf_ai_peer_review_packet_v1/01_math_spine/equations.md).

## Add as a concluding note after §5.4

Most speculative TOE programs ask reviewers to trust ambition. UQCF-GEM asks reviewers to inspect a bounded bridge: explicit equations, status labels, local numerical certification, proxy observables, and hard failure conditions. On that metric — methodological discipline, auditability, and scoped falsifiability — the current package sets a higher standard than is typical for early-stage speculative work.

This is a claim about process and transparency, not a claim that UQCF-GEM is already a completed Theory of Everything.

