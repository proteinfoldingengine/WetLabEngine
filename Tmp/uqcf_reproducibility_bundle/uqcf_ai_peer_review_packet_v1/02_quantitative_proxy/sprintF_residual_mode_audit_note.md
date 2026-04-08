# Sprint F — Residual-mode audit

We test whether the mismatch seen in the first proxy confrontation is better explained by
an overly simple observable wrapper than by immediate failure of the bridge core.

## Setup

Base locked bridge ratio:
- bridge_over_baseline from Sprint F confrontation table

One extra low-complexity mode:
- R2(z) = z / (1 + z)

Augmented observable wrapper:
y_model(z) = y_base(z) + c * R2(z)

where c is fit once by weighted least squares against the data-side ratio using the propagated
proxy uncertainties.

## Result

- base proxy chi2 = 6.831
- augmented proxy chi2 = 6.149
- delta chi2 = 0.682
- best extra coefficient c = -0.014594 ± 0.017670

## Interpretation

A large drop in chi2 with only one extra response mode suggests the current mismatch is at least partly
an observable-wrapper problem, not a direct refutation of the bridge core.
