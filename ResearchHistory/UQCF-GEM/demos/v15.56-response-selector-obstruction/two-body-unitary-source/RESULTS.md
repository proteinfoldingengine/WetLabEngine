# v15.73 — Explicit two-body unitary source

Verdict: **TWO_BODY_UNITARY_HIDDEN_ROTATION_CONFIRMED**.

All 11,664 state/source/hidden-probe cases passed numerical validity. Each of the 324 state/two-body-source combinations produced exactly twelve nonzero unit-HS response tangents, leakage rank 12 and polar-skew/rotation rank six. Each responding edge had rank three; the source-support edge had zero marginal response. Aggregating the 27 two-body sources gave leakage rank 27 and Q/E rank nine on every state at all three frozen thresholds. All nine matched one-body source controls remained active, with exactly zero retained leakage, skew and rotation maps.

The smallest sixth per-source Q singular value was 3.9999999999999956; the smallest aggregate ninth was 19.595917942265405. These ranks are far from their cutoffs. The exact Pauli-support argument in DERIVATION.md explains them independently of numerical fitting.

## Validity evidence

- Unitarity residual: 6.280369838047253e-16.
- Mixture-affinity residual: 9.856691834228504e-17.
- Centered derivative versus exact sinc identity: 1.998899812222513e-17.
- Centered derivative truncation: 1.666666583314181e-7, as predicted at s=1e-3.
- Sylvester residual: 1.4941919998528006e-14.
- Disjoint exterior change: 1.570447882860392e-16.
- Minimum baseline source activity: 0.06997263019470394.
- Minimum finite density eigenvalue: 0.03831621266594473.
- Minimum retained correlation singular value: 0.02083908843655896.

## Exact execution provenance

Parent certified head: `846cc623b6c4f26f8e85e0cbd64d2eb0ba9ed040`.

Preregistration/test commit: `0689bdffb12b16b26daba52524de664f5ed4d10d`.
[Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36295058906): job `108552261852`, artifact `10923193441`, artifact SHA-256 `ae838a2c0a1759faa3f26e8a9cfafc9c01b0866f84d974f7a495aa1e145838a4`. Setup succeeded; the sole failure was the deliberate missing-implementation assertion. Downloaded archive and execution head verified.

Initial implementation: `8dafdc2d3e445992a2bd3465a6a75fa2f592c4f8`.
[Implementation-defect run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36295187757): job `108552622836`, artifact `10923622736`. Exact logs show three unit tests passed and measurement finalization raised TypeError because source-label dictionary keys were integers. This is an implementation failure, not a scientific NO. The correction only converts report keys to strings. Tests, preregistration and scientific criteria were unchanged. Unexpected programming exceptions fail CI; they are not converted into scientific claims.

Corrected tested implementation: `9817b8034127fd9db17726184e2e49024d98f3a8`.
[GREEN run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36295199652): job `108552653865`, artifact `10923433633`, artifact SHA-256 `6e97d27551327de5e2fced1675a829bd742b0c69a2af6083ab965900c876231c`. Four tests passed; standalone result explicitly reports the verdict above and all_valid=true. Exact job logs inspected. Downloaded artifact hash, execution SHA, all recorded source/result hashes and source bytes were verified.

Raw result SHA-256: `2c73db463084e0e77b638031fa0ece4c2bbbbe147c58179e8f416c39a3be667c`. RESULT.json.gz preserves the exact standalone JSON losslessly, including aggregate Q/E matrices, per-source spectra and coverage. SUMMARY.json is a readable reduction. Decompress with `gzip -dc RESULT.json.gz > result.json` and verify the raw digest. Reproduce at the tested commit with Python 3.11 and numpy==2.3.5, following the workflow. Documentation is an additive later commit; its containing Git commit identifies the published documentation head without circular self-hashing.

## What was learned and what remains open

The v15.71 null construction failed the unconditioned mixture-affinity gate in v15.72. Here a state-independent unitary source passes that operational constraint and produces full retained edge rotation rank through ordinary two-body operator-support transfer. The source generator does not consult the extracted polar factors, hidden probe, or source-memory record. Thus an explicitly admissible quantum operation can supply the required skew sector when its interaction support overlaps the retained region appropriately.

The interaction is specified, not derived from Genesis Pin or recoverability. This is standard quantum correlation redistribution, not a novel quantum mechanism, physical source-selection theorem, gravity derivation, or change in admissible worlds. The result does not establish that operational admissibility forces every source to rotate: local-unitary controls remain null. Neither does it resolve a universal classification of covariant affine null sources. The precise remaining question is which interaction/source axiom the retained framework selects, and whether a nontrivial operationally admissible interacting source can retain leakage while remaining polar-skew null on an open state domain. No fundamental time, preferred external alignment, fitted explanation or new matter primitive is introduced. All historical verdicts remain unchanged. No merge to main.
