# HEAT_KERNEL_BASELINE_UNIVERSALITY_TEST.md

# Heat Kernel Baseline Universality Test
## Testing whether the flat heat-coefficient baseline is universal across flat reference geometries

## Status
**Baseline universality diagnostic. Not baseline theorem closure.**

`HEAT_KERNEL_BASELINE_THEOREM.md` stated the key conditional decomposition:

\[
C_{\mathrm{raw},n}(M)
=
B_n(\mathcal R)
+
C_{\mathrm{curv}}(M)
+
E_n(M).
\]

The current heat-curvature route depends on the assumption that the flat reference measures:

\[
B_n(\mathcal R)
\]

rather than a geometry-specific artifact.

This file tests that assumption on flat boundaryless geometries.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving baseline universality.

---

# 1. Test principle

All flat tori satisfy:

\[
R=0.
\]

Therefore:

\[
\int R\,dV=0.
\]

If the graph heat baseline is universal, then flat-torus raw coefficients should vary mainly with:

```text
graph rule
dimension
sample size
sampling noise
```

not strongly with flat aspect ratio.

---

# 2. Reference family

The verifier tests rectangular flat tori:

\[
T^2(L_1,L_2)
\]

with different aspect ratios.

All have zero scalar curvature.

The expected result is not that raw coefficients are zero.

The expected result is:

```text
flat baseline coefficients are stable across flat aspect ratios up to sampling noise
```

---

# 3. Verifier implementation

## Status
**Implemented as `heat_kernel_baseline_universality_verifier.py`. Execution log captured.**

The verifier:
1. samples rectangular flat tori with aspect ratios:
   ```text
   0.75, 1.0, 1.5, 2.0
   ```
2. applies the same \(\alpha=1\) density-normalized graph rule;
3. scales the spectrum by the known first eigenvalue of each rectangular torus;
4. estimates the heat coefficient baseline;
5. compares aspect-ratio spread to seed-level noise.

## Captured verifier output

```text
Heat kernel baseline universality verifier
==================================================
Route:
flat rectangular tori with different aspect ratios -> baseline coefficient stability
No curvature target; all references have R=0.

n,aspect,flat_baseline_coeff_median,flat_baseline_coeff_std,window_cv_median,h_median,spectral_scale_median
90,0.75,1.8293728310449584,13.127149507703747,1.2722854755062354,0.7320163228362312,5.158083665695938
90,1.0,11.777915108621013,9.861103468941433,0.6085456068393981,0.8274537306387706,5.8730215605435
90,1.5,12.506998972463883,13.365308109882221,1.2123058926355064,1.0217851710176107,4.888700671870849
90,2.0,20.173725954011896,4.958255395450461,0.9122384052214138,1.2274861190779256,4.948711470685219
130,0.75,0.5155975398742898,10.368550038140642,1.2215052431161297,0.5915519001360212,5.497965984273719
130,1.0,2.3280742084487462,16.33162745797724,0.8914123882113548,0.7054769228611917,6.0180532031492255
130,1.5,7.378414565537867,17.90491234726339,1.0154322778712062,0.8696838598602441,5.617757742637856
130,2.0,-11.483794021874305,12.154629032479516,2.3866434129986445,0.9946697576788323,4.6753787734504035
n_90_aspect_spread: 6.515847942739462
n_90_seed_noise_median: 11.494126488322589
n_90_aspect_spread_over_seed_noise: 0.5668850042113809
n_130_aspect_spread: 6.921096741048903
n_130_seed_noise_median: 14.243128245228379
n_130_aspect_spread_over_seed_noise: 0.4859253263669144
classification: BASELINE_UNIVERSALITY_PROMISING
```

---

# 4. Interpretation rule

If:

\[
\frac{
\text{aspect-ratio baseline spread}
}{
\text{seed noise}
}
\lesssim 1
\]

then baseline universality is promising.

If this ratio is large, the baseline depends on flat geometry details and the subtraction is not universal enough.

---

# 5. What this establishes

### If promising

Flat baseline subtraction is less likely to be a one-geometry artifact.

### If weak

The current baseline correction is not universal and must be replaced by a better operator/measure normalization.

---

# 6. What remains open

1. Larger refinement ladder.
2. Flat 3-torus baseline.
3. Irregular sampling densities.
4. Theoretical baseline decomposition.
5. Curved magnitude convergence.
6. ADM action integration.

---

# 7. Next derivation target

If promising:

```text
HEAT_CURVATURE_MAGNITUDE_TEST.md
```

If weak:

```text
GRAPH_LAPLACIAN_BASELINE_FAILURE.md
```

---

# Honest status line

> `HEAT_KERNEL_BASELINE_UNIVERSALITY_TEST.md` tests whether the flat heat-kernel baseline is stable across flat torus aspect ratios. It is a necessary diagnostic for the baseline theorem, not a proof of baseline universality.

**End of file.**
