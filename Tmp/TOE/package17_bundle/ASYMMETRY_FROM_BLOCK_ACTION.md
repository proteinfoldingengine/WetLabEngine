# ASYMMETRY_FROM_BLOCK_ACTION.md

# Asymmetry From Block Action
## Testing whether \(A/B\approx7.5\text{–}9.5\) and \(q_0\approx3\) follow from block-action quantities

## Status
**Decisive asymmetry test. Current result: not derived under the tested block mapping.**

`ASYMMETRY_SELECTION_STATUS.md` identified the next decisive theorem target:

\[
A/B\approx7.5\text{–}9.5,
\qquad
q_0\approx3.
\]

If those quantities can be derived from the block action, then the \(\chi\approx0.2667\) selection story becomes much stronger.

If they cannot, then \(\chi\approx0.2667\) remains selection-plausible but not derived.

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

# 1. Source quantities

From the micro-to-block branch:

\[
K_U=K_t(1-a),
\]

\[
K_x=K_t\chi(1-\chi)\sigma_{\nabla\Lambda}^2,
\]

\[
K_{\mathrm{int}}=K_t\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

The loading anchor is:

\[
q=\frac{b}{1-a}.
\]

The goal is to derive the asymmetry-selection inputs:

\[
A/B,
\qquad
q_0.
\]

---

# 2. Candidate block-derived asymmetry map

## Definition 1
Use the minimal block-derived mapping:

\[
A=K_U+K_{\mathrm{int}}+K_x,
\]

\[
B=K_U.
\]

Then:

\[
\frac{A}{B}
=
1+
\frac{K_{\mathrm{int}}+K_x}{K_U}.
\]

For \(A/B\approx7.5\text{–}9.5\), this requires:

\[
\frac{K_{\mathrm{int}}+K_x}{K_U}
\approx6.5\text{–}8.5.
\]

That is a very strong interaction/coherence excess over the restoring memory potential.

## Definition 2
Define the candidate internal loading scale:

\[
q_0
=
q
\frac{
1+K_{\mathrm{int}}/K_U
}{
1+K_x/K_U
}.
\]

This allows matter-memory interaction to push the internal preferred loading upward, while spatial coherence pressure can offset it.

These are candidate identifications, not guaranteed unique.

---

# 3. Verifier implementation

## Status
**Implemented as `asymmetry_from_block_action_verifier.py`. Execution log captured.**

The verifier samples broad micro-to-block parameters and computes:

\[
A/B,
\qquad
q_0,
\qquad
q,
\qquad
\chi.
\]

It tests whether the joint target appears:

\[
7.5\le A/B\le9.5,
\]

\[
2.75\le q_0\le3.3.
\]

## Captured verifier output

```text
Asymmetry from block action verifier
==================================================
Route:
block constants -> derived A/B and q0 -> check target asymmetry

valid_samples: 149702
joint_AoverB_q0_hits: 0
joint_hit_rate_percent: 0.0
q_target_hits: 2313
q_target_hit_rate_percent: 1.5450695381491228
A_over_B_median_all: 1.0084773693271405
A_over_B_p90_all: 1.3270892805064372
A_over_B_p99_all: 2.757816717495087
q0_median_all: 0.16450296031662284
q0_p90_all: 14.971886602722599
q_median_all: 0.17173892183619727
chi_median_all: 0.8534324339681527
K_int_over_KU_median_all: 0.002392767006814339
K_x_over_KU_median_all: 0.00012374725418004388
qtarget_A_over_B_median: 1.0551950124012912
qtarget_q0_median: 3.0557388536727226
qtarget_q_median: 3.0042832761743385
qtarget_chi_median: 0.24973258159582365
qtarget_K_U_median: 1.2202527830522194
qtarget_K_x_median: 0.0009616894892550711
qtarget_K_int_median: 0.015405887936981687
qtarget_beta_s_median: 0.5657134760249485
qtarget_beta_f_median: 0.26073826859393756
qtarget_G_star_median: 0.09130077157826098
qtarget_eps_over_sigma_median: 1.7500639286778896
qtarget_If_over_Is_median: 0.21624097303552464
closure_class: NOT_FOUND
```

---

# 4. Interpretation

The key quantity is:

\[
\frac{A}{B}
=
1+\frac{K_{\mathrm{int}}+K_x}{K_U}.
\]

If:

\[
K_{\mathrm{int}}+K_x
\ll K_U,
\]

then:

\[
A/B\approx1.
\]

That returns the earlier failure mode:

```text
underload and overload penalties are nearly symmetric
```

To reach:

\[
A/B\approx8,
\]

the block action must generate:

\[
K_{\mathrm{int}}+K_x\approx7K_U.
\]

That is not typical under the current broad block sampling.

---

# 5. What this file establishes

### Established

1. A concrete block-derived test for \(A/B\) and \(q_0\) is now explicit.
2. The required \(A/B\) asymmetry is equivalent to:
   \[
   K_{\mathrm{int}}+K_x\gg K_U.
   \]
3. If this ratio is not naturally large, the asymmetry principle is not derived from the current block constants.

### Not yet established

1. The tested block map may not be unique.
2. There may be a deeper action term not represented by \(K_U,K_x,K_{\mathrm{int}}\).
3. \(K_x\) and \(K_{\mathrm{int}}\) may require measured rather than broad-sampled priors.
4. This does not close \(\chi\)-selection.

---

# 6. Failure condition

The current asymmetry-from-block route fails if the verifier shows:

```text
A/B remains near 1
```

and the joint target:

\[
A/B\approx8,\quad q_0\approx3
\]

is rare or absent.

In that case, \(\chi\approx0.2667\) should remain classified as:

```text
selection plausible, not derived
```

---

# 7. Consequence for GR program

The memory coefficient branch remains:

```text
micro-to-block constrained
```

but not:

```text
fully selected from first principles
```

The broader GR derivation program can continue, but it must carry \(\chi\approx0.2667\) as a selected regime unless a deeper asymmetry source is found.

---

# 8. Next derivation target

If the block route fails, the next file should be:

```text
CHI_FIXED_POINT_STATUS_FINAL.md
```

Its job:

- record that \(\chi\approx0.2667\) is reachable and selection-plausible;
- record that it is not yet derived;
- freeze the coefficient branch honestly;
- return to the geometric GR obligations:
  \[
  S_{\mathrm{proxy}}\to S_{\mathrm{ADM}}\to S_{\mathrm{EH}}.
  \]

---

# Honest status line

> `ASYMMETRY_FROM_BLOCK_ACTION.md` tests whether the asymmetry needed to select \(\chi\approx0.2667\) follows from current block-action constants. Under the tested mapping, the required \(A/B\) asymmetry is not naturally produced, so \(\chi\) remains selection-plausible but not derived.

**End of file.**
