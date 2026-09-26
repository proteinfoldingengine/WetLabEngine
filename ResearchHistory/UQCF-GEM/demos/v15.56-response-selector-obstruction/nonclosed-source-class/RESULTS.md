# v15.59 Non-closed source-class gate — COMPLETE

Date: 2026-09-26.

## Verdict

```
NONCLOSURE_SUFFICIENT_FOR_RESPONSE_ON_ENSEMBLE
```

A second independently defined non-marginally-closed source law produces a nonzero hidden/source geometry response on all 12 frozen asymmetric states.

The tested filter law was preregistered before response measurement:

[
T^{\rm filt}_s(\rho;p)=
\frac{e^{sp/2}\rho e^{sp/2}}
{\operatorname{Tr}(e^{sp/2}\rho e^{sp/2})}.
]

It uses the same nine one-body Pauli source generators as the historical normalized exponential tilt.

## Main result

Across all 12 frozen v15.58 asymmetric states:

- exponential mixed edge rank: **9/9** on every state;
- filter mixed edge rank: **9/9** on every state;
- filter source activity: **9/9 generators active** on every state;
- filter retained-marginal non-closure exceeded the preregistered (10^{-8}) floor on every state;
- all rank results were stable at relative cuts (10^{-9},10^{-10},10^{-11});
- artifact verification independently reproduced the verdict.

Rank nine was not required for the sufficiency verdict. It emerged on every state.

## The two non-closed laws are related but not identical

Both maps span nine-dimensional subspaces of the 243-dimensional hidden/source domain, but their maps are not simple scalar copies.

Across the 12 states:

- minimum principal cosine between the two nine-dimensional row spaces: **0.9289480365879012–0.9577807541948985**;
- optimal scalar-fit relative residual: **0.20277658173310243–0.2893387871161325**;
- normalized full-map distance: **0.2040484230612293–0.2924464936439281**;
- optimal scalar (alpha), fitting (E_{filter}\approx\alpha E_{exp}): **0.8681194555113287–0.9495710400663041**.

Thus the second law largely accesses a similar hidden/source subspace, while retaining substantial law-dependent structure. This is evidence against both extremes:

1. the response is unique to normalized exponential tilt — not supported by this test;
2. all non-closed source laws produce the identical map — also not supported.

## Non-closure and response magnitude

The maximum retained-marginal hidden contrast under the filter law was approximately **0.001772–0.002531** across the states, far above the frozen (10^{-8}) demonstration floor.

Filter response Frobenius norms were **355.003–500.782**, comparable in scale to exponential norms **386.181–535.445**. No amplitude fitting was performed.

## What is earned

Together v15.57–v15.59 establish on the tested regular ensembles:

[
\text{retained-marginally closed local unitary}
\quad\Longrightarrow\quad
E\simeq0
]

for the tested local-unitary class, while two structurally different non-closed laws give

[
\operatorname{rank}E=9.
]

This supports a concrete mechanistic hypothesis: **access of the source update to hidden global completion is the relevant prerequisite for the observed retained-geometry response.**

The current evidence does not establish the converse as a theorem. “Non-closure is sufficient” here is strictly an empirical statement about this preregistered filter law on the 12-state ensemble.

## Reproducibility

- Branch: `research/v15.59-nonclosed-source-class`.
- Preregistration: `bbefb58181fddb31de4370c633686d3c42f0ebf9`.
- RED run: [36273389227](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273389227), expected failure because `gate.py` was absent.
- Tested implementation: `95a418e468951b8eff3410a8c67e5f63d07e56f6`.
- GREEN run: [36273507804](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273507804), job `108491756307`.
- Tests: pass.
- Full 12-state measurement: pass.
- Saved-artifact verification: pass.
- Artifact: [10916263480](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36273507804/artifacts/10916263480).
- Artifact ZIP SHA-256: `a43e4c343660361c964019e9eb0f7efeb752dc92c4ffde528cc1123722f0c248`.

## Interpretation boundary

Not established:

- that every non-closed source law has nonzero response;
- that non-closure alone mathematically guarantees rank nine;
- that the exponential or filter law is physically preferred;
- that the response is gravity;
- Einstein dynamics or an emergent spacetime law.

## Next bounded question

The important next object is the **shared versus source-specific response geometry**.

Because two independent non-closed laws both yield rank nine with strongly overlapping but non-identical row spaces, the next preregistered experiment should decompose

[
\mathcal I_{exp}\cap\mathcal I_{filter}
]

and the complementary source-specific directions state by state, then test whether the shared component is stable under source amplitude and a third non-closed law.

That is a more discriminating universality test than adding more examples that merely reproduce rank nine.
