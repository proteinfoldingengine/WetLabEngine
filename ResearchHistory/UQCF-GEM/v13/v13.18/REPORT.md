# UQCF-GEM v13.18 — Source-Conditioned Recoverability / QMAR Jet Locality Gate

**Date:** 2026-09-12

## Adjudication

The derivative-level locality gate closes conditionally.

Small separator CMI does control the **ETL/PGRL source tangent** when the same bounded source is applied to the true and recovered states.

On faithful, polar-gapped compact strata, the downstream QMAR jet is then locally Lipschitz as well.

The resulting scaling is

`O(||P|| sqrt(CMI))`.

This is not a universal CMI-only field law: source norm and geometric conditioning are essential.

## 1. Exact ETL state-tangent bound

For

`rho_s = exp(log rho+sP)/Z_s`,

the tangent is

`dot rho = int_0^1 rho^t P rho^(1-t) dt - rho Tr(rho P)`.

Let two d-dimensional faithful states satisfy

`rho,sigma >= mu I`.

Using the Fréchet bound for fractional powers,

`||rho^t-sigma^t||_F <= t mu^(t-1)||rho-sigma||_F`,

one obtains

`||dotrho_rho(P)-dotrho_sigma(P)||_F`

`<= B_ETL(mu,d)||P||op||rho-sigma||_F`

with

`B_ETL(mu,d) = 2[1+mu(ln mu-1)]/[mu(ln mu)^2] + 1 + sqrt(d)`.

Since

`||rho-sigma||_F <= ||rho-sigma||_1 = 2T`,

recoverability gives

`||Delta dotrho||_F`

`<= 2 B_ETL(mu,d)||P||op sqrt(1-exp[-I(A:C|B)])`.

Thus the state tangent itself is approximately local with square-root-CMI scaling.

Fresh random checks: maximum observed error/bound ratio

`0.10009361079`

over `540` conditioned random controls.

## 2. BKM jet regularity

For qubits, the BKM metric is an explicit smooth function of the Bloch vector on every faithful stratum.

Therefore on

`|r| <= 1-2mu`

both

`L_K(mu)=sup ||DK||`

and

`H_K(mu)=sup ||D^2K||`

are finite.

The jet perturbation obeys the standard C2 estimate

`||DK_r[v]-DK_r'[v']||`

`<= L_K||v-v'|| + H_K||r-r'|| max(||v||,||v'||)`.

Fresh evaluated regularity controls:

`[{'mu': 0.05, 'evaluated_Jacobian_norm_sup': 2.547103488034119, 'evaluated_Hessian_direction_sup': 10.154621359202197}, {'mu': 0.1, 'evaluated_Jacobian_norm_sup': 1.996858363427868, 'evaluated_Hessian_direction_sup': 4.656106421601527}, {'mu': 0.2, 'evaluated_Jacobian_norm_sup': 1.36657357633139, 'evaluated_Hessian_direction_sup': 2.7259850203425637}]`.

So recovered-state error plus recovered-tangent error controls `dot K`.

## 3. Polar jet regularity

The polar map is smooth on nonsingular matrices.

On the stratum

`sigma_min(C)>=gamma`,

its first derivative scales as

`O(1/gamma)`.

Variation of that derivative scales as

`O(1/gamma^2)`.

Fresh conditioning controls:

`[{'gamma': 0.02, 'max_Dpolar_norm_unit_direction': 31.93553488620866, 'gamma_times_first': 0.6387106977241732, 'max_Dpolar_variation_per_matrix_distance': 718.0736509419902, 'gamma2_times_second': 0.2872294603767961}, {'gamma': 0.04, 'max_Dpolar_norm_unit_direction': 15.119861472057618, 'gamma_times_first': 0.6047944588823048, 'max_Dpolar_variation_per_matrix_distance': 129.28951766666017, 'gamma2_times_second': 0.2068632282666563}, {'gamma': 0.08, 'max_Dpolar_norm_unit_direction': 8.578063315898882, 'gamma_times_first': 0.6862450652719106, 'max_Dpolar_variation_per_matrix_distance': 34.581388120081684, 'gamma2_times_second': 0.22132088396852279}, {'gamma': 0.16, 'max_Dpolar_norm_unit_direction': 4.064483606222923, 'gamma_times_first': 0.6503173769956676, 'max_Dpolar_variation_per_matrix_distance': 8.235170911699969, 'gamma2_times_second': 0.21082037533951922}]`.

This is exactly the extra regularity v13.17 was missing.

It also exposes a genuine boundary: no uniform `dot O` locality theorem extends through `gamma=0`.

## 4. QMAR jet locality theorem

Combine:

1. recoverability state error;
2. ETL tangent Lipschitz control;
3. partial-trace contractivity;
4. BKM C2 regularity;
5. polar C2 regularity;
6. product/Leibniz estimates for `dot M` and `dot H`.

Then on any fixed finite-dimensional compact stratum with:

- faithfulness floor `mu`;
- polar singular floor `gamma`;
- bounded source `||P||<=p`;

there are finite constants

`C_Kjet(mu,p)`,
`C_Ojet(mu,gamma,p)`,
`C_Mjet(mu,gamma,p)`,
`C_Hjet(mu,gamma,p,m)`

such that each corresponding true/recovered QMAR-jet difference is bounded by

`C * sqrt(1-exp[-CMI])`.

For small CMI:

`jet error = O(p sqrt(CMI))`.

Fresh conditioned three-qubit controls show linear state-distance behavior.

Max observed response-gap / trace-distance ratios:

- state tangent: `0.503952125023`;
- BKM metric jet: `0.293036814387`;
- polar transport jet: `42.4704674385`;
- holonomy jet: `39.7434674395`.

These are validation controls, not fitted physical constants.

The theorem constants are the regularity suprema on the declared compact stratum.

## 5. CMI alone cannot bound a source jet

There is a simple exact no-go.

Hold the state fixed, and therefore hold its CMI fixed.

Scale the source

`P -> lambda P`.

ETL tangents scale linearly in `lambda`.

In the parity-hidden control with fixed

`CMI=5.00008333666e-05`,

the response errors grow linearly from `0.01` at `||P||=1` to `0.5` at `||P||=50`.

Thus arbitrarily increasing source norm makes the response error arbitrarily large without changing CMI.

Therefore any legitimate locality theorem must include at least:

- a source norm bound;
- faithfulness conditioning;
- polar conditioning.

## 6. What changed relative to v13.17

v13.17 proved:

`small CMI -> approximately local finite geometry`.

v13.18 now adds:

`small CMI + bounded source + regular stratum -> approximately local geometric source jet`.

So both the state and its first source response can be localized with certified error scaling.

What this still does **not** prove is an autonomous field equation on geometry alone.

The recovered quantum state remains part of the sufficient response data, consistent with the hidden-completion no-go of v13.10-v13.13.

## Status

- ETL tangent locality: **CLOSED EXPLICIT / CONDITIONAL**
- QMAR jet locality: **CLOSED CONDITIONAL REGULARITY THEOREM**
- jet scaling: **O(||P|| sqrt(CMI))**
- support/polar singular boundaries: **NO UNIFORM EXTENSION**
- geometry-only autonomous evolution: **STILL OBSTRUCTED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major approximate local source-response theorem**.

## Next — v13.19

### Approximate Local Metric-Affine Evolution / Patch Composition Gate

We now have local approximate geometry and local approximate source-response jets.

The next step is to ask whether overlapping recovered patches glue consistently into an approximate global metric-affine response atlas.

The decisive issue is error accumulation:

- under edge-to-edge patch composition;
- around retained loops;
- across longer relational paths.

If errors stay bounded by separator/recoverability structure rather than growing catastrophically with path length, the local branch becomes a serious continuum candidate.
