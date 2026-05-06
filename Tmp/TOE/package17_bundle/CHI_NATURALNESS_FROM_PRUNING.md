# CHI_NATURALNESS_FROM_PRUNING.md

# Chi Naturalness From Pruning
## Testing whether \(\chi_*\approx0.2667\) emerges naturally from the explicit pruning-threshold integrals

## Status
**Naturalness test. Reachability is not the same as derivation.**

`PRUNING_THRESHOLD_INTEGRALS.md` made the threshold dependence explicit:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

\[
I_f=
\sqrt{\frac{2}{\pi}}\sigma_\xi
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

`CHI_TARGET_PARAMETER_REGIME.md` showed that the target:

\[
\chi_*\approx0.2667
\]

requires:

\[
\Lambda_*\approx2.75.
\]

This file tests whether that regime appears naturally under broad pruning/noise sampling, without solving parameters to force the target.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as proving \(\chi\) from first principles.

---

# 1. Naturalness question

The target relation is:

\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

For:

\[
\chi_*=0.2667,
\]

we need:

\[
\Lambda_*\approx2.75.
\]

The naturalness question is:

> Does broad sampling of the micro-to-block recursion with explicit pruning integrals naturally produce \(\Lambda_*\approx2.75\), or does it require targeted parameter tuning?

---

# 2. Sampling rule

The verifier samples broad positive regimes for:

\[
\alpha_s,\alpha_f,
\beta_s,\beta_f,
w_s,w_f,
c_s,c_f,
\mu_G,
\mathcal G_*,
\sigma_\xi,
\varepsilon^*/\sigma_\xi.
\]

It computes:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

\[
I_f=I_s e^{-(\varepsilon^*/\sigma_\xi)^2/2}.
\]

Then:

\[
a=
\frac{
w_s\alpha_s c_s+w_f\alpha_f c_f
}{\mu_G},
\]

\[
b=
\frac{
w_s\beta_s I_s+w_f\beta_f I_f
}{
\mu_G\mathcal G_*
}.
\]

The fixed point is:

\[
\Lambda_*=\frac{b}{1-a},
\]

\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

No targeted solving for \(b\) is used in this file.

---

# 3. Verifier implementation

## Status
**Implemented as `chi_naturalness_from_pruning_verifier.py`. Execution log captured.**

The verifier checks:

1. broad stable parameter samples;
2. resulting \(\chi_*\) distribution;
3. hit rate near \(\chi_*=0.2667\);
4. parameter features of target hits;
5. whether the target appears natural, rare-but-reachable, or not found.

## Captured verifier output

```text
Chi naturalness from pruning verifier
==================================================
Route:
broad pruning/noise sampling with explicit I_s,I_f -> chi* distribution

valid_samples: 249539
target_hits: 2143
hit_rate_percent: 0.858783596952781
chi_median_all: 0.8527751752703292
chi_p10_all: 0.061434340623868114
chi_p90_all: 0.9983735550437378
Lambda_median_all: 0.17264201515129765
logLambda_distance_median: 3.1382145421049943
hit_a_median: 0.11863619656071525
hit_b_median: 2.4152643015811384
hit_G_star_median: 0.09804365580627097
hit_beta_s_median: 0.5458242221063235
hit_beta_f_median: 0.257958959177852
hit_eps_over_sigma_median: 1.7629387008820712
hit_I_f_over_I_s_median: 0.21140566010193304
hit_sigma_median: 1.678014439167241
naturalness_class: RARE_BUT_REACHABLE
```

---

# 4. Interpretation of naturalness classes

## Definition 1

```text
NATURAL
```

means the target-hit rate is at least 5% under broad sampling.

```text
RARE_BUT_REACHABLE
```

means target hits exist but are below 5%.

```text
NOT_FOUND
```

means no target hits were found.

This classification is heuristic, not a theorem.

---

# 5. What this file establishes

### Established

1. The \(\chi\)-target regime can be tested without targeting \(b\).
2. Explicit pruning integrals can be plugged into the micro-to-block fixed point.
3. The hit rate quantifies naturalness under the chosen sampling prior.
4. Parameter features of target hits are measurable.

### Not yet established

1. The sampling prior is not derived from microscopic physics.
2. Gaussian noise remains an assumption.
3. The target \(\chi\) may be sensitive to priors over \(\beta,\mathcal G_*,\mu_G\).
4. Naturalness is not uniqueness.
5. A low hit rate would not disprove reachability.

---

# 6. Consequence for the GR derivation program

If \(\chi_*\approx0.2667\) is natural, the coefficient branch becomes much stronger.

If it is rare but reachable, then the framework needs an additional principle explaining why the system selects the target loading ratio.

If it is not found, the current micro-to-block route fails to support the target \(\chi\) without new physics.

---

# 7. Next derivation target

The next file should depend on the verifier result:

- if natural: `CHI_SELECTION_PRINCIPLE.md`;
- if rare but reachable: `CHI_SELECTION_PRINCIPLE.md`;
- if not found: `MICRO_TO_BLOCK_FAILURE_ANALYSIS.md`.

In either non-failure case, the next real question is:

\[
\text{What selects }\Lambda_*\approx2.75?
\]

---

# Honest status line

> `CHI_NATURALNESS_FROM_PRUNING.md` tests whether the target \(\chi_*\approx0.2667\) appears naturally under broad pruning/noise sampling. It quantifies naturalness but does not prove first-principles selection.

**End of file.**
