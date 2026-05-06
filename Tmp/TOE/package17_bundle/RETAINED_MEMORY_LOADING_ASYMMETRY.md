# RETAINED_MEMORY_LOADING_ASYMMETRY.md

# Retained Memory Loading Asymmetry
## Testing whether the micro-to-block recursion naturally drives \(q_{\mathrm{block}}=b/(1-a)\approx2.75\text{–}3.3\)

## Status
**Direct bottleneck test. Target loading remains rare under current sampling.**

`CHI_SELECTION_FAILURE_ANALYSIS.md` identified the main failure mode:

```text
ANCHOR_CENTERED_NEAR_LAMBDA_1
```

The block-derived selection functional usually lands near:

\[
\Lambda_{\mathrm{opt}}\approx1,
\qquad
\chi_{\mathrm{opt}}\approx0.5,
\]

because the loading anchor:

\[
q_{\mathrm{block}}=\frac{b}{1-a}
\]

is broadly centered near \(1\).

Target selection requires:

\[
q_{\mathrm{block}}\approx2.75\text{–}3.3.
\]

This file directly tests whether the retained-memory/pruning recursion naturally creates that loading asymmetry.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Loading anchor

The micro-to-block loading map is:

\[
\Lambda_{n+1}=a\Lambda_n+b.
\]

The fixed loading anchor is:

\[
q_{\mathrm{block}}=\Lambda_*=\frac{b}{1-a}.
\]

The bridge coefficient is:

\[
\chi_*=\frac{1}{1+q_{\mathrm{block}}}.
\]

To get:

\[
\chi_*\approx0.2667,
\]

we need:

\[
q_{\mathrm{block}}\approx2.75.
\]

Prior target-hit regimes suggested:

\[
q_{\mathrm{block}}\approx3.3.
\]

So the test window is:

\[
2.75\le q_{\mathrm{block}}\le3.3.
\]

---

# 2. Explicit pruning inputs

From `PRUNING_THRESHOLD_INTEGRALS.md`:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

\[
I_f=I_s
\exp\left(
-\frac{1}{2}
\left(
\frac{\varepsilon^*}{\sigma_\xi}
\right)^2
\right).
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

Therefore:

\[
q_{\mathrm{block}}
=
\frac{
w_s\beta_s I_s+w_f\beta_f I_f
}{
\mathcal G_*
[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
]
}.
\]

This is the key expression.

---

# 3. Verifier implementation

## Status
**Implemented as `retained_memory_loading_asymmetry_verifier.py`. Execution log captured.**

The verifier compares two regimes:

1. **Broad sampling**  
   General positive micro-to-block parameters.

2. **Memory-biased sampling**  
   Stronger retained-memory input, smaller geometry normalization, and less severe fast-channel pruning.

It computes:
- \(q_{\mathrm{block}}\);
- \(\chi_*\);
- target hit rate for \(2.75\le q\le3.3\);
- near-target rate for \(2.4\le q\le3.6\);
- parameter diagnostics for target hits.

## Captured verifier output

```text
Retained memory loading asymmetry verifier
==================================================
Route:
explicit pruning integrals + micro-to-block loading -> q=b/(1-a) distribution

broad_valid_samples: 74865
broad_target_hits_2p75_to_3p3: 1127
broad_target_hit_rate_percent: 1.5053763440860215
broad_near_hits_2p4_to_3p6: 2503
broad_near_hit_rate_percent: 3.3433513657917584
broad_q_median_all: 0.17553275951011793
broad_chi_median_all: 0.8506781218217448
broad_loading_drive_median_all: 0.17553275950955477
broad_G_star_median_all: 0.30487392734473956
broad_memory_input_median_all: 0.09364437647497151
broad_eps_over_sigma_median_all: 1.9985299033466326
broad_If_over_Is_median_all: 0.13573363400045274
broad_target_q_median: 3.00163458100821
broad_target_chi_median: 0.24989788041766936
broad_target_a_median: 0.12198660695972319
broad_target_b_median: 2.6125731028995873
broad_target_loading_drive_median: 3.0016345809912077
broad_target_G_star_median: 0.09304888619570047
broad_target_memory_input_median: 0.425642713581517
broad_target_eps_over_sigma_median: 1.7398882957443078
broad_target_If_over_Is_median: 0.22011489018406866
broad_target_beta_s_median: 0.5455845430595797
broad_target_beta_f_median: 0.27473944834952674
broad_target_sigma_median: 1.5539329352873918
broad_near_q_median: 2.9205216608899565
broad_near_chi_median: 0.2550680971809758
broad_near_a_median: 0.12211250020713382
broad_near_b_median: 2.484265742342554
broad_near_loading_drive_median: 2.9205216608776694
broad_near_G_star_median: 0.0927627095969295
broad_near_memory_input_median: 0.4263795998332962
broad_near_eps_over_sigma_median: 1.6960638696891888
broad_near_If_over_Is_median: 0.2373270040238931
broad_near_beta_s_median: 0.5343902274738956
broad_near_beta_f_median: 0.21310557889959997
broad_near_sigma_median: 1.6004428751284772
broad_naturalness_class: RARE_BUT_PRESENT
memory_biased_valid_samples: 74885
memory_biased_target_hits_2p75_to_3p3: 1902
memory_biased_target_hit_rate_percent: 2.539894504907525
memory_biased_near_hits_2p4_to_3p6: 4232
memory_biased_near_hit_rate_percent: 5.651332042465113
memory_biased_q_median_all: 14.532719099008165
memory_biased_chi_median_all: 0.0643802281896577
memory_biased_loading_drive_median_all: 14.532719098948832
memory_biased_G_star_median_all: 0.14233722350781067
memory_biased_memory_input_median_all: 3.5253770781651808
memory_biased_eps_over_sigma_median_all: 1.0030739280772307
memory_biased_If_over_Is_median_all: 0.6046662339558795
memory_biased_target_q_median: 2.99164457906397
memory_biased_target_chi_median: 0.2505233069340437
memory_biased_target_a_median: 0.08933522751600764
memory_biased_target_b_median: 2.69619454864175
memory_biased_target_loading_drive_median: 2.9916445790512283
memory_biased_target_G_star_median: 0.3850389091547527
memory_biased_target_memory_input_median: 2.098756270123192
memory_biased_target_eps_over_sigma_median: 1.0755665937154273
memory_biased_target_If_over_Is_median: 0.5607827261999365
memory_biased_target_beta_s_median: 0.7713984979120911
memory_biased_target_beta_f_median: 1.0611081596297955
memory_biased_target_sigma_median: 2.6483416366253154
memory_biased_near_q_median: 2.9337759150877556
memory_biased_near_chi_median: 0.25420868438986466
memory_biased_near_a_median: 0.08653838307803899
memory_biased_near_b_median: 2.5878497442817268
memory_biased_near_loading_drive_median: 2.9337759150836087
memory_biased_near_G_star_median: 0.3887049324522912
memory_biased_near_memory_input_median: 2.138953361382151
memory_biased_near_eps_over_sigma_median: 1.0663335995099925
memory_biased_near_If_over_Is_median: 0.5663552933116897
memory_biased_near_beta_s_median: 0.8129074750787195
memory_biased_near_beta_f_median: 0.999430485615717
memory_biased_near_sigma_median: 2.6349991783927527
memory_biased_naturalness_class: RARE_BUT_PRESENT
```

---

# 4. Main result

## Broad sampling

The broad regime gives:

```text
target hit rate: 1.505%
near-target rate: 3.343%
q median: 0.176
chi median: 0.851
```

So under neutral broad priors, the system does **not** naturally sit near the target loading.

The target is:

```text
rare but present
```

not natural.

## Memory-biased sampling

The memory-biased regime gives:

```text
target hit rate: 2.540%
near-target rate: 5.651%
q median: 14.53
chi median: 0.064
```

This is also not natural for the target. It overcorrects: memory loading becomes too strong, driving \(\chi\) too low.

Thus the target appears in a transitional band, not as the default of broad or strongly memory-biased sampling.

---

# 5. Interpretation

The target loading requires a balanced asymmetry:

\[
q_{\mathrm{block}}\sim3.
\]

Broad sampling usually gives too little retained-memory loading:

\[
q_{\mathrm{block}}\ll3.
\]

Strong memory bias often gives too much retained-memory loading:

\[
q_{\mathrm{block}}\gg3.
\]

Therefore the target appears to require an intermediate loading-stabilization principle, not merely "more memory."

---

# 6. Target-hit diagnostics

In broad target hits:

```text
q_median: 3.002
G_star_median: 0.093
memory_input_median: 0.426
eps_over_sigma_median: 1.740
If/Is_median: 0.220
```

In memory-biased target hits:

```text
q_median: 2.992
G_star_median: 0.385
memory_input_median: 2.099
eps_over_sigma_median: 1.076
If/Is_median: 0.561
```

So there are at least two ways to hit the target:

1. lower geometry scale with modest memory input;
2. higher memory input with less fast-channel pruning.

Neither has yet been derived as necessary.

---

# 7. What this file establishes

### Established

1. The required loading asymmetry is explicitly:
   \[
   q_{\mathrm{block}}=\frac{b}{1-a}\approx3.
   \]

2. Broad retained-memory recursion does not naturally produce the target often.

3. Strong memory bias also does not naturally center on the target; it overshoots.

4. The target lies in a transition band between weak-memory and over-memory regimes.

### Not yet established

1. The transition band is not yet derived from a stability condition.
2. The target loading is not yet forced.
3. \(\chi\approx0.2667\) remains rare but reachable.
4. We need a principle selecting intermediate retained-memory loading.

---

# 8. Failure condition

The current result blocks a claim that:

```text
the slow/fast retained-memory recursion naturally selects χ≈0.2667 under broad priors
```

It does not.

The strongest honest statement is:

```text
χ≈0.2667 occurs in a transition band between under-loaded and over-loaded retained-memory regimes.
```

---

# 9. Next derivation target

The next file should be:

```text
ASYMMETRY_SELECTION_PRINCIPLE.md
```

Its job:

Derive a stabilizing principle that selects intermediate loading:

\[
q_{\mathrm{block}}\approx3
\]

instead of either:

\[
q\ll3
\]

or:

\[
q\gg3.
\]

Candidate physical idea:

```text
retained-memory loading must be high enough to stabilize coherence,
but not so high that it overwhelms geometry.
```

That is the likely next theorem.

---

# Honest status line

> `RETAINED_MEMORY_LOADING_ASYMMETRY.md` shows that the target loading \(q_{\mathrm{block}}\approx3\) is rare under broad sampling and not the default under strong memory bias. The target appears to lie in an intermediate stabilization band, so a new asymmetry-selection principle is required.

**End of file.**
