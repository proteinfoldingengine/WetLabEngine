# Scientific Status Memorandum
## Restricted Bridge Theorem, Restricted Fractal Corollary, Current Closures, Remaining Gaps, and Forward Plan

## 1. Executive Summary

This memorandum explains the current scientific status of the program.

The strongest present result is a **restricted mathematical/computational theorem packet**:

1. a **restricted bridge theorem** from retained baseline structure to bounded local geometric correction under iteration,
2. a **restricted fractal corollary** in the tested regime,
3. a robust branch-support scaling program across thresholds, seeds, time, resolution uplift, family variation, and regime variation,
4. a strongest current residual-estimator family based on **persistence envelopes**,
5. and a restricted asymptotic effective-dimension extrapolation.

The work is no longer merely conceptual or visual.
It now has:
- formal theorem statements,
- explicit observables,
- numerical support campaigns,
- ablation-ready estimator families,
- and clear falsifiable next steps.

It is still **restricted**, not universal.
But it is scientifically real.

---

## 2. Core Model

### 2.1 Retained baseline structure

Let:
- \(q\) denote the target probability vector,
- \(p_b\) denote the baseline score vector,
- \(r := q - p_b\) denote the retained baseline residual.

This retained residual is the central memory-like object in the current program.
The baseline is not a metaphorical memory only.
It enters the dynamics explicitly.

### 2.2 Corrected update decomposition

For a corrected state \(p_c\), define:
\[
\delta := p_c - p_b.
\]

Project the update relative to the retained residual:
\[
\delta = \lambda r + \xi,
\]
where:
- \(\lambda r\) is the residual-directed coarse correction,
- \(\xi\) is the residual-orthogonal local innovation.

This is the fundamental two-level decomposition:
- coarse residual-directed correction,
- bounded local branching / innovation.

### 2.3 Restricted affine law

Define:
\[
C_0 := \mathrm{Cov}(p_b, r), \qquad V_0 := \mathrm{Var}(r).
\]

At a reference gain \(\lambda_0\), define:
\[
a_0 = \frac{C_0+V_0}{2C_0+2\lambda_0V_0},
\]
\[
b_0 = \frac{\lambda_0^2 V_0 (C_0+V_0)}{2(C_0+\lambda_0V_0)}.
\]

Then the restricted affine relation takes the form:
\[
\Delta \mathrm{Cov} = a_0\,\Delta \mathrm{Var} + b_0 + \epsilon,
\]
with the remainder \(\epsilon\) controlled by:
- gain drift,
- curvature,
- innovation.

This is the static restricted bridge law.

### 2.4 Iterated bridge law

Let \(p_t\) evolve iteratively.
Define:
\[
r_t := q - p_t,
\]
\[
\delta_t := p_{t+1} - p_t.
\]

Then the iterated decomposition is:
\[
\delta_t = \lambda_t r_t + \xi_t.
\]

This is the iterated form of the bridge:
- a coarse affine component,
- and a local branch field.

---

## 3. What Is Closed

This section states what is now substantially closed in restricted form.

### 3.1 Restricted bridge theorem

The program now supports the restricted claim that retained baseline geometry generates bounded local geometric correction under iteration, while preserving a two-level structure:

1. coarse residual-directed correction,
2. bounded local residual-orthogonal branch field.

This is no longer speculative architecture only.
It is supported by:
- explicit decomposition,
- explicit anchored quantities,
- and successful calibration-style tests.

### 3.2 Restricted fractal corollary

The branch field support exhibits nontrivial scale-consistent behavior in the tested regime.

This is supported by:
- threshold-support scaling campaigns,
- box-count style support tests,
- multi-seed experiments,
- time-window persistence,
- multi-observable comparison,
- resolution uplift,
- family variation,
- regime variation.

So the program now supports a **restricted fractal-style interpretation**.

### 3.3 Multi-observable robustness

The scaling signal does not depend on only one branch observable.

Tested observables included:
- raw support,
- persistent support,
- change support,
- energy support.

The strongest overlap came from:
- raw support,
- persistent support,
- change support.

This materially weakens the “one hand-picked observable” criticism.

### 3.4 Large-support survival

The scaling band survives on larger support sizes, not only on the smallest original support.

Support-size campaigns showed:
- stable nontrivial bands,
- narrowing with increasing support,
- and a clean support-size ladder trend.

This weakens the finite-size criticism.

### 3.5 Family robustness

The band survives across multiple family variants and also across genuinely independent synthetic family classes.

This weakens the criticism that the result is tied to one special family or one small perturbative neighborhood.

### 3.6 Regime robustness

The band survives across multiple update regimes, not only one parameter setting.

This weakens the criticism that the signal is tied to a single update law.

### 3.7 Renormalization-style consistency

Fine→coarse support slopes remain close under coarse-graining.
Renormalization-style probes showed:
- small mean gaps,
- near-identity linear coarse-graining maps,
- and persistence of the scaling regime under coarse-graining.

This is not a final exact renormalization theorem, but it is much stronger than qualitative similarity only.

### 3.8 Persistence-derived estimator family

The branch field shows very strong lagged correlation over time.
This means the exact residual estimator should be chosen from a **persistence-envelope family**.

A fixed finite-window max estimator was a useful practical step, but the persistence analysis showed the deeper structure:
- the field is genuinely long-memory,
- therefore the estimator family should be persistence-based rather than purely short-memory.

### 3.9 Discounted persistence-envelope derivation step

To remove the arbitrariness of fixed-window truncation, the program introduced the discounted persistence-envelope estimator:

\[
\widehat{R}_t^{(\rho)} = \sup_{k\ge 0} \rho^k |\xi_{t-k}|,
\]
with \(\rho\) estimated from the measured lagged correlations.

A fitted persistence value was:
\[
\rho \approx 0.985693.
\]

This is a major closure step because it replaces arbitrary truncation with a persistence parameter estimated from the dynamics themselves.

### 3.10 Restricted asymptotic extrapolation

The support-size ladder was pushed into an explicit asymptotic extrapolation.

A restricted asymptotic effective-dimension band estimate was:

\[
D_{\mathrm{eff}}^{(\infty)} \in [0.779995,\ 0.913899],
\]
with asymptotic center approximately:
\[
0.856838.
\]

This does not prove a final asymptotic theorem, but it strongly reduces the criticism that the result is “only a finite-size phenomenon with no asymptotic meaning.”

---

## 4. Strongest Current Quantitative Statements

The strongest current restricted quantitative claims are the following.

### 4.1 Strong current jointly robust band under the official max-envelope campaign
A jointly robust effective-dimension core band under a max-like persistence estimator was:

\[
D_{\mathrm{eff}} \in [0.811364,\ 0.834298].
\]

This survived:
- family variation,
- regime variation,
- thresholds,
- seeds,
- and support uplift.

### 4.2 Persistence-envelope asymptotic direction
The discounted persistence-envelope estimator with
\[
\rho \approx 0.985693
\]
is the strongest currently motivated “derived” estimator family.

### 4.3 Restricted asymptotic extrapolation
The size-ladder extrapolation yielded:
\[
D_{\mathrm{eff}}^{(\infty)} \in [0.779995,\ 0.913899].
\]

These are not universal constants of nature.
They are restricted scientific quantities in the tested regime.

---

## 5. What Gaps Remain

Several gaps remain open.
They are now narrower than before, but still real.

### 5.1 Exact residual-estimator derivation
This is still the sharpest remaining gap.

We now know much more:
- the estimator should come from a persistence-envelope family,
- the branch field is genuinely long-memory,
- the arbitrary truncation problem has been reduced,
- a discounted persistence envelope is now motivated.

But a strict peer can still ask:
- why this exact estimator and not a nearby variant?
- can the estimator be derived directly from the dynamics or a variational principle?
- is \(\rho\) uniquely forced, or only the best current fit?

So:
- estimator family selection is much stronger,
- exact estimator theorem is still open.

### 5.2 Exact renormalization closure
The renormalization gap is much smaller than before.

We now have:
- small fine→coarse slope gaps,
- near-identity estimated renormalization maps,
- stability across family and regime variation.

But we do not yet have:
- an exact coarse-graining operator theorem,
- a formal parameter flow,
- an exact invariance or fixed-point proof,
- a rigorous renormalization closure theorem.

So the renormalization gap is reduced but not eliminated.

### 5.3 Restricted vs broader scope
The result is now strong in the tested regime, but it is still not universal.

A peer can still ask:
- how broad is the valid class?
- what happens on genuinely external or natural families?
- what happens outside the tested synthetic family classes?

So the program is scientifically strong as a **restricted result**, but broader universality remains open.

### 5.4 Provenance-clean independent reproduction
This matters less for the internal mathematics and more for scientific posture.

A rigorous peer may still ask:
- can another person regenerate the full result from a provenance-clean source pipeline?
- how much of the present system depends on hand-supplied payloads versus fully external generation?

This is still a meaningful scientific gap.

### 5.5 Exact asymptotic theorem
The support-size ladder and extrapolation strongly improve the asymptotic story.

But a final exact asymptotic theorem has not yet been proved.
The present asymptotic result is still:
- extrapolated,
- restricted,
- and supported by finite-size evidence,
rather than fully closed analytically.

---

## 6. Updated Gap Ranking

### Most attackable remaining
1. exact residual-estimator derivation
2. exact renormalization closure
3. broader universality beyond the restricted tested class
4. provenance-clean independent reproduction
5. exact asymptotic theorem

### Much less attackable now
- existence of the bridge
- existence of bounded branching
- existence of scale-consistent support behavior
- seed / threshold / time robustness
- resolution uplift robustness
- large-support survival
- family robustness
- regime robustness
- multi-observable support

---

## 7. Plan to Close the Remaining Gaps

### 7.1 Close the exact residual-estimator gap
Goal:
derive the persistence-envelope estimator from the dynamics more explicitly.

Planned directions:
1. formulate the estimator as the optimal carrier of branch persistence under bounded innovation,
2. derive the discount parameter \(\rho\) from a principled persistence model rather than only an empirical fit,
3. test infinite-horizon / discounted-envelope approximations against finite truncations,
4. look for a variational or information-stability interpretation selecting the estimator uniquely.

### 7.2 Close the renormalization gap
Goal:
move from near-identity empirical renormalization behavior to an explicit renormalization theorem.

Planned directions:
1. define an exact coarse-graining operator,
2. derive the parameter transformation under block coarse-graining,
3. identify approximate or exact invariants,
4. prove conditions under which the effective band is preserved.

### 7.3 Strengthen broader scope
Goal:
move beyond restricted family classes toward broader generality.

Planned directions:
1. independent family replication on more diverse synthetic classes,
2. larger support sizes,
3. alternative model-generation mechanisms,
4. external system classes if available.

### 7.4 Close provenance / reproduction gap
Goal:
make the result independently reproducible from a clean source pipeline.

Planned directions:
1. source-clean input generation,
2. full scripted reproduction of the theorem packet,
3. exact regeneration of all core figures and support bundles,
4. independent rerun verification.

### 7.5 Close asymptotic gap
Goal:
convert the asymptotic extrapolation into a stronger theorem.

Planned directions:
1. extend the support-size ladder,
2. test alternative extrapolation models,
3. prove convergence under the discounted persistence-envelope dynamics if possible,
4. separate finite-size artifacts from true asymptotic structure more rigorously.

---

## 8. Best Current Scientific Claim

The strongest honest scientific claim at present is:

> The program now supports a restricted bridge theorem in which retained baseline structure generates bounded local geometric correction under iteration, together with a restricted fractal corollary in the tested regime. The branch-support field exhibits stable scale-consistent behavior across thresholds, seeds, support uplift, family variation, and regime variation. A persistence-envelope residual estimator is now supported by the branch-field’s long-memory structure, and the support-size ladder is consistent with convergence toward a nontrivial restricted asymptotic effective-dimension band.

This is a real scientific statement.
It is strong.
And it is still properly scoped.

---

## 9. Bottom Line

What is closed:
- the existence of a restricted bridge
- the existence of a restricted fractal-style regime
- strong robustness of the scaling signal
- persistence as the correct estimator family
- substantial reduction of the finite-size and one-family criticisms

What remains open:
- exact residual-estimator theorem
- exact renormalization theorem
- broader universality
- provenance-clean independent reproduction
- final asymptotic closure

The program is now well past the stage of loose conceptual architecture.
It is a restricted, quantitative, proof-oriented scientific program with a much narrower and much clearer set of remaining gaps.
