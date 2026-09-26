# v15.59 Non-closed source-class gate — preregistration

Date: 2026-09-26.

## Question

Is violation of retained-marginal closure by itself sufficient to produce a nonzero hidden/source geometry response, or does normalized exponential tilt possess additional special structure?

v15.57 and v15.58 established that an active retained-marginally closed local-unitary law has zero hidden/source mixed response while normalized exponential tilt has rank nine. v15.59 introduces a second, independently defined **non-closed** source law and freezes it before measuring its hidden/source response.

## Frozen ensemble

Use exactly the 12 v15.58 asymmetric held-out states selected by seed 20260928 and candidate indices:

`13, 16, 22, 25, 27, 29, 37, 39, 46, 50, 66, 77`.

No new state selection is permitted.

## Second non-closed source law

For the same one-body Hermitian Pauli source generator (p), define the normalized congruence/filter update

[
T^{\rm filt}_s(\rho;p)=
\frac{A_p(s)\rho A_p(s)}
{\operatorname{Tr}[A_p(s)\rho A_p(s)]},
\qquad
A_p(s)=\exp(s p/2).
]

This is distinct from the historical exponential-family update

[
T^{\rm exp}_s(\rho;p)=
\frac{\exp(\log\rho+s p)}
{\operatorname{Tr}\exp(\log\rho+s p)}.
]

The filter law is chosen for a structural reason independent of the previous response: it is positive, normalized, smooth, uses the same local source generators, but because of global renormalization its retained marginals are generally not autonomous under hidden changes in the global state.

It has no fitted parameters. Freeze finite source amplitude `S_FILTER=0.137`, matching the v15.57 unitary-control amplitude for scale comparability, and hidden amplitude `ETA=1e-3`.

## Measurements

For every one of the 12 states and all 243 hidden/source columns:

1. historical exponential mixed edge map (E_{exp});
2. filter-law mixed edge map (E_{filt}), by symmetric four-corner finite difference;
3. filter-law proper-marginal non-closure residual;
4. finite filter source activity;
5. principal-angle/singular-value comparison between the row spaces/images of (E_{exp}) and (E_{filt});
6. best scalar Procrustes-free comparison: relative residual after optimal scalar (alpha E_{exp}) fit to (E_{filt}).

Use parent-scaled rank cuts `1e-9,1e-10,1e-11`, inherited unchanged.

## Preregistered adjudication

Controls:
- every filter source generator must be active above `1e-4` on each state;
- filter non-closure must be demonstrably nonzero: maximum proper-marginal hidden/source contrast > `1e-8` on every state;
- all matrices finite and all v15.58 state-conditioning criteria remain satisfied.

Outcomes:

- `NONCLOSURE_SUFFICIENT_FOR_RESPONSE_ON_ENSEMBLE`: controls pass and filter mixed rank > 0 on all 12 states.
- `NONCLOSURE_NOT_SUFFICIENT_ON_ENSEMBLE`: controls pass but at least one filter mixed map has effective rank zero.
- `INVALID`: any control/provenance/artifact failure.

**Rank nine is reported, not required. Image alignment with exponential tilt is reported, not used to decide sufficiency.**

## Interpretation

A nonzero filter response would show that exponential tilt is not unique in transmitting hidden global completion into retained geometry. It would support the narrower statement that retained-marginal non-closure can be sufficient on this ensemble.

It would **not** prove that every non-closed source law responds, that non-closure is sufficient as a theorem, or that either source law is physical/gravitational.

If both laws produce rank nine but substantially different normalized maps, the next question becomes which image features are source-law invariant. If their normalized maps align closely, that would motivate a source-class universality test.
