# v15.60 Shared response geometry — preregistration

Date: 2026-09-26.

## Question

v15.59 found two independent non-closed source laws with rank-nine hidden/source response and strongly overlapping, non-identical row spaces. Is there a stable common response geometry, or is the overlap merely state- and amplitude-specific?

## Frozen states and laws

Use exactly the 12 v15.58 asymmetric states, candidate indices:
`13,16,22,25,27,29,37,39,46,50,66,77`.

Source laws:
1. historical normalized exponential tilt, evaluated by its analytic mixed derivative;
2. normalized positive filter (A\rho A/\mathrm{Tr}(A\rho A)), (A=e^{sp/2}).

No new source law is introduced in this stage.

## Frozen amplitudes

For the filter finite-difference map use three source amplitudes:

[
s\in\{0.0685,0.137,0.274\}.
]

Hidden amplitude remains `ETA=1e-3`.

The center amplitude is the v15.59 value. The half/double values are fixed before measurement.

## Objects

For each state and amplitude, compute the rank-nine row-space projectors in the 243-dimensional hidden/source domain:

[
P_{exp}=V_{exp}V_{exp}^T,qquad P_{filt}(s)=V_{filt}(s)V_{filt}(s)^T.
]

Record:

- all nine principal cosines between exponential and filter row spaces;
- chordal projector distance (|P_{exp}-P_{filt}|_F/\sqrt{2});
- eigenvalues of the averaged projector (P_*=(P_{exp}+P_{filt})/2);
- source-law-common directions defined only descriptively by principal vectors, not by an arbitrary hard intersection threshold;
- filter amplitude drift: principal cosines and projector distance between (P_{filt}(0.0685)), (P_{filt}(0.137)), and (P_{filt}(0.274));
- normalized-map and optimal-scalar residuals at each amplitude.

## Preregistered controls

- both laws must have effective rank 9 on all 12 states at all three filter amplitudes;
- filter source activity must remain nonzero;
- filter non-closure must remain >1e-8;
- all matrices finite and state identity unchanged.

No minimum overlap is required for validity.

## Adjudication

This stage is primarily descriptive and avoids manufacturing a binary universality claim.

`SHARED_GEOMETRY_MEASURED`: all controls pass and all requested geometry diagnostics are preserved.

`INVALID`: any rank, activity, non-closure, state-identity, finite-value, or artifact-integrity control fails.

Interpretation categories reported after measurement:

- **amplitude-stable overlap** if the filter row-space projector changes less across half/center/double amplitude than the filter differs from exponential at center amplitude;
- **amplitude-sensitive overlap** otherwise.

This category is descriptive, not a physical certification.

## Boundary

Even a stable common nine-dimensional response geometry would not establish a physical source law, gravity, Einstein dynamics, or universality across arbitrary source laws. It would identify a concrete invariant candidate for the next source-class test.
