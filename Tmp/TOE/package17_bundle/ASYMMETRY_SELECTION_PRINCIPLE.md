# ASYMMETRY_SELECTION_PRINCIPLE.md

# Asymmetry Selection Principle
## Candidate stabilization law for intermediate retained-memory loading

## Status
**Selection theorem candidate. Not final derivation.**

`RETAINED_MEMORY_LOADING_ASYMMETRY.md` showed that the desired loading

\[
q_{\mathrm{block}}=\frac{b}{1-a}\approx2.75\text{–}3.3
\]

is not the default under broad sampling and is not the default under strong memory bias.

Broad sampling underloads memory:

\[
q_{\mathrm{median}}\approx0.176,
\qquad
\chi_{\mathrm{median}}\approx0.851.
\]

Memory-biased sampling overloads memory:

\[
q_{\mathrm{median}}\approx14.53,
\qquad
\chi_{\mathrm{median}}\approx0.064.
\]

Therefore the target appears to lie in an intermediate stabilization band:

```text
too little memory  -> chi too high
too much memory    -> chi too low
balanced memory    -> chi near 0.2667
```

This file proposes the first explicit asymmetry-selection principle.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Theorem candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Target

The target loading is:

\[
q_{\mathrm{target}}
\approx
2.75\text{–}3.3.
\]

The equivalent bridge coefficient is:

\[
\chi=\frac{1}{1+q}.
\]

For:

\[
q\approx2.75,
\]

\[
\chi\approx0.2667.
\]

---

# 2. Candidate stabilization functional

## Definition 1
Define a retained-memory loading stability cost:

\[
\mathcal A(q)
=
\frac{A}{q}
+
Bq
+
C\left[\log\left(\frac{q}{q_0}\right)\right]^2
+
\frac{D}{\chi(q)(1-\chi(q))}.
\]

where:

\[
\chi(q)=\frac{1}{1+q}.
\]

Interpretation:

- \(\frac{A}{q}\): penalty for insufficient retained-memory loading;
- \(Bq\): penalty for overloading memory relative to geometry;
- \(C[\log(q/q_0)]^2\): critical-band stabilization around internal loading scale \(q_0\);
- \(\frac{D}{\chi(1-\chi)}\): bridge-response penalty when the bridge becomes too one-sided.

This is not a final microscopic derivation. It is a candidate selection law.

---

# 3. Stationarity condition

A selected loading satisfies:

\[
\frac{d\mathcal A}{dq}=0.
\]

The derivative is:

\[
-\frac{A}{q^2}
+
B
+
\frac{2C\log(q/q_0)}{q}
+
D\frac{d}{dq}
\left[
\frac{1}{\chi(1-\chi)}
\right]
=
0.
\]

Since:

\[
\chi(1-\chi)=\frac{q}{(1+q)^2},
\]

we have:

\[
\frac{1}{\chi(1-\chi)}
=
q+2+\frac{1}{q}.
\]

Therefore:

\[
\frac{d}{dq}
\left[
\frac{1}{\chi(1-\chi)}
\right]
=
1-\frac{1}{q^2}.
\]

So the selection equation is:

\[
-\frac{A}{q^2}
+
B
+
\frac{2C\log(q/q_0)}{q}
+
D\left(1-\frac{1}{q^2}\right)
=
0.
\]

This is the explicit asymmetry-selection equation.

---

# 4. Why this differs from “more memory”

The previous verifier showed that simply increasing memory bias often overshoots:

\[
q\gg3.
\]

This functional does not say:

```text
increase memory without bound
```

It says:

```text
select the stable intermediate band where underloading and overloading costs balance
```

The target \(q\approx3\) is plausible only if the internal scale \(q_0\), underload cost \(A\), overload cost \(B\), and bridge-response cost \(D\) combine to stabilize that band.

---

# 5. Verifier implementation

## Status
**Implemented as `asymmetry_selection_principle_verifier.py`. Execution log captured.**

The verifier samples positive values of:

\[
A,B,C,D,q_0
\]

and minimizes:

\[
\mathcal A(q).
\]

It checks how often the selected \(q\) lands in:

\[
2.75\le q\le3.3.
\]

## Captured verifier output

```text
Asymmetry selection principle verifier
==================================================
Route:
underload + overload + critical-band + bridge-response penalties -> selected q=b/(1-a)
Tests intermediate-loading stabilization, not final derivation.

valid_samples: 100000
target_band_hits: 5150
target_band_hit_rate_percent: 5.15
selection_class: STABILIZATION_PLAUSIBLE
qopt_median_all: 1.2275231083861395
chiopt_median_all: 0.44892912501568116
A_median_all: 1.7975418904241978
B_median_all: 1.7810096224787921
C_median_all: 0.3154873000869417
D_median_all: 0.007858400277544472
q0_median_all: 1.9867353639387744
A_over_B_median_all: 1.0147875585407822
qopt_median_hits: 3.00026111275527
qopt_p10_hits: 2.7999420937032915
qopt_p90_hits: 3.2297560709039357
chiopt_median_hits: 0.24998368151803657
chiopt_p10_hits: 0.23642025290273805
chiopt_p90_hits: 0.2631619049293024
A_median_hits: 5.28344841448599
A_p10_hits: 0.4249661941036908
A_p90_hits: 22.30932516142066
B_median_hits: 0.539018569699225
B_p10_hits: 0.1375941795046336
B_p90_hits: 2.311026127939568
C_median_hits: 0.6627094128599387
C_p10_hits: 0.025401678128113205
C_p90_hits: 5.985785798765115
D_median_hits: 0.007836907743859256
D_p10_hits: 0.0002449060897038847
D_p90_hits: 0.2565046185481074
q0_median_hits: 2.960010550186321
q0_p10_hits: 0.9461211523725174
q0_p90_hits: 5.224007597005755
A_over_B_median_hits: 9.395868385300648
A_over_B_p10_hits: 1.1086512637511443
A_over_B_p90_hits: 26.786365026435636
```

---

# 6. What this file establishes

### Established

1. The intermediate-loading problem can be written as an explicit variational selection equation.
2. The selection equation penalizes both underloading and overloading.
3. The bridge-response term prevents one-sided \(\chi\) extremes.
4. A target loading band can be tested without simply forcing \(b/(1-a)\).

### Not yet established

1. \(A,B,C,D,q_0\) are not yet derived from the micro-to-block action.
2. The functional is still a candidate principle.
3. The internal loading scale \(q_0\) must be explained.
4. This does not close the GR derivation.

---

# 7. Failure conditions

This route fails if:

1. the target band is rare under broad positive \(A,B,C,D,q_0\);
2. the target requires \(q_0\) to be manually set to \(3\);
3. \(A/B\) must be tuned rather than derived;
4. the functional cannot be derived from retained-memory action stability.

---

# 8. Next derivation target

The next file should be:

```text
ASYMMETRY_SELECTION_STATUS.md
```

Its job:

- assess whether this selection law improves the \(\chi\) bottleneck;
- decide whether to derive \(A,B,C,D,q_0\) from the block action;
- or mark \(\chi\approx0.2667\) as still phenomenological.

---

# Honest status line

> `ASYMMETRY_SELECTION_PRINCIPLE.md` proposes and tests a stabilization law for intermediate retained-memory loading. It can explain why neither underloaded nor overloaded memory regimes are correct, but it is not yet derived from first principles.

**End of file.**
