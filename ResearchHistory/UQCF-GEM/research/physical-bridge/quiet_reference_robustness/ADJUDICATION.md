# Noisy-reference threshold: conditional acceptance and scope

Date: 2026-11-13 UTC (2026-11-12 MST).
Status: **ACCEPTED CONDITIONAL MATHEMATICS**. Native bridge **NOT_DERIVED**. PR146 is unmerged; no numbered-stage CLOSED/CERTIFIED status.

## Accepted implication

With the same qubit receiver/effect, exact source channel and diagonal pair, known full-rank bath spectrum and NEW reference constraint q_0<=epsilon, the sharp signed contrast minimum is `(1-epsilon-T(epsilon))/5`, with T the opposite-order piecewise spectral allocation in ARGUMENT.md. The minimum absolute contrast is its positive part. The exact threshold is the lower half of the bath spectrum, including half the middle eigenvalue for odd dimension. Explicit rotated frames attain the bound while implementing the full source channel.

For a two-state bath with eigenvalues (a,b), a>=b>0, the threshold is b. Thus (9/10,1/10) admits a blind fixed effect at reference response 1/10, whereas a uniform bath guarantees positive contrast for every reference response bounded strictly below 1/2. These are exact conditional statements, not empirical noise estimates.

## Independent review and publication identities

| Item | Identity |
|---|---|
| Integrated parent | `2ab565c3f5bf10305a96ddeef30901de49959ba5` |
| New proof freeze | `7e916a59980f6124831b0c67c3fd59b58cc09cb4` |
| New argument blob | `740098f98d2f308cde7a5d2ce08618c424b6627e` |
| Prior corrected PR145 source pin (unmerged) | `fe4a49b9093cc1e24c619d84ec646d9f6d075de0` |
| Workflow and checkout | `3230e67c760ea00004560aaaa0dac738b71cfb00` |
| Actions run / attempt | [43336512365](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/43336512365) / 1 |
| Requested / returned model | `gemini-3.1-pro-preview` / `gemini-3.1-pro-preview` |
| Source packet SHA256 | `cf79e1f5cf31852d7fb171c4c6262485ae6bfa95dd5664a51465986dc344956a` |
| Raw response SHA256 | `ec3b99d861e5410f7cbd6587f4ced50badb260aa3a8a0bcd27ff4bc08a76ae14` |
| Review original ZIP SHA256 | `ac66f4a79e5b6035f5f77108be3caa588dc38cf67a92cba0e7ad6e37044da605` |
| Publication original ZIP SHA256 | `69bbc1e3f17da9fc9ef1e3fe43efc535a499d1c72ef67c2d9e4ae3f36bf6917c` |

Gemini returned ACCEPTED, ten claim-specific checks, no findings/missing assumptions/counterexamples, and NOT_DERIVED. Root inspected its complete ordinary answer and the manuscript. In particular the proof uses completeness of two d-frames in dimension 2d, not an assumed ability to realize arbitrary diagonals; the explicit rotations establish simultaneous attainment. The zero-contrast threshold implementation remains admitted beyond the threshold, which is required for the absolute-contrast assertion.

Two reviewer phrasings are interpreted strictly according to the manuscript: cross-index orthogonality follows from unitarity on distinct input vectors |p,e_i,0> and |u,e_j,0>, not from the reduced channel's vanishing coherence alone. “Preserves all source matrix units exactly” means reproduces **C's specified action** on every matrix unit: retained coherences survive, u population resets to p, and u-retained coherences vanish. It does not mean that U's reduced map fixes every matrix unit. The manuscript states these distinctions explicitly; the raw answer is preserved unchanged.

The review's empty `limitations` array removes none of the author's stated scope. QR_epsilon, full rank/known spectrum, source correspondence and physical ownership/access remain supplied/new. No general coherent-input population-only receiver formula is adopted. No approximate-channel, mixed-initial-receiver, spectral-uncertainty or general-noise robustness theorem is claimed. Zero probability contrast in one effect is not generally complete-receiver blindness. No new mathematical priority or physical law claim is made.

## Validation and retained evidence

Both GitHub jobs passed. The separate publication job reread five source documents plus two immutable helper files and verified prompt/request/raw-response/verdict/run identity. The downloaded original ZIPs match GitHub digests and byte sizes, 82,874 and 792. Complete member manifests, exact input packet and raw parsed response relationship were checked locally. The archive under `evidence/43336512365/` includes both original ZIPs, all extracted members, full decoded logs and run/job/artifact metadata.

Eight evidence-plumbing tests passed locally and on GitHub after an initial expected RED for the absent new controller. A separate read-only adaptation review found no new defect. All eleven controller function bodies are unchanged from the already inspected exact-QR controller after normalizing its success-log label. Two inherited minor automated-schema gaps were checked manually: all ten proof-check strings and the next-native-obligation are present, and redundant manifest status/returned-model fields match the raw response and completed run. The original raw review and download receipt document these checks. The only CI warnings were upstream Node-action deprecations; jobs completed successfully.

No scientific simulation, numerical enumeration, inherited-stack replay or post-merge scientific audit was run. The proof was known before freeze. The completed analytical review/publication contract supports human review of this conditional addition, not a merge or native certification.

## Next obligation

Establish from native structure why the actual nominated receiver satisfies an independently justified bound q_0<epsilon_* and why its fixed effect is available, while respecting the actual bath/resource assumptions. The conditional threshold identifies a sufficient and sharp restriction within this supplied benchmark; it does not itself supply that restriction or the event-to-owner relation. Existing PR130/131 holds and stopped campaigns remain unchanged.
