# UQCF-GEM v13.19 — Approximate Local Metric-Affine Evolution / Patch Composition Gate

**Date:** 2026-09-12

## Adjudication

Approximate recovered patches compose stably at finite scale when they are gauge-aligned and tied to one underlying global retained state/reference.

Finite geometry is especially well behaved:

**SO(3) transport, cocycle, holonomy, and transported-metric errors accumulate at most linearly with path length, not exponentially.**

The source-response jet has a stricter boundary:

**holonomy-jet errors admit a quadratic worst-case path-length bound, and explicit controls realize genuine m^2 scaling.**

So a finite recoverability locality horizon is now closed, but scale-independent continuum response closure remains open.

## Finite transport theorem

For exact and recovered polar transports,

`||Ohat_1...Ohat_m-O_1...O_m||_F <= sum_i ||Ohat_i-O_i||_F`.

Random controls: `[{'m': 2, 'max_error_over_sum_edge_errors': 0.9970334860686177}, {'m': 3, 'max_error_over_sum_edge_errors': 0.9940261270902145}, {'m': 5, 'max_error_over_sum_edge_errors': 0.8479375550256888}, {'m': 10, 'max_error_over_sum_edge_errors': 0.6245434056859422}, {'m': 20, 'max_error_over_sum_edge_errors': 0.5285632038828713}, {'m': 40, 'max_error_over_sum_edge_errors': 0.33722539173856014}]`.

Aligned same-axis controls give

`path_error/(m edge_error) = [0.9999999949999999, 0.9999999750000002, 0.9999998950000032, 0.9999995750000542, 0.9999982950008719, 0.9999931750139717]`,

showing the linear scaling is sharp.

## Approximate overlaps and cocycles

Two gauge-aligned recovered estimates of one true transition differ by at most the sum of their errors.

If the exact triple overlap satisfies

`T_ki T_jk T_ij=I`,

then

`||That_ki That_jk That_ij-I|| <= epsilon_ki+epsilon_jk+epsilon_ij`.

Fresh maximum ratios:
- overlap: `0.999872270802`;
- cocycle: `0.971066990934`.

This is the perturbative counterpart of the exact V1698 chart-basis cocycle construction.

## Transported metric/nonmetricity

For

`M_path=K_end-H^T K_start H`,

`||Delta M_path||_F <= eK_end+eK_start+2||K_start||op eH`.

Fresh max ratio: `0.772674627721`.

Since BKM `||K||op<=1`, path metric/nonmetricity error inherits the linear transport bound.

## QMAR jet composition

For

`H=O_1...O_m`,

`dotH=sum_i O_1...dotO_i...O_m`.

With

`epsilon_i=||Delta O_i||`,
`eta_i=||Delta dotO_i||`,
`Lambda_i=max(||dotO_i||,||dothatO_i||)`,

we obtain

`||Delta dotH|| <= sum eta_i + sum_i Lambda_i sum_(j!=i) epsilon_j`.

Uniformly:

`<= m eta + Lambda m(m-1) epsilon`.

Random bound controls: `[{'m': 2, 'max_error_over_jet_bound': 0.7854993141397322}, {'m': 3, 'max_error_over_jet_bound': 0.6867469675626728}, {'m': 5, 'max_error_over_jet_bound': 0.32951827092393604}, {'m': 10, 'max_error_over_jet_bound': 0.21995947008456004}, {'m': 20, 'max_error_over_jet_bound': 0.08119547778358305}]`.

## Quadratic scaling is genuinely attainable

Use

`O_i(s)=R_z(lambda s)`

and

`Ohat_i(s)=R_z(delta+lambda s)`.

The path jet difference scales as `m^2 lambda delta`.

Executed controls:

`[{'m': 2, 'path_jet_error': 7.919595896492028e-05, 'uniform_bound': 9.559797958711672e-05, 'error_over_bound': 0.8284271206040544, 'error_over_m2_delta': 0.09899494870615035}, {'m': 4, 'path_jet_error': 0.0003167838295240044, 'uniform_bound': 0.0004151959588009002, 'error_over_bound': 0.7629742602478278, 'error_over_m2_delta': 0.09899494672625136}, {'m': 8, 'path_jet_error': 0.0012671352167251937, 'uniform_bound': 0.0017263919161084672, 'error_over_bound': 0.7339788867764724, 'error_over_m2_delta': 0.09899493880665576}, {'m': 16, 'path_jet_error': 0.005068539244967785, 'uniform_bound': 0.007036783826243602, 'error_over_bound': 0.720292021202176, 'error_over_m2_delta': 0.09899490712827705}, {'m': 32, 'path_jet_error': 0.02027413102895576, 'uniform_bound': 0.02840956762859387, 'error_over_bound': 0.7136374370073165, 'error_over_m2_delta': 0.09899478041482304}, {'m': 64, 'path_jet_error': 0.08109610890197394, 'uniform_bound': 0.11416313516161443, 'error_over_bound': 0.7103528541605894, 'error_over_m2_delta': 0.0989942735619799}]`.

The quantity

`path_jet_error/(m^2 delta)`

is constant across `m=2,4,8,16,32,64` to better than `2e-5` relative.

So the m^2 scaling is real, even though the conservative coefficient inequality is not exactly saturated.

## Insert v13.17/v13.18 locality bounds

Per edge,

`epsilon_e <= (18/gamma_e) sqrt(1-exp[-I_e])`.

And v13.18 gives

`eta_e <= C_Ojet(mu_e,gamma_e,d,p_e) sqrt(1-exp[-I_e])`.

Therefore finite path geometry obeys a fully explicit summed recoverability certificate, while its source-response jet obeys the double-sum certificate above.

At uniform `gamma=.05`, for example, the value-level edge certificate is about `0.036` at `CMI=1e-8`, `0.114` at `1e-7`, and `0.360` at `1e-6`. Because the path certificate is linear in the number of edges, it eventually becomes non-informative unless the per-edge recoverability error improves with scale.

## Common-reference boundary

Pairwise valid local transitions do **not** automatically form a global atlas.

A control with individually valid SO(3) transitions has pair inverse residual

`1.741e-17`

but triple-cocycle defect

`0.0424248158988`.

Thus approximate global gluing requires either:
1. all recovered patches approximate one common global state/reference, or
2. an independently enforced approximate cocycle law.

## Continuum boundary

For a path with `m` edges:

- value geometry error: `O(m epsilon)`;
- source-response jet error: worst-case `O(m eta+m^2 Lambda epsilon)`.

So fixed microscopic recoverability error cannot remain informative as `m->infinity`.

A continuum/refinement limit needs edge errors to improve with scale, or a new cancellation/renormalization/cocycle theorem.

## Status

- finite transport glue: **CLOSED / LINEAR ERROR**
- approximate cocycle: **CLOSED WITH COMMON REFERENCE**
- transported metric/nonmetricity: **CLOSED / LINEAR ERROR**
- QMAR holonomy-jet glue: **QUADRATIC WORST CASE**
- quadratic jet scaling: **ATTAINABLE**
- finite approximate atlas: **CLOSED CONDITIONAL**
- scale-independent continuum response atlas: **OPEN**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major patch-composition theorem and continuum-scaling boundary**.

## Next — v13.20

### Refinement Error Scaling / Continuum Atlas Stability Gate

Let patch scale be `h` and a fixed physical path have `m(h)~L/h`.

Derive how fast separator CMI, polar conditioning, and edge QMAR errors must improve so that:
- linear value-level atlas errors remain finite or vanish;
- quadratic jet-level atlas errors remain finite or vanish.

Then compare those threshold exponents against archived refinement evidence without fitting.