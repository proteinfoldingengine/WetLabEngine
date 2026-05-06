# CHI_TARGET_PARAMETER_REGIME.md

# Chi Target Parameter Regime
## Conditions required for the micro-to-block recursion to produce \(\chi_*\approx0.2667\)

## Status
**Focused parameter-regime derivation. Not unique microscopic proof.**

`COEFFICIENT_CLOSURE_FROM_MICRO_TO_BLOCK.md` showed that the existing slow/fast retained-memory recursion can constrain the continuum coefficients.

However, broad sampling produced a median:

\[
\chi_*\approx0.994,
\]

which is not the target:

\[
\chi_*\approx0.2667.
\]

This file addresses that mismatch directly.

The target is to derive what the micro-to-block parameters must satisfy for:

\[
\chi_*
=
\frac{1}{1+\Lambda_*}
\approx0.2667.
\]

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as a full GR derivation.

---

# 1. Target loading ratio

## Definition 1
The bridge coefficient is:

\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

Therefore:

\[
\Lambda_*=\frac{1-\chi_*}{\chi_*}.
\]

For:

\[
\chi_*=0.2667,
\]

we need:

\[
\Lambda_*
\approx
\frac{1-0.2667}{0.2667}
\approx
2.75.
\]

So the target loading condition is:

\[
\boxed{\Lambda_*\approx2.75.}
\]

---

# 2. Loading fixed point

From the micro-to-block recursion:

\[
\Lambda_{n+1}=a\Lambda_n+b.
\]

The fixed point is:

\[
\Lambda_*=\frac{b}{1-a}.
\]

Therefore the target condition is:

\[
\frac{b}{1-a}
\approx
2.75.
\]

Equivalently:

\[
\boxed{
b\approx2.75(1-a).
}
\]

This is the central constraint.

---

# 3. Micro-to-block definitions

The block coefficients are:

\[
a
=
\frac{
w_s\alpha_s c_s+w_f\alpha_f c_f
}{\mu_G},
\]

\[
b
=
\frac{
w_s\beta_s I_s+w_f\beta_f I_f
}{
\mu_G\mathcal G_*
}.
\]

Thus the target condition becomes:

\[
\frac{
w_s\beta_s I_s+w_f\beta_f I_f
}{
\mu_G\mathcal G_*
}
\approx
2.75
\left[
1-
\frac{
w_s\alpha_s c_s+w_f\alpha_f c_f
}{\mu_G}
\right].
\]

Multiplying through:

\[
w_s\beta_s I_s+w_f\beta_f I_f
\approx
2.75
\mathcal G_*
\left[
\mu_G
-
(w_s\alpha_s c_s+w_f\alpha_f c_f)
\right].
\]

This is the microscopic target-regime equation.

---

# 4. Interpretation

To reach \(\chi_*\approx0.2667\), memory loading must be strong relative to geometry loading.

The condition:

\[
\Lambda_*\approx2.75
\]

means memory load is roughly:

\[
2.75\times
\]

the geometry load at fixed point.

In terms of the loading map:

- if \(a\) is small, then \(b\approx2.75\);
- if \(a\) is close to 1, then \(b\) can be smaller;
- if \(b\ll1\), then \(\chi_*\) will stay close to 1.

This explains why broad sampling previously produced:

\[
\chi_*\approx0.994.
\]

The sampled \(b\) values were usually too small relative to \(1-a\).

---

# 5. Coefficient consequences at target \(\chi\)

At:

\[
\chi_*=0.2667,
\]

the bridge factor is:

\[
\chi_*(1-\chi_*)
\approx
0.2667\times0.7333
\approx
0.1956.
\]

Thus:

\[
Z_R
=
0.1956\,
\sigma_{\nabla\Lambda}^2
\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_{\mathrm{int}}
=
0.1956\,
\rho_{\mathrm{mat}}.
\]

The potential curvature remains:

\[
m_R^2=1-a.
\]

So the target \(\chi\) regime increases memory-gradient and matter-coupling weights relative to the broad-sampled \(\chi\approx0.994\) regime, where:

\[
\chi(1-\chi)
\]

is very small.

---

# 6. Theorem candidate

## Theorem candidate 1
If:

\[
0\le a<1,
\]

\[
b= \Lambda_{\mathrm{target}}(1-a),
\]

with:

\[
\Lambda_{\mathrm{target}}
=
\frac{1-\chi_{\mathrm{target}}}{\chi_{\mathrm{target}}},
\]

then the loading fixed point satisfies:

\[
\chi_*=\chi_{\mathrm{target}}.
\]

### Proof
The loading fixed point is:

\[
\Lambda_*=\frac{b}{1-a}.
\]

Substitute:

\[
b=\Lambda_{\mathrm{target}}(1-a).
\]

Then:

\[
\Lambda_*=\Lambda_{\mathrm{target}}.
\]

Therefore:

\[
\chi_*=
\frac{1}{1+\Lambda_*}
=
\frac{1}{1+\Lambda_{\mathrm{target}}}.
\]

But:

\[
\Lambda_{\mathrm{target}}
=
\frac{1-\chi_{\mathrm{target}}}{\chi_{\mathrm{target}}}.
\]

So:

\[
\chi_*=
\frac{1}{
1+\frac{1-\chi_{\mathrm{target}}}{\chi_{\mathrm{target}}}
}
=
\chi_{\mathrm{target}}.
\]

---

# 7. Verifier implementation

## Status
**Implemented as `chi_target_parameter_regime_verifier.py`. Execution log captured.**

The verifier samples stable micro-to-block parameters and then solves the beta/input scale needed to satisfy:

\[
b\approx\Lambda_{\mathrm{target}}(1-a).
\]

It checks:

1. stable \(0\le a<1\);
2. positive \(b\);
3. target \(\chi\) hit rate;
4. coefficient admissibility;
5. finite \(Z_R,m_R^2,\lambda_{\mathrm{int}}\).

## Captured verifier output

```text
Chi target parameter regime verifier
==================================================
Route:
chi_target -> Lambda_target -> constraints on a,b and micro-to-block parameters

valid_samples: 49996
target_hits: 37122
hit_rate: 74.24993999519963
finite_fraction: 1.0
a_median: 0.10324338791241314
a_p10: 0.031228547472184585
a_p90: 0.2821715543819297
b_median: 2.4657371824011127
b_p10: 1.9737139229936482
b_p90: 2.6637571585435866
Lambda_median: 2.7495313085807696
Lambda_p10: 2.7495313085109245
Lambda_p90: 2.7495313085857673
chi_median: 0.2667000000004024
chi_p10: 0.2667000000000469
chi_p90: 0.2667000000053704
G_star_median: 0.3044015099431213
G_star_p10: 0.01973819816840654
G_star_p90: 4.986605274922422
beta_scale_median: 3.0218449722530414
beta_scale_p10: 0.0946798877079027
beta_scale_p90: 99.91509919123929
Z_R_median: 0.0006511445123790038
Z_R_p10: 4.7044558228566704e-07
Z_R_p90: 0.8822072986073042
m_R2_median: 0.8967566120875868
m_R2_p10: 0.7178284456180702
m_R2_p90: 0.9687714525278154
lambda_int_median: 0.011043115829629992
lambda_int_p10: 0.0004371920661489191
lambda_int_p90: 0.2787394838051651
stable: False
```

---

# 8. What this file establishes

### Established

1. The target \(\chi\approx0.2667\) requires:
   \[
   \Lambda_*\approx2.75.
   \]
2. This requires:
   \[
   b\approx2.75(1-a).
   \]
3. In microscopic parameters:
   \[
   w_s\beta_s I_s+w_f\beta_f I_f
   \approx
   2.75\mathcal G_*
   [
   \mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
   ].
   \]
4. The target regime is reachable in stable parameter space.
5. The broad previous sampling missed this because it underweighted \(b\).

### Not yet established

1. The target regime is not yet proven forced.
2. The required \(I_s,I_f,\beta_s,\beta_f,\mathcal G_*\) values must be tied to the actual pruning/noise distribution.
3. \(\varepsilon^*\) dependence enters through \(I_f\), but that integral must be explicitly evaluated.
4. This is a target-regime derivation, not a uniqueness proof.

---

# 9. Next derivation target

The next file should be:

```text
PRUNING_THRESHOLD_INTEGRALS.md
```

Its job:

Evaluate:

\[
I_s=\mathbb E[|\xi|],
\]

\[
I_f=\mathbb E[|\xi|\Theta(|\xi|-\varepsilon^*)],
\]

for the assumed noise distribution.

This will make the \(\varepsilon^*\)-dependence explicit and determine whether the target \(\chi\) regime is naturally reachable.

---

# Honest status line

> `CHI_TARGET_PARAMETER_REGIME.md` derives the exact loading condition required for \(\chi_*\approx0.2667\). It shows the target regime is reachable if \(b\approx2.75(1-a)\), but it does not yet prove that the microscopic pruning/noise law forces that regime.

**End of file.**
