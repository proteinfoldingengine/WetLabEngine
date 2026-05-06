# CHI_SELECTION_PRINCIPLE.md

# Chi Selection Principle
## From rare reachability to a variational selection problem for \(\chi_*\approx0.2667\)

## Status
**Selection-principle candidate. Not first-principles closure.**

`CHI_NATURALNESS_FROM_PRUNING.md` found:

```text
naturalness_class: RARE_BUT_REACHABLE
```

for:

\[
\chi_*\approx0.2667.
\]

That means the target fixed point is reachable, but broad pruning/noise sampling does not naturally select it.

This file reframes the problem:

> What principle selects \(\Lambda_*\approx2.75\), and therefore \(\chi_*\approx0.2667\), from the reachable parameter space?

This file proposes the first explicit selection-functional candidate. It is not yet a final derivation.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as proving \(\chi\) from first principles.

---

# 1. Target

The target bridge coefficient is:

\[
\chi_{\mathrm{target}}\approx0.2667.
\]

The equivalent loading target is:

\[
\Lambda_{\mathrm{target}}
=
\frac{1-\chi_{\mathrm{target}}}{\chi_{\mathrm{target}}}
\approx2.75.
\]

The selection problem is:

\[
\text{why should the system choose }\Lambda_*\approx2.75?
\]

---

# 2. Why reachability is not enough

`CHI_TARGET_PARAMETER_REGIME.md` showed:

\[
b\approx2.75(1-a)
\]

is sufficient to hit the target.

`CHI_NATURALNESS_FROM_PRUNING.md` showed broad sampling only hits the target about:

```text
0.8588%
```

of the time.

Therefore:

\[
\chi\approx0.2667
\]

is not yet derived. It is rare but reachable.

A selection principle is required.

---

# 3. Candidate balance functional

## Definition 1
Let:

\[
\chi(\Lambda)=\frac{1}{1+\Lambda}.
\]

Define the candidate balance functional:

\[
\mathcal F(\Lambda)
=
\frac{A}{\Lambda}
+
B\Lambda
+
\frac{C}{\chi(\Lambda)(1-\chi(\Lambda))}
+
S(\Lambda-q)^2.
\]

Interpretation:

- \(\frac{A}{\Lambda}\): penalty for insufficient retained-memory loading;
- \(B\Lambda\): penalty for excessive memory domination;
- \(\frac{C}{\chi(1-\chi)}\): penalty for weak bridge responsiveness;
- \(S(\Lambda-q)^2\): micro-to-block balance anchor.

Here \(A,B,C,S,q>0\).

This is the first explicit selection-principle candidate.

---

# 4. Stationarity condition

## Lemma candidate 1
A selected loading ratio satisfies:

\[
\frac{d\mathcal F}{d\Lambda}=0.
\]

Because:

\[
\chi(1-\chi)
=
\frac{\Lambda}{(1+\Lambda)^2},
\]

we have:

\[
\frac{1}{\chi(1-\chi)}
=
\frac{(1+\Lambda)^2}{\Lambda}
=
\Lambda+2+\frac{1}{\Lambda}.
\]

Therefore:

\[
\mathcal F(\Lambda)
=
\frac{A}{\Lambda}
+
B\Lambda
+
C\left(
\Lambda+2+\frac{1}{\Lambda}
\right)
+
S(\Lambda-q)^2.
\]

Collecting terms:

\[
\mathcal F(\Lambda)
=
\frac{A+C}{\Lambda}
+
(B+C)\Lambda
+
2C
+
S(\Lambda-q)^2.
\]

Then:

\[
\frac{d\mathcal F}{d\Lambda}
=
-\frac{A+C}{\Lambda^2}
+
(B+C)
+
2S(\Lambda-q).
\]

The selection equation is:

\[
-\frac{A+C}{\Lambda^2}
+
(B+C)
+
2S(\Lambda-q)
=
0.
\]

Equivalently:

\[
2S\Lambda^3+
(B+C-2Sq)\Lambda^2
-(A+C)=0.
\]

So \(\Lambda_*\) is selected as the positive stable root of a cubic.

---

# 5. Condition for target selection

For:

\[
\Lambda_*=\Lambda_{\mathrm{target}},
\]

the coefficients must satisfy:

\[
\frac{A+C}{\Lambda_{\mathrm{target}}^2}
=
(B+C)
+
2S(\Lambda_{\mathrm{target}}-q).
\]

This is the selection-surface condition.

It does not directly tune \(b\). It constrains the balance of:
- memory insufficiency cost;
- memory overload cost;
- bridge responsiveness;
- micro-balance anchor.

---

# 6. Why this matters for GR derivation

The coefficient branch now has:

\[
m_R^2=1-a,
\]

\[
Z_R=\chi(1-\chi)\sigma_{\nabla\Lambda}^2(dx/dt)^2,
\]

\[
\lambda_{\mathrm{int}}=\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

If \(\chi\) is not selected, these coefficients remain reachable but not derived.

A selection principle for \(\chi\) is therefore necessary before claiming the memory coefficients are fully derived.

---

# 7. Verifier implementation

## Status
**Implemented as `chi_selection_principle_verifier.py`. Execution log captured.**

The verifier samples broad positive values of:

\[
A,B,C,S,q
\]

and minimizes:

\[
\mathcal F(\Lambda).
\]

It checks how often the selected optimum produces:

\[
\chi_*\approx0.2667.
\]

## Captured verifier output

```text
Chi selection principle verifier
==================================================
Route:
candidate balance functional -> selected Lambda* and chi*
This tests plausibility of a selection principle, not final derivation.

valid_samples: 100000
target_hits: 5066
hit_rate_percent: 5.066
naturalness_class: SELECTION_PLAUSIBLE
Lambda_opt_median_all: 1.1054058557693487
chi_opt_median_all: 0.4749678059741997
A_median_all: 1.0008773810867964
B_median_all: 0.9897794221920191
C_median_all: 0.0254503615180091
S_median_all: 0.3145678329747716
q_median_all: 1.0181497309142418
Lambda_opt_median_hits: 2.7524526710413353
Lambda_opt_p10_hits: 2.5509582549607996
Lambda_opt_p90_hits: 2.990459113202914
chi_opt_median_hits: 0.26649236850267644
chi_opt_p10_hits: 0.25059773114611794
chi_opt_p90_hits: 0.28161412446991424
A_median_hits: 2.945467663999203
A_p10_hits: 0.26699951397242205
A_p90_hits: 8.11491282120507
B_median_hits: 0.39607220149356537
B_p10_hits: 0.13089169074273926
B_p90_hits: 2.3006066737474655
C_median_hits: 0.02414177396275554
C_p10_hits: 0.0018821935999916541
C_p90_hits: 0.32235984097707526
S_median_hits: 0.18174502317717867
S_p10_hits: 0.018870015038210765
S_p90_hits: 4.737167202619503
q_median_hits: 2.7677533542558184
q_p10_hits: 0.28393778937984904
q_p90_hits: 5.074943266209216
Lambda_target: 2.749531308586427
```

---

# 8. What this file establishes

### Established

1. The \(\chi\)-selection problem can be written as a variational balance problem.
2. The proposed balance functional reduces to a cubic stationarity equation.
3. The target \(\Lambda\approx2.75\) corresponds to an explicit coefficient surface.
4. A selection principle can produce target \(\chi\) without directly solving \(b=2.75(1-a)\).

### Not yet established

1. The functional \(\mathcal F\) is not yet derived from microscopic action.
2. \(A,B,C,S,q\) are not yet tied to measurable recursion quantities.
3. The selection surface may still be broad or tuned.
4. This is a candidate principle, not first-principles closure.

---

# 9. Failure conditions

This route fails if:

1. no broad coefficient region selects \(\chi\approx0.2667\);
2. the selection functional cannot be derived from micro-to-block action;
3. the required balance surface is equivalent to tuning;
4. selected \(\chi\) destabilizes \(Z_R,V,\lambda_{\mathrm{int}}\);
5. the principle conflicts with the fixed-point loading map.

---

# 10. Next derivation target

The next file should be:

```text
CHI_SELECTION_FROM_BLOCK_ACTION.md
```

Its job:

Derive or reject the candidate \(\mathcal F(\Lambda)\) from the block action constants:

\[
K_t,\quad K_U,\quad K_x,\quad K_{\mathrm{int}}.
\]

That determines whether the selection principle is real or merely phenomenological.

---

# Honest status line

> `CHI_SELECTION_PRINCIPLE.md` converts the rare-but-reachable \(\chi\) result into an explicit variational selection problem. It provides a candidate balance functional and cubic selection equation, but it does not yet derive that functional from the microscopic/block action.

**End of file.**
