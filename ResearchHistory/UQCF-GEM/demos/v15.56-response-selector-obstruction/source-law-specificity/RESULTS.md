# v15.57 Source-law specificity — COMPLETE

Date: 2026-09-26.

## Result

The frozen hidden/source response is **source-law specific** on the tested ensemble.

Using the same 27 exact-weight-three hidden directions and the same 9 one-body Pauli source generators:

- historical normalized exponential tilt: source-to-edge mixed rank **9** on all 11 fixtures;
- matched local-unitary source law: mixed rank **0** on all 11 fixtures under the preregistered parent-scaled numerical resolution rule;
- all **9/9** local-unitary source generators were active on every fixture, so the null is not an identity-source artifact;
- proper one- and two-body marginal closure held to a worst residual of **1.249000902703301e-16**;
- the largest `||E_U||_F / ||E_exp||_F` ratio was **1.233979125448394e-14**, versus the frozen acceptance ceiling `1e-9`.

The verdict is:

```
SOURCE_LAW_SPECIFICITY_CONFIRMED
```

This means the previously observed hidden/source geometry response is not forced merely by using the same one-body source directions. It depends on how the source acts on the global state. A marginally closed local-unitary action removes the hidden-completion sensitivity while remaining operationally active.

This does **not** establish that normalized exponential tilt is a physical source law, a unique source law, gravity, or universal pre-time dynamics.

## Frozen comparison

Historical source:
[
T^{\rm exp}_s(\rho;p)=
\frac{\exp(\log\rho+s p)}
{\operatorname{Tr}\exp(\log\rho+s p)}.
]

Control source:
[
T^{\rm U}_s(\rho;p)=U_p(s)\rho U_p(s)^\dagger,
\qquad
U_p(s)=\exp(-i s p/2).
]

The control uses the exact same nine one-body Pauli generators as the exponential experiment. Hidden amplitude was frozen at `eta=1e-3`; unitary source amplitude at `s=0.137`.

For a local unitary, proper marginals evolve autonomously under endpoint rotations. Exact-weight-three hidden tangents have zero proper marginals, so their invisibility is retained by this law. The numerical experiment directly checks that closure and the resulting four-corner mixed edge response.

## Reproducibility record

- Parent branch: `research/v15.56-source-edge-factorization`.
- v15.57 branch: `research/v15.57-source-law-specificity`.
- Preregistration commit: `4d5c2bb87585f9881ec6ebcc888fd1b13e8c4273`.
- RED workflow head: `e8cda72cf09624647a2697d53a761df8991b500d`.
- RED run: [36272352778](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36272352778). All eight tests failed only because `gate.py` was absent.
- Implementation commit: `5ca626b8aec6f87b5da0befb618604d7cb8cee0e`.
- Tested GREEN head: `9a63fa173964d472334e9499d3c145150bc051b8`.
- GREEN run: [36272614253](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36272614253).
- GREEN job: `108489302483`, completed success.
- New tests: **8/8 pass**.
- Full measurement and saved-artifact verification: success.
- Evidence artifact: [10916167589](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36272614253/artifacts/10916167589).
- Evidence ZIP SHA-256: `aa1dffcd3238812cf8f12c143cbb896ede5ebe06e333aadecb827982a8d4178c`.
- `report.json` SHA-256: `a0f7f240c38482a20198472c2e9360943afd7d5efdf91b6ee8610f75bc0be62a`.

The downloaded ZIP digest was independently recomputed after the run and matches GitHub's artifact digest.

## Numerical summary

| Quantity | Result |
| --- | ---: |
| Fixtures | 11 |
| Hidden/source pairs per fixture | 243 |
| Total hidden/source pairs | 2,673 |
| Exponential mixed edge rank | 9 on every fixture |
| Local-unitary mixed edge rank | 0 on every fixture |
| Active unitary source generators | 9/9 on every fixture |
| Max proper-marginal closure residual | 1.249000902703301e-16 |
| Max unitary/exponential mixed Frobenius ratio | 1.233979125448394e-14 |
| Unitary finite source-change norm | 0.2737857708503469–0.2737857708503472 |
| Exponential `||E||_F` | 337.63324524049176–637.5981182701858 |
| Unitary mixed `||E||_F` | 1.944915357733686e-12–6.355623359335722e-12 |

All exponential ranks and all unitary-null ranks were stable at the preregistered relative cuts `1e-9`, `1e-10`, and `1e-11`.

## Mechanistic implication

This sharply narrows the signal.

The earlier chain

[
243 \to 9 \to 3
]

contains two different kinds of structure:

1. `9 -> 3` is the compulsory SO(3) loop-composition reduction already derived.
2. The nonzero `243 -> 9` response is **not source-law invariant**. It survives the normalized exponential tilt but disappears under a retained-marginally closed local-unitary update.

Therefore the scientifically interesting object is no longer just the response quotient. It is the property of the source update that allows hidden global completion to feed back into retained pair geometry.

For the exponential tilt, `exp(log rho + s p)` is globally state-dependent before marginalization. The local-unitary law, by contrast, transports retained marginals autonomously. The experiment distinguishes those two mechanisms cleanly.

## What is not established

- No claim that the exponential tilt is the physical source rule.
- No derivation of Einstein dynamics.
- No gravity identification.
- No emergent spatial dimension inference from the rank-three loop space.
- No universality outside the frozen axial/cyclic ensemble.
- No statement about singular polar strata.

## Next bounded discriminator

The next test should attack ensemble dependence rather than repeat source-law controls:

**conditioning-selected symmetry-breaking ensemble.**

Construct a preregistered set of full-rank states with regular edge polar decompositions but without the axial/cyclic symmetry of the present fixtures. Do not select them using the hidden/source response. Then rerun the exponential source-to-edge measurement and the matched local-unitary null on that held-out ensemble.

The decisive questions are:

- Does exponential `E` remain nonzero and well conditioned?
- Does its rank remain nine, or was rank-nine saturation symmetry-assisted?
- Does the local-unitary mixed response remain null?
- Does the loop-visible fraction retain similar structure without cyclic symmetry?

That is the next test needed before assigning broader significance to the source-sensitive hidden-completion signal.
