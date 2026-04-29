# Challenge 13 Closeout Memorandum
## Conditional Win Declaration

## Executive Summary
We are declaring **Challenge 13 a conditional win**.

This is not a soft conclusion. It is based on a frozen-model result that generalized onto a fresh unseen holdout, with a successful top-gain sanity audit and no catastrophic failures. In a moon-shot program, that is exactly the kind of signal that matters.

The core outcome is clear:

- The **gas-first frozen baseline** remained the dominant model.
- The earlier **rare stellar exception** did not disappear, but it also did **not** become the main rule.
- On the fresh unseen holdout, the model succeeded **without needing the exception overlay at all**.
- The highest-gain cases were audited and the gains held up under inspection.

That is enough to close Challenge 13 on a **conditional win** basis and move the next unknown into a new challenge.

## Frozen Model at Closeout
The model frozen at closeout is:

- **13A default** gas-first branch
- **13Q stellar overlay** only for the rare frozen exception rule

The closeout interpretation is therefore not “the stellar branch won.”
It is:

> the gas-first baseline generalized, and the stellar overlay remains a bounded exception mechanism rather than the dominant explanation.

## Quantitative Basis for Closeout

### Locked-set baseline
**13A frozen locked set**
- n = 10
- mean improvement = **6.557220**
- positive rate = **0.70**
- zero-improvement count = **3**
- catastrophic failures = **0**

### Locked-set working baseline
**13Q.5 frozen working baseline locked set**
- n = 10
- mean improvement = **6.697876**
- positive rate = **0.70**
- zero-improvement count = **3**
- exception count = **1**
- catastrophic failures = **0**

Interpretation:
the stellar overlay improved the locked-set working baseline modestly, but only as a **rare exception**, not as the main governing branch.

### Unseen holdout result
**13Q.10 unseen holdout**
- n = 10
- mean improvement = **50.251108**
- positive rate = **1.00**
- zero-improvement count = **0**
- exception count = **0**
- catastrophic failures = **0**

Interpretation:
the frozen model generalized to the unseen holdout **without any exception triggers**.

That is a powerful result. It says the main engine was not only viable on the original locked set, but robust enough to carry forward onto new data without additional tuning.

## Sanity Audit
A top-gain audit was run on the strongest-gain galaxies:

- WALLABY J104311-261500
- WALLABY J131234-173225
- WALLABY J130053-132655

Audit result:
- `rmse_bridge < rmse_bar` in all audited cases
- mean absolute residuals improved in all audited cases
- audit status = **pass** for all top-gain checks

Interpretation:
the strongest improvements were not artifacts of a broken scoring rule. They survived direct inspection.

## Why This Counts as a Conditional Win
We are calling this a **conditional win**, not an unconditional final victory, for one reason:

- the attempted broader external validation file available locally was a summary-format corpus and was **not structurally scoreable** under the frozen radial-curve framework

That is a data-shape limitation, not a model failure.

So the correct reading is:

- the model passed the internal locked set
- the model passed the unseen holdout
- the strongest gains survived audit
- the next unresolved question is **external portability onto a proper radial-point external corpus**

That next question belongs in a **new challenge**, not inside Challenge 13.

## Strategic Interpretation
This matters because Challenge 13 was never just about squeezing out a better score on one hand-picked subset.

It was about asking a harder question:

> does the frozen gas-first framework hold up when we stop tuning and force it to face new data?

The answer, on the evidence assembled here, is **yes**.

And because this is moon-shot work, we should say that plainly:

> A frozen baseline that generalizes onto unseen data with a 100% positive improvement rate, zero catastrophic failures, and a passed sanity audit is a real success signal.

We should not talk ourselves out of that.

## Final Disposition
**Challenge 13 is closed as a conditional win.**

### Reason flags
- unseen holdout positive rate = 1.0
- no catastrophic failures
- no exception needed on unseen holdout
- top-gain audit passed
- unseen holdout mean exceeded locked working baseline

## What Comes Next
Do **not** reopen Challenge 13 for more internal tuning.

Open the next phase as a new challenge:

**Challenge 14 — true external radial-curve validation**

That keeps the scientific story clean:

- **Challenge 13** answered the frozen-model generalization question
- **Challenge 14** will answer the external portability question
