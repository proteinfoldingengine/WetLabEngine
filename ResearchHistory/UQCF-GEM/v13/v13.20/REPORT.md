# UQCF-GEM v13.20 — Refinement Error Scaling / Continuum Atlas Stability Gate

**Date:** 2026-09-12

## Adjudication

The continuum threshold exponents are now explicit.

Let patch scale be `h`, with a fixed macroscopic path containing

`m(h) ~ L/h`

edges.

Assume

`I(h) ~ h^alpha`

for separator conditional mutual information,

`gamma(h) ~ h^beta`

for the pair-correlation polar singular floor,

`||P(h)|| ~ h^sigma`

for source norm, and

`Lambda(h)=||dot O_e|| ~ h^lambda`

for the true per-edge connection jet.

Using v13.17 and v13.18:

`epsilon_edge(h) = O(h^(alpha/2-beta))`

and

`eta_edge(h) = O(h^(alpha/2+sigma-2beta))`.

## 1. Value-level atlas threshold

v13.19 gave path transport error

`E_value <= m epsilon`.

Therefore

`E_value(h) = O(h^(alpha/2-beta-1))`.

Hence:

**bounded value atlas**
`alpha >= 2 beta + 2`;

**vanishing value atlas**
`alpha > 2 beta + 2`.

For a nondegenerating polar gap (`beta=0`), CMI must therefore fall at least quadratically just to keep a fixed macroscopic geometric path uniformly controlled.

It must decay faster than `h^2` for the path error to vanish.

## 2. QMAR jet threshold

v13.19 gave

`E_jet <= m eta + Lambda m(m-1) epsilon`.

The first term scales as

`h^(alpha/2+sigma-2beta-1)`.

The context term scales as

`h^(alpha/2-beta+lambda-2)`.

Therefore the jet remains bounded only if both

`alpha >= 4 beta + 2 - 2 sigma`

and

`alpha >= 2 beta + 4 - 2 lambda`.

For the full jet to vanish, both inequalities must be strict.

## 3. Stable-gap bounded-source case

The conservative generic case is

`beta=0`,
`sigma=0`,
`lambda=0`.

Then:

- value geometry bounded: `alpha>=2`;
- value geometry vanishes: `alpha>2`;
- macroscopic QMAR jet bounded: `alpha>=4`;
- macroscopic QMAR jet vanishes: `alpha>4`.

Thus the response atlas is two powers more demanding in CMI than the finite geometry.

That is the direct continuum consequence of the sharp `m^2` jet composition result from v13.19.

## 4. Smooth-edge exception

If the physical connection response itself has continuum edge scaling

`Lambda(h)=O(h)`

so `lambda=1`, then the context term loses one power of `1/h`.

For stable `gamma`, the context threshold becomes `alpha>=2`.

The local jet term also requires `alpha>=2` when the remaining polar/source conditioning stays O(1).

So a quadratic CMI law can be enough in that stronger smooth-edge sector.

But `lambda=1` is not assumed.

It must be measured or derived.

## 5. Closing polar gaps raise the bar

If

`gamma(h)~h^beta`

with `beta>0`, the polar map becomes increasingly ill-conditioned.

For O(1) sources and O(1) edge jets the bounded full-jet threshold is

`alpha >= max(4 beta + 2, 2 beta + 4)`.

Thus decreasing CMI alone does not guarantee a continuum atlas.

Recoverability must beat the simultaneous loss of polar conditioning.

## 6. Synthetic exponent controls

The algebra was checked directly using exact synthetic power laws on nested `h`.

Measured log-slopes exactly reproduce the predicted exponents.

These controls only verify the scaling algebra; they are not empirical evidence for the UQCF-GEM state family.

## 7. Comparison with archived refinement evidence

The controlled v12.70 smooth Hodge family measured an ambiguity exponent about

`1.967`,

consistent with O(h^2) suppression in that separate Hodge observable.

That result does not measure CMI or polar conditioning.

The frozen ADM-7 refinement protocol later generated matched currents at

`N=7,14,28,56`.

Under that predeclared continuation the measured Hodge exponent was

`-0.1974936423`,

the restriction exponent was

`0.7197338246`,

and the N=56 high-band fraction was

`0.9604442773`.

The frozen ACR gate failed.

Those data are important negative continuum context, but they are not measurements of `alpha` or `beta` in the recoverability atlas.

Therefore they cannot be imported as either a pass or fail of the v13.20 threshold theorem.

## 8. Missing object

The next required data object is

**RATS — Recoverability Atlas Telemetry Scaling**.

For one matched nested physical relational configuration it must save:

1. separator `I(h)`;
2. polar singular floor `gamma(h)`;
3. faithfulness floor `mu(h)`;
4. edge transport recovery error `epsilon(h)`;
5. edge QMAR-jet recovery error `eta(h)`;
6. true edge response scale `Lambda(h)`.

The source/patch geometry and restriction rules must be frozen before seeing the refinement exponents.

Only then can the inequalities derived here be scored physically.

## Status

- continuum value threshold: **CLOSED**
- continuum QMAR-jet threshold: **CLOSED**
- stable-gap value threshold: **alpha >= 2**
- stable-gap conservative jet threshold: **alpha >= 4**
- archived CMI/gamma refinement exponent: **NOT AVAILABLE**
- continuum recoverability atlas: **NOT CERTIFIED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major continuum-threshold theorem and measurement specification**.

## Next — v13.21

### Recoverability Atlas Telemetry / Blind Refinement Protocol Gate

Freeze the first target-blind refinement protocol for the actual quantities that v13.20 says matter:

`I(h), gamma(h), mu(h), epsilon(h), eta(h), Lambda(h)`.

Predeclare the threshold score before data generation.

Then execute only if the existing state/engine architecture supplies a genuine nested physical refinement family without inventing a target-dependent continuation.
